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

fig, ax = plt.subplots(nrows =1, ncols =1)

step = np.array(df["step"])
duration = np.array(df["duration"])

ax.scatter(duration, step, s= 4)
ax.set_xlabel('''Duration

Scatter Plot for step count and duration for bout
''')
ax.set_ylabel("Step count")

plt.savefig(os.path.join(cwd,'Fig','step_dut_scatter.png'))
