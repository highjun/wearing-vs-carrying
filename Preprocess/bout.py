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

df = df.set_index(['uid', 'timestamp', 'device'])[['step', "speed","distance", "calorie", "run", "walk"]]
df = df.unstack(level = 2)
df.columns = ["phone_step","watch_step","phone_speed","watch_speed","phone_distance","watch_distance","phone_calorie","watch_calorie", "phone_run","watch_run","phone_walk","watch_walk"]
df = df.reset_index().rename({'level_0':'uid','level_1':'timestamp'})
df.sort_values(["uid","timestamp"], inplace= True)

bidx = []
for user in sorted(set(df['uid'])):
    udf = df.query(f"uid == @user")
    diff = udf['timestamp'].diff().dt.total_seconds()//60
    diff = np.array([1 if val != 1 else 0 for val in diff])
    bidx += list(diff.cumsum())
df['bidx'] = bidx

for val in ["speed","distance","calorie", 'step', 'run','walk']:
    df[val] = df[['phone_'+val, 'watch_'+val]].mean(axis = 1)
df.to_csv("integrated_include_bidx.csv")

df = df.groupby(["uid","bidx"]).agg(first = ('timestamp','first'), last = ('timestamp','last'), 
pstep = ('phone_step','sum'), wstep = ('watch_step','sum'), step = ('step','sum'),
pdist = ('phone_distance', 'sum'), wdist = ('watch_distance','sum'), dist = ('distance','sum'),
pspeed= ('phone_speed','mean'), wspeed = ('watch_speed','mean'), speed=('speed','mean'),
pcal = ('phone_calorie','sum'),wcal = ('watch_calorie','sum'), cal = ('calorie','sum'),
prun = ('phone_run','sum'), wrun = ('watch_run','sum'), run = ('run','sum'),
pwalk = ('phone_walk','sum'), wwalk = ('watch_walk','sum'), walk = ('walk','sum'))


df['btype'] = ['b' if val[0] > 0 and val[1]> 0 else ('p' if val[0]> 0 else 'w') for val in df[['pstep','wstep']].to_numpy()] 

df['hour'] = df['first'].dt.hour
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = (df[['first','last']].diff(axis = 1)['last'].dt.total_seconds()//60) + 1

df = df.reset_index()

df.to_csv(os.path.join(data_dir,f'{cur}.csv'))