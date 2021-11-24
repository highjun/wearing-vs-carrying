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
fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (12,3),constrained_layout = True)

p_step = np.array(df.query("device == 'phone'")["step"])
p_step ,bins= np.histogram(p_step, bins = np.arange(0,55, 5))

w_step = np.array(df.query("device == 'watch'")["step"])
w_step ,bins= np.histogram(w_step, bins = np.arange(0,55, 5))

ax[0].bar(x= list(np.arange(0.5,11.5-1)), height = p_step, width = .8, bottom = 0, color = color[0])
ax[1].bar(x= list(np.arange(0.5,11.5-1)), height = w_step, width = .8, bottom = 0, color = color[1])
ax[0].set_xticks(np.arange(0,11))
ax[0].set_xticklabels(np.arange(0,55,5), fontsize =7)
ax[1].set_xticks(np.arange(0,11))
ax[1].set_xticklabels(np.arange(0,55,5), fontsize =7)

ax[0].set_ylabel('Step', fontsize = 16)
# ax[1][0].set_ylabel('Duration', fontsize = 16)
# ax[2][0].set_ylabel('Interarrival', fontsize = 16)
ax[0].set_xlabel('Phone', fontsize = 16)
ax[1].set_xlabel('Watch', fontsize = 16)
# fig.supxlabel('''', fontsize = 16)
plt.savefig(os.path.join(cwd,'Fig','bout_histogram_subdiv.png'))
