# Activity Statistics
# Histogram for each participants

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

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

def scale_sum(x):
    return np.sum(x)/60000
def scale_cnt(x):
    return len(x)/2
def scale_mean(x):
    return np.mean(x)/100

phone_act = data.query("phone_act_idx!=0").query("device == 'phone'").groupby(["user","phone_act_idx"]).agg(duration = ('duration',scale_sum), step = ('step','sum'))
watch_act = data.query("watch_act_idx!=0").query("device == 'watch'").groupby(["user","watch_act_idx"]).agg(duration = ('duration',scale_sum), step = ('step','sum'))

fig, ax = plt.subplots(1,3, figsize = (12,4), constrained_layout = True)
ax[0].hist([phone_act.query("user==1")["duration"], watch_act.query("user==1")["duration"]], bins = np.arange(9)-0.5, label= ["phone","watch"])
ax[1].hist([phone_act.query("user==2")["duration"], watch_act.query("user==2")["duration"]], bins = np.arange(9)-0.5, label= ["phone","watch"])
ax[2].hist([phone_act.query("user==3")["duration"], watch_act.query("user==3")["duration"]], bins = np.arange(9)-0.5, label= ["phone","watch"])
for i in range(3):
    ax[i].set_title(f"User {i+1}")

fig.supxlabel("Activity duration Distribution per User")
fig.supylabel("# of Activity")
plt.legend()

plt.savefig("../Figure/001.png")
