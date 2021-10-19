# Grouping Hourly Intervals
# Coloring of each hour by existence of activity

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

fig, ax = plt.subplots(1,1, figsize=(6,18))

c = ['white','lightcoral','limegreen','slateblue','gold','darkorange', 'olive', 'deeppink', 'skyblue']
label = []
idx = 0
for i in range(hour_features.shape[0]):
    p_c = hour_features.iloc[i]["p_c"]
    w_c = hour_features.iloc[i]["w_c"]
    b_c = hour_features.iloc[i]["b_c"]
    idx = (4 if p_c >0 else 0) + (2 if w_c>0 else 0) #+ (1 if b_c>0 else 0)
    label.append(idx)
width = .2
height = .5
group_size = hour_features.groupby(["user"]).size()
plt.xlim([0, 24* width])
plt.ylim([0, hour_features.shape[0]//24* height])
for i in range(hour_features.shape[0]):
    row = hour_features.iloc[i]
    ch = 1

    rect = matplotlib.patches.Rectangle(((i%24)*width, (i//24)*height),width,height,color = c[label[i]], alpha = ch)
    ax.add_patch(rect)
for i in range(hour_features.shape[0]//24):
    plt.axhline(y=height*i, color='k', linestyle='-')
lower = 0
yticklabel = []
for i in group_size:
    lower += i//24
    plt.axhline(y=height*lower, color='r', linestyle='-')
    yticklabel += list(range(i//24))
for i in range(1,4):
    plt.axvline(x=width*i*6, color ='k',linestyle='--')
plt.yticks(np.linspace(.5*height,(hour_features.shape[0]//24-.5)*height,hour_features.shape[0]//24), yticklabel)
plt.xticks(np.linspace(0,24*width,25), range(25))
plt.ylabel("Different Days per User")
plt.xlabel('''Hour

Yellow = Phone-only, Green = Watch-only, Olive = Both
''')
plt.savefig("../Figure/004.png")