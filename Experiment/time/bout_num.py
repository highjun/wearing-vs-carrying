import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
cwd = os.getcwd()
data_path  = os.path.join(cwd, 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
color = plt.get_cmap('Set2')(np.linspace(0.2,0.45, 3))
#step count distribution
df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
fig, ax = plt.subplots(nrows =1, ncols = 1, figsize = (6,4),constrained_layout = True)
# users = list(set(df["users"]))
df = df.query('users == 3')
df['hour'] = pd.to_datetime(df['first']).dt.hour
tmp = df.groupby(['hour','bout_type']).count()
tmp = tmp.reindex(pd.MultiIndex.from_product([list(range(24)), ['p','w','b']]), fill_value = 0)
# print(tmp)
tmp = tmp.reset_index().rename(columns={'level_0':'hour','level_1':'bout_type'})

plt.plot(range(24), tmp.query("bout_type == 'p'")["phone"],label='phone', color = color[2])
plt.plot(range(24), tmp.query("bout_type == 'w'")["phone"],label='watch', color = color[1])
plt.plot(range(24), tmp.query("bout_type == 'b'")["phone"],label='both',color = color[0])
plt.legend()
plt.savefig(os.path.join(cwd,'Fig','bout_per_time.png'))
