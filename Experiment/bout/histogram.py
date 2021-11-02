import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_path  = os.path.join(cwd, 'all_users.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])
color = ['tab:blue', 'tab:orange', 'tab:green']

#step count distribution
df = df.groupby(['users','device','bout']).agg({'step':['sum','count'], 'timestamp':['first','last']})

df.columns = df.columns.droplevel()
df.rename({'sum':'step','count':'duration'},axis = 1, inplace=True)
df = df.reset_index().rename({'level_0':'users','level_1':'device','level_2':'bout'})
fig, ax = plt.subplots(nrows =3, ncols = 2, figsize = (12,12),constrained_layout = True)

p_step = np.array(df.query("device == 'phone'")["step"])
p_step ,bins= np.histogram(p_step, bins = np.arange(0,1000, 50))

w_step = np.array(df.query("device == 'watch'")["step"])
w_step ,bins= np.histogram(w_step, bins = np.arange(0,1000, 50))

ax[0][0].bar(x= list(np.arange(0.5,20.5-1)), height = p_step, width = .8, bottom = 0, color = color[0])
ax[0][1].bar(x= list(np.arange(0.5,20.5-1)), height = w_step, width = .8, bottom = 0, color = color[1])
ax[0][0].set_xticks(np.arange(0.5,20.5-1))
ax[0][0].set_xticklabels(np.arange(0,(20-1)*50,50), fontsize =7)
ax[0][1].set_xticks(np.arange(0.5,20.5-1))
ax[0][1].set_xticklabels(np.arange(0,(20-1)*50,50), fontsize =7)


p_duration = np.array(df.query("device == 'phone'")["duration"])
p_duration ,bins= np.histogram(p_duration, bins = np.arange(1,25))

w_duration = np.array(df.query("device == 'watch'")["duration"])
w_duration ,bins= np.histogram(w_duration, bins = np.arange(1,25))

ax[1][0].bar(x= list(np.arange(0.5,24.5-1)), height = p_duration, width = .8, bottom = 0, color = color[0])
ax[1][1].bar(x= list(np.arange(0.5,24.5-1)), height = w_duration, width = .8, bottom = 0, color = color[1])
ax[1][0].set_xticks(np.arange(0.5,24.5-1))
ax[1][0].set_xticklabels(np.arange(1,24))
ax[1][1].set_xticks(np.arange(0.5,24.5-1))
ax[1][1].set_xticklabels(np.arange(1,24))

phone_interarrival = []
watch_interarrival = []
for user in set(df['users']):
    prev_row = None
    for idx, row in df.query(f"users =={user} and device =='phone'").iterrows():
        if prev_row is not None:
            phone_interarrival.append((row['first'] - prev_row['last']).total_seconds()/60)
        prev_row = row        
    prev_row = None
    for idx, row in df.query(f"users =={user} and device =='watch'").iterrows():
        if prev_row is not None:
            watch_interarrival.append((row['first'] - prev_row['last']).total_seconds()/60)
        prev_row = row

p_interarrival = np.array(phone_interarrival)
p_interarrival ,bins= np.histogram(p_interarrival, bins = np.arange(0,200,10))

w_interarrival = np.array(watch_interarrival)
w_interarrival ,bins= np.histogram(w_interarrival, bins = np.arange(0,200,10))

ax[2][0].bar(x= list(np.arange(0.5,20.5-1)), height = p_interarrival, width = .8, bottom = 0, color = color[0])
ax[2][1].bar(x= list(np.arange(0.5,20.5-1)), height = w_interarrival, width = .8, bottom = 0, color = color[1])
ax[2][0].set_xticks(np.arange(0.5,20.5-1))
ax[2][0].set_xticklabels(np.arange(0,200-10,10),fontsize = 7)
ax[2][1].set_xticks(np.arange(0.5,20.5-1))
ax[2][1].set_xticklabels(np.arange(0,200-10,10),fontsize = 7)

ax[0][0].set_ylabel('Step', fontsize = 16)
ax[1][0].set_ylabel('Duration', fontsize = 16)
ax[2][0].set_ylabel('Interarrival', fontsize = 16)
ax[2][0].set_xlabel('Phone', fontsize = 16)
ax[2][1].set_xlabel('Watch', fontsize = 16)
plt.savefig(os.path.join(cwd,'Fig','bout_histogram.png'))
