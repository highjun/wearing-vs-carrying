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
#step count distribution of Type A
df = df.set_index(['users', 'timestamp', 'device'])[['step']]
print(df)
df = df.unstack(level = 2, fill_value = 0)
df.columns = df.columns.droplevel()
df = df.reset_index().rename({'level_0':'users','level_1':'timestamp'})
bout_type= []
bout_idx = []
for user in set(df['users']):
    n_saved = 0
    prev_row = None
    bout_ = 0
    p, w = False, False
    for idx, row in df.query(f"users == {user}").iterrows():
        if prev_row is not None and (row['timestamp']-prev_row['timestamp']).total_seconds()/60 == 1:
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
print(df)
df.to_csv(os.path.join(cwd,'bout.csv'))