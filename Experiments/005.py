# Difference in Daily Step count from phone and watch

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

daily_step = data.groupby(["user","day","device"]).agg(step = ("step","sum"))

fig, ax= plt.subplots(nrows= 1, ncols= 4, figsize = (16,4), sharey= True, constrained_layout = True)
ax[0].boxplot([daily_step.query("device == 'phone'")["step"], daily_step.query("device == 'watch'")["step"], np.array(daily_step.query("device=='phone'")["step"])- np.array(daily_step.query("device=='watch'")["step"])], showfliers = True)
ax[0].set_title("Total")
ax[0].axhline(y=0, ls = "--", c='r', lw = 0.3)

for i in range(1,4):
    ax[i].boxplot([daily_step.query(f"user == {i}").query("device == 'phone'")["step"], daily_step.query(f"user == {i}").query("device == 'watch'")["step"], np.array(daily_step.query(f"user == {i}").query("device=='phone'")["step"])- np.array(daily_step.query(f"user == {i}").query("device=='watch'")["step"])], showfliers = True)
    ax[i].axhline(y=0, ls = "--", c='r',lw = 0.3)
    ax[i].set_title(f"User {i}")


fig.supxlabel('''Users

Phone, Watch, Phone-Watch Boxplot for Daily Step
''')
fig.supylabel("Step Counts")
plt.savefig("../Figure/005.png")