import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_path  = os.path.join(cwd, 'all_users.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)

#step count distribution
df = df.groupby(['users','device','bout']).agg({'step':['sum','count'], 'timestamp':['first','last']})
df.columns = df.columns.droplevel()
df.rename({'sum':'step','count':'duration'},axis = 1, inplace=True)
df = df.reset_index().rename({'level_0':'users','level_1':'device','level_2':'bout'})
phone_steps = []
phone_durations = []
watch_steps = []
watch_durations = []
for idx in set(df['users']):
    phone_steps.append(df.query(f"device=='phone' and users =={idx}")["step"])
    watch_steps.append(df.query(f"device=='watch' and users =={idx}")["step"])
    phone_durations.append(df.query(f"device=='phone' and users =={idx}")["duration"])
    watch_durations.append(df.query(f"device=='watch' and users =={idx}")["duration"])

fig, ax = plt.subplots(nrows =2, ncols = 2, figsize = (12,8),constrained_layout = True)
ax[0][0].boxplot(phone_steps)
ax[0][1].boxplot(watch_steps)
ax[1][0].boxplot(phone_durations)
ax[1][1].boxplot(watch_durations)
plt.setp(ax[0, 0], ylabel='Step')
plt.setp(ax[1, 0], ylabel='Duration')
plt.setp(ax[1, 0], xlabel='Phone')
plt.setp(ax[1, 1], xlabel='Watch')
plt.savefig(os.path.join(cwd,'Fig','bout_dist_boxplot.png'))
