import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd
import numpy as np
import os

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'Preprocess')
all_users = []
for csv in os.listdir(data_dir):
    data = pd.read_csv(os.path.join(data_dir,csv),index_col= 0, header = 0, encoding = 'utf-8')
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(['timestamp','device'], inplace= True)
    data = data.groupby(['timestamp','date','weekday','hour','device']).sum()
    # data.set_index(['timestamp','device'])
    # data.reindex(pd.MultiIndex.from_product([list(set(data.index.get_level_values(0))),['phone','watch']]), fill_value = 0,inplace = True)
    data = data.reset_index().rename({'level_0':'timestamp','level_1':'date','level_2':'weekday','level_3':'hour','level_4':'device'})
    prev_phone_timestamp = None
    prev_watch_timestamp = None
    cur_phone_bout_idx = -1
    cur_watch_bout_idx = -1

    bout = []
    for idx, row in data.iterrows():
        if row['device'] == 'phone':
            if prev_phone_timestamp is None or (row['timestamp']-prev_phone_timestamp).total_seconds()> 60:
                cur_phone_bout_idx += 1
            bout.append(cur_phone_bout_idx)
            prev_phone_timestamp = row['timestamp']
                
        else:
            if prev_watch_timestamp is None or (row['timestamp']-prev_watch_timestamp).total_seconds()> 60:
                cur_watch_bout_idx += 1
            bout.append(cur_watch_bout_idx)
            prev_watch_timestamp = row['timestamp']
        
    data['bout'] = bout
    data['users'] = [os.path.splitext(csv)[0]]*data.shape[0]
    all_users.append(data)
all_users = pd.concat(all_users, ignore_index= True)
all_users.to_csv(os.path.join(cwd,'all_users.csv'))