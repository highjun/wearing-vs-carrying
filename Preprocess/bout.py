import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

cur = os.path.splitext(os.path.basename(__file__))[0]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_dir = os.path.join(cwd, "Data")
data_path  = os.path.join(data_dir, 'integrated.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])

df = df.set_index(['users', 'timestamp', 'device'])[['step', "speed","distance", "calorie"]]
df = df.unstack(level = 2, fill_value = 0)
# df.columns = df.columns.droplevel()
df.columns = ["phone","watch","phone_speed","watch_speed","phone_distance","watch_distance","phone_calorie","watch_calorie"]
# print(df)
df = df.reset_index().rename({'level_0':'users','level_1':'timestamp'})
df.sort_values(["users","timestamp"], inplace= True)
# df.to_csv("tmp.csv")
bout_type= []
bout_idx = []
for user in sorted(set(df['users'])):
    n_saved = 0
    prev_row = None
    bout_ = 0
    p, w = False, False
    for idx, row in df.query(f"users == '{user}'").iterrows():
        # if prev_row is not None:
        #     print(idx, row["timestamp"], prev_row["timestamp"])
        if prev_row is not None and (row['timestamp']-prev_row['timestamp']).total_seconds()//60 == 1:
            n_saved += 1
            p = p or row['phone'] > 0
            w = w or row['watch'] > 0
        else:
            bout_type +=  ['b' if p and w else ('w' if w else 'p')]* n_saved
            bout_ += 1
            n_saved = 1
            p = row['phone'] > 0
            w = row['watch'] > 0
        bout_idx.append(bout_)
        prev_row = row
    bout_type +=  ['b' if p and w else ('w' if w else 'p')]* n_saved
df['bout_type'] = bout_type
df['bout_idx'] = bout_idx
df['speed'] = [(row['phone_speed']+row['watch_speed'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
df["distance"] = [(row['phone_distance']+row['watch_distance'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
df["calorie"] = [(row['phone_calorie']+row['watch_calorie'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]

def nonzero_mean(data):
    return np.mean(data[data!= 0])


df = df.groupby(["users","bout_idx"]).agg(first = ('timestamp','first'), last = ('timestamp','last'), phone = ('phone','sum'), watch = ('watch','sum'), step = ('step','sum'),
phone_distance = ('phone_distance', 'sum'), watch_distance = ('watch_distance','sum'), distance = ('distance','sum'),
phone_speed= ('phone_speed',nonzero_mean), watch_speed = ('watch_speed',nonzero_mean), speed=('speed','mean'),
phone_calorie = ('phone_calorie','sum'),watch_calorie = ('watch_calorie','sum'),calorie = ('calorie','sum'),bout_type=('bout_type','first'))
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
df['hour'] = df['first'].dt.hour + df['first'].dt.minute/60
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = [(row['last']-row['first']).seconds/60+1 for _, row in df.iterrows()]

# Bout의 분류
df['night'] = [1 if hour> 18 or hour < 9 else 0 for hour in df['hour']]
df['weekend'] = [1 if weekday>=5 else 0 for weekday in df['weekday']]
survey = pd.read_csv(os.path.join(os.getcwd(),"Data",'survey.csv'), header = 0)
routine = []
df = df.reset_index().rename({'level_0':'users'})
routine = []
for _, row in df.iterrows():
    user = row["users"]
    sleep, wake, work, home = list(survey.query(f"id == '{user}'")[["sleep", "wake", "work", "home"]].values)[0]
    hour = row["hour"]
    j = 0
    if wake < hour:
        j += 1
    if work < hour:
        j += 1
    if home < hour:
        j += 1
    if sleep > 12 and hour > sleep:
        j = 0
    routine.append(j)
df["routine"] = routine
## Wearing Day Ratio
tmp = df.groupby(["users", "date","bout_type"]).agg(step = ("step","sum"))
tmp = tmp.unstack(level=2, fill_value = 0)
tmp.columns = ['b','p','w']
tmp = tmp.apply(lambda x: x/np.sum(x),axis = 1)
tmp = tmp.reset_index()

df["date_wearing_ratio"] =[tmp.query("date == @row['date'] and users == @row['users']")["p"].values[0] for idx,row in df[["date","users"]].iterrows()]


df.to_csv(os.path.join(data_dir,f'{cur}.csv'))