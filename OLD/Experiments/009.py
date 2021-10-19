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
week_data = data.groupby(["user", "day", "hour", "device"]).sum().groupby(["user","day","hour"]).agg(phone=("step","first"), watch=("step","last"), diff =("step", diff)).reset_index(level=2)
fig, ax = plt.subplots(nrows=2, ncols= 2, constrained_layout = True, figsize= (16,8), sharey= True)
ax = ax.flatten()
for idx, ax_ in enumerate(ax):
    if idx == 0:
        ax_.boxplot([week_data.query(f"hour== {i}")["diff"] for i in range(24)])
        ax_.set_title("Total")
    else:
        ax_.boxplot([week_data.query(f"user == {idx} and hour== {i}")["diff"] for i in range(24)])
        ax_.set_title(f"User {idx}")
    ax_.set_xticks(np.arange(1,25))
    ax_.set_xticklabels([f"{i}-{i+1}" for i in range(24)], rotation= 45)

fig.supxlabel('''boxplot of hourly step for daily pattern 

Daily Pattern of difference
''')
fig.supylabel("Step difference")
plt.savefig("../Figure/009.png")