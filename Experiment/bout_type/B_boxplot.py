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
step =[]
duration =[]

for idx in set(df['users']):
    step.append((np.array(df.query(f"users=={idx} and bout_type=='b'")["phone"])+np.array(df.query(f"users=={idx} and bout_type=='b'")["watch"]))/2)
    duration.append(df.query(f"bout_type=='b' and users =={idx}")["duration"])

fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (12,4),constrained_layout = True)
ax[0].boxplot(step)
ax[1].boxplot(duration)
ax[0].set_xlabel('step')
ax[0].set_xlabel('duration')
plt.savefig(os.path.join(cwd,'Fig','bout_B_boxplot.png'))
