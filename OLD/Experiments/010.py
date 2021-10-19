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

def scale_sum(x):
    return np.sum(x)/2
def scale_cnt(x):
    return len(x)/2
def scale_mean(x):
    return np.mean(x)/100
phone_act = data.query("by == 'phone'").query("phone_act_idx!=0").query("device == 'phone'").groupby(["user","phone_act_idx"]).agg(day = ('day','first'), hour = ('hour','first'), n_min = ('duration','count'), step = ('step','sum'))
watch_act = data.query("by == 'watch'").query("watch_act_idx!=0").query("device == 'watch'").groupby(["user","watch_act_idx"]).agg(day = ('day','first'), hour = ('hour','first'), n_min = ('duration','count'), step = ('step','sum'))
both_act = data.query("by == 'both'").query("comb_act_idx!=0").groupby(["user","comb_act_idx"]).agg(day = ('day','first'), hour = ('hour','first'), n_min = ('duration',scale_cnt), step = ('step',scale_sum))

phone_act = phone_act.groupby(["user","day","hour"]).agg(cnt =("step","count"), mean = ("step",scale_mean))
watch_act = watch_act.groupby(["user","day","hour"]).agg(cnt =("step","count"), mean = ("step",scale_mean))
both_act = both_act.groupby(["user","day","hour"]).agg(cnt =("step","count"), mean = ("step",scale_mean))

phone_act= phone_act.reset_index().set_index(["user","day","hour"]).reindex(pd.MultiIndex.from_product([range(1,n_user+1),range(36), range(24)], names= ["user", "day", "hour"])).fillna(0)
watch_act= watch_act.reset_index().set_index(["user","day","hour"]).reindex(pd.MultiIndex.from_product([range(1,n_user+1),range(36), range(24)], names= ["user", "day", "hour"])).fillna(0)
both_act= both_act.reset_index().set_index(["user","day","hour"]).reindex(pd.MultiIndex.from_product([range(1,n_user+1),range(36), range(24)], names= ["user", "day", "hour"])).fillna(0)

hour_features = pd.concat([phone_act.rename(columns = {'cnt':'p_c','mean':'p_m'}),watch_act.rename(columns = {'cnt':'w_c','mean':'w_m'}),both_act.rename(columns = {'cnt':'b_c','mean':'b_m'})], axis = 1)

hour_features = hour_features[hour_features.T.any()!=0]
hour_features = hour_features.reset_index()

import datetime as dt
import matplotlib
fig, axes = plt.subplots(nrows = 1, ncols = 3, constrained_layout = True, figsize = (12,6))
for idx in range(3):
    axes[idx].set_title(f"User {idx+1}")
    axes[idx].set_xlim([0,24])
    total_day = (dt.datetime.strptime(setting[f"P{idx+1}"][1], '%Y-%m-%d %H:%M') - dt.datetime.strptime(setting[f"P{idx+1}"][0], '%Y-%m-%d %H:%M')).days
    axes[idx].set_ylim([0, total_day])
    
    for i in range(total_day):
        axes[idx].axhline(y = i, c='k',ls='-')
    for i in range(4):
        axes[idx].axvline(x = i*6, c='k',ls='--')
    for label, row in hour_features.query(f"user == {idx +1}").iterrows():
        rect = None
        if row["p_c"]> 0 and row["w_c"]> 0:
            rect = matplotlib.patches.Rectangle((row["hour"], row["day"]),1, 1, color= 'y')
        elif row["p_c"]>0:    
            rect = matplotlib.patches.Rectangle((row["hour"], row["day"]),1, 1,color = plt.cm.Blues(row["p_c"]/3))
        elif row["w_c"]>0:
            rect = matplotlib.patches.Rectangle((row["hour"], row["day"]),1, 1,color = plt.cm.Reds(row["w_c"]/3))
        # if row["b_c"] + row["w_c"] > 0:
        #     rect= matplotlib.patches.Rectangle((row["hour"], row["day"]),1, 1,color = 'g')
        if rect is not None:
            axes[idx].add_patch(rect)
fig.supylabel("Day")
fig.supxlabel('''Hours

Intensity for single activity, blue means phone and red means watch,
gold means each of single activity emerged in the hour''')

plt.savefig("../Figure/010.png")