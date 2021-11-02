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
pstep =[]
wstep =[]
pduration =[]
wduration =[]

for idx in set(df['users']):
    pstep.append(df.query(f"bout_type=='p' and users =={idx}")["phone"])
    wstep.append(df.query(f"bout_type=='w' and users =={idx}")["watch"])
    pduration.append(df.query(f"bout_type=='p' and users =={idx}")["duration"])
    wduration.append(df.query(f"bout_type=='w' and users =={idx}")["duration"])

fig, ax = plt.subplots(nrows =2, ncols = 2, figsize = (12,8),constrained_layout = True)
ax[0][0].boxplot(pstep)
ax[0][1].boxplot(wstep)
ax[1][0].boxplot(pduration)
ax[1][1].boxplot(wduration)
plt.setp(ax[0, 0], ylabel='Step')
plt.setp(ax[1, 0], ylabel='Duration')
plt.setp(ax[1, 0], xlabel='Phone')
plt.setp(ax[1, 1], xlabel='Watch')
plt.savefig(os.path.join(cwd,'Fig','bout_A_boxplot.png'))
