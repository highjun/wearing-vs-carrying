import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_path  = os.path.join(cwd, 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)

#step count distribution
df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
print(df)
fig, ax = plt.subplots(nrows =2, ncols = 2, figsize = (12,8),constrained_layout = True)
ax[0][0].hist(df.query(f"bout_type=='p'")["phone"], np.arange(0,2000, 50))
ax[0][1].hist(df.query(f"bout_type=='w'")["watch"], np.arange(0,2000, 50))
ax[1][0].hist(df.query(f"bout_type=='p'")["duration"], np.arange(0,60))
ax[1][1].hist(df.query(f"bout_type=='p'")["duration"], np.arange(0,60))
plt.setp(ax[0, 0], ylabel='Step')
plt.setp(ax[1, 0], ylabel='Duration')
plt.setp(ax[1, 0], xlabel='Phone')
plt.setp(ax[1, 1], xlabel='Watch')
plt.savefig(os.path.join(cwd,'Fig','bout_A_historgram.png'))
