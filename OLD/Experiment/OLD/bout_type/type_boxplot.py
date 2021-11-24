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
# print(df)
pstep =[]
wstep =[]
bstep = []
# pduration =[]
# wduration =[]

for idx in set(df['users']):
    pstep.append(df.query(f"bout_type=='p' and users =={idx}")["phone"])
    wstep.append(df.query(f"bout_type=='w' and users =={idx}")["watch"])
    bstep.append((np.array(df.query(f"bout_type=='b' and users =={idx}")["phone"])+np.array(df.query(f"bout_type=='b' and users =={idx}")["phone"]))/2)
    # pduration.append(df.query(f"bout_type=='p' and users =={idx}")["duration"])
    # wduration.append(df.query(f"bout_type=='w' and users =={idx}")["duration"])

fig, ax = plt.subplots(nrows =1, ncols = 3, figsize = (15,3), sharey = True)
ax[0].boxplot(pstep, showfliers = False)
ax[0].set_ylim([0,200])
ax[1].boxplot(wstep, showfliers = False)
ax[2].boxplot(bstep, showfliers = False)
ax[0].set_ylabel('Step', fontsize = 16)
# ax[0].set_ylabel('Duration', fontsize = 16)
ax[0].set_xlabel('Phone', fontsize = 16)
ax[1].set_xlabel('Watch', fontsize = 16)
ax[2].set_xlabel('Both', fontsize = 16)
for i in range(3):
    ax[i].set_xticks(list(range(1,len(set(df["users"]))+1)))
    ax[i].set_xticklabels(list(set(df["users"])),fontsize =7)
plt.tight_layout()

plt.savefig(os.path.join(cwd,'Fig','bout_type_boxplot.png'))
