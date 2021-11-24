import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
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
df["distance"] = (np.array(df["phone_distance"]) +np.array(df["watch_distance"]))
df["calorie"] = [(row['phone_calorie']+row['watch_calorie'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]


df = df.groupby(["users","bout_idx"]).agg(first = ('timestamp','first'), last = ('timestamp','last'), phone = ('phone','sum'), watch = ('watch','sum'), distance = ('distance', 'sum'), speed= ('speed','mean'), calorie = ('calorie','sum'),bout_type=('bout_type','first'))
df = df.reset_index().rename({'level_0':'users'})#[['first','last','phone','watch','bout_type','users']]
df.to_csv(os.path.join(data_dir,'bout.csv'))