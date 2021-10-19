import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json
import os

pd.set_option("precision",2)
pd.set_option("expand_frame_repr", False)
pd.set_option("max_columns", 20)
np.printoptions(precision=2, suppress=True)

with open("../setting.json") as f:
    setting = json.load(f)
data_arr = []
for id in sorted(os.listdir("../Raw")):
    data_arr.append(pd.read_excel(f"../Preprocess/{id}.xlsx"))

n_user = len(data_arr)
data = pd.concat(data_arr, keys = list(range(1,n_user+1)))
data["user"] = data.index.get_level_values(0)
data.reset_index(drop = True, inplace = True)

def diff(x):
    x= x.to_numpy()
    return x[0]-x[1]
week_data = data.groupby(["user", "day", "weekday", "device"]).sum().groupby(["user","day","weekday"]).agg(phone=("step","first"), watch=("step","last"), diff =("step", diff)).reset_index(level=2)
fig, ax = plt.subplots(nrows=1, ncols= 4, constrained_layout = True, figsize= (16,4), sharey= True)
ax[0].boxplot([week_data.query(f"weekday== {i}")["diff"] for i in range(7)])
ax[0].set_xticks(range(1,8))
ax[0].set_xticklabels(['Mon','Tue','Wed',"Thu",'Fri',"Sat",'Sun'])
ax[0].set_title("Total")
for idx in range(1,4):
    ax[idx].set_title(f"User {idx}")
    ax[idx].boxplot([week_data.query(f"user == {idx} and weekday== {i}")["diff"] for i in range(7)])
    ax[idx].set_xticks(range(1,8))
    ax[idx].set_xticklabels(['Mon','Tue','Wed',"Thu",'Fri',"Sat",'Sun'])
fig.supxlabel('''boxplot of daily step for weekly pattern 

Weekly Pattern of difference
''')
fig.supylabel("Step difference")
plt.savefig("../Figure/008.png")