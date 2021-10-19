# Correlation between the Duration and Step count
# Scatter Plot and linear regression

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


import json
import os

pd.set_option("precision",2)
pd.set_option("expand_frame_repr", False)
pd.set_option("max_columns", 20)
np.printoptions(precision=2, suppress=True)

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

fig, ax = plt.subplots(1,2, figsize = (8,4), constrained_layout = True)
ax[0].scatter(phone_act["duration"], phone_act["step"])
ax[1].scatter(watch_act["duration"], watch_act["step"])
ax[0].set_title("Phone")
ax[1].set_title("Watch")
x = np.arange(0,int(max(np.max(phone_act["duration"]),np.max(watch_act["duration"])))+1, 1000).reshape(-1,1)
l_phone =LinearRegression().fit(np.array(phone_act["duration"]).reshape(-1,1), np.array(phone_act["step"]))
p_score = l_phone.score(np.array(phone_act["duration"]).reshape(-1,1), np.array(phone_act["step"]))
ax[0].plot(x, l_phone.predict(x), 'y')
ax[0].text(1,1.6,f"R^2= {round(p_score,4)}")
l_watch =LinearRegression().fit(np.array(watch_act["duration"]).reshape(-1,1), np.array(watch_act["step"]))
w_score = l_watch.score(np.array(watch_act["duration"]).reshape(-1,1), np.array(watch_act["step"]))
ax[1].plot(x, l_watch.predict(x), 'y')
ax[1].text(1,1.6,f"R^2= {round(w_score,4)}")

fig.supxlabel('''Duration per User

Correlation between duration and Step count for each Activity
''')
fig.supylabel("Step Counts")

plt.savefig("../Figure/002.png")
