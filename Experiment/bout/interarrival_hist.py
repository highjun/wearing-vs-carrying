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
#step count distribution
df = df.groupby(['users','device','bout']).agg({'step':['sum','count'], 'timestamp':['first','last']})
df.columns = df.columns.droplevel()
df.rename({'sum':'step','count':'duration'},axis = 1, inplace=True)
df = df.reset_index().rename({'level_0':'users','level_1':'device','level_2':'bout'})
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
fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (12,4),constrained_layout = True)
ax[0].hist(phone_interarrival, bins = np.arange(0,600, 10))
ax[1].hist(watch_interarrival, bins = np.arange(0,600, 10))
ax[0].set_xlabel('phone')
ax[1].set_xlabel('watch')
plt.savefig(os.path.join(cwd,'Fig','bout_interarrival_hist.png'))
