import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
cwd = os.getcwd()
data_path  = os.path.join(cwd, 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df = df.query(f'users == 9')
print(df.groupby(['date']).agg(phone=('phone','sum'), watch = ('watch','sum')))
df = df[df['date']==dt.date(2021,7,24)]

color = ['tab:blue', 'tab:orange', 'tab:green']
#step count distribution
df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
users= set(df["users"])

df['hour'] = df['first'].dt.hour
df['weekday'] = df['first'].dt.weekday
df['date'] = df['first'].dt.date

fig, ax = plt.subplots(nrows =1, ncols = 1, figsize = (6,3))#,constrained_layout = True)
tmp = df.groupby(['users','date']).sum()
tmp = tmp.reset_index().rename(columns={'level_0':'users','level_1':'date'})
n_day = tmp.shape[0]

tmp = df.groupby(['hour','bout_type']).agg(phone = ('phone','sum'), watch = ('watch','sum'), duration =('duration','sum'),count = ('bout_type','count'))
tmp = tmp.reindex(pd.MultiIndex.from_product([list(range(24)), ['p','w','b']]), fill_value = 0)
tmp = tmp.reset_index().rename(columns={'level_0':'hour','level_1':'bout_type'})

p_bout = np.array(tmp.query("bout_type == 'p'")["phone"])/n_day
w_bout = np.array(tmp.query("bout_type == 'w'")["watch"])/n_day
b_bout = (np.array(tmp.query("bout_type == 'b'")["watch"])+ np.array(tmp.query("bout_type == 'b'")["phone"]))/n_day/2
data = np.array([p_bout,w_bout,b_bout])
data_cum = data.cumsum(axis = 0)
ax.bar(x= list(np.arange(0.5,24.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
ax.bar(x= list(np.arange(0.5,24.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
ax.bar(x= list(np.arange(0.5,24.5)), height = data[0,:], width = .8, label='phone', color = color[0])

ax.set_xticks(np.arange(0.5,24.5))
ax.set_xticklabels([str(idx).zfill(2) for idx in range(24)])
ax.set_xlabel('Hour')
ax.set_ylabel('step count')
ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(cwd,'check.png'))
plt.close()