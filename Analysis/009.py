import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
import json

users = []
with open("../meta_data.json") as f:
    dicts = json.load(f)
    for vals in dicts.values():
        users.append(vals["folder"])
phone_color = "#ff7f0e"
watch_color = "#1f77b4"
diff_color = "#7f7f7f"
df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
survey = pd.read_excel("../survey_result.xlsx")
survey["user"] = survey.index
for i in ["work_start","work_end","sleep","wake"]:
    survey[i] = pd.to_datetime(survey[i], format="%H:%M:%S")


chunks = df.groupby(["user","both_chunk_idx","device"]).agg(step = ("step","sum")).unstack(level="device").fillna(0).droplevel(level=0, axis=1)

time_info = df.groupby(["user","both_chunk_idx"]).agg(day_first = ("day","first"),day_last = ("day","last"), hour_first = ("hour","first"), hour_last = ("hour","last"), weekday_last = ("weekday","first"), weekday_first = ("weekday","last"))
time_info["week_first"] = [row["day_first"]//7 + (1 if row["day_first"]%7 - row["weekday_first"] > 0 else 0) for _,row in time_info.iterrows()]
time_info["week_last"] = [row["day_last"]//7 + (1 if row["day_last"]%7 - row["weekday_last"] > 0 else 0) for _,row in time_info.iterrows()]
chunks["detected"] = ["both" if (row["phone"] > 0 and row["watch"]> 0) else ("watch" if row["watch"] > 0 else "phone") for _, row in chunks.iterrows()]
chunks = pd.concat([chunks, time_info], axis='columns')
def n_phone(x):
    return np.sum(x == 'phone')/2
def n_watch(x):
    return np.sum(x == 'watch')/2
def n_both(x):
    return np.sum(x == 'both')/2
weeks_first = chunks.groupby(["user","weekday_first"]).agg(p_act = ("detected", n_phone),w_act = ("detected", n_watch),b_act = ("detected", n_both))
weeks_first.index.rename(["user","weekday"],inplace=True)
weeks_last = chunks.groupby(["user","weekday_last"]).agg(p_act = ("detected", n_phone),w_act = ("detected", n_watch),b_act = ("detected", n_both))
weeks_last.index.rename(["user","weekday"],inplace=True)
weeks = weeks_first.add(weeks_last, fill_value=0)

weeks = weeks.reindex(pd.MultiIndex.from_product([users, range(7)], names =["users","weekday"])).fillna(0)

p_ratio = (weeks.values[:,0]/(weeks.values[:,0]+weeks.values[:,2])).reshape(-1,7)
w_ratio = (weeks.values[:,1]/(weeks.values[:,1]+weeks.values[:,2])).reshape(-1,7)
for i in range(7):
    p_ratio[:,i][np.isnan(p_ratio[:,i])]= np.mean(p_ratio[:,i][~np.isnan(p_ratio[:,i])])
    w_ratio[:,i][np.isnan(w_ratio[:,i])]= np.mean(w_ratio[:,i][~np.isnan(w_ratio[:,i])])
weeks_ratios = np.concatenate([p_ratio, w_ratio], axis = 1)

# weeks_next_ratios = np.zeros_like(weeks_ratios)
# permute =[1,2,3,4,5,6,0,8,9,10,11,12,13,7]
# for i in range(14):
#     weeks_next_ratios[:,i] = weeks_ratios[:,permute[i]]
# weeks_ratios = weeks_ratios-weeks_next_ratios

n_clusters = 3
km = cluster.KMeans(n_clusters = 3, random_state = 10).fit(weeks_ratios)
labels = km.labels_
centers = km.cluster_centers_
fig, axes = plt.subplots(nrows = 2, ncols = 4, figsize = (12, 8), sharex = True, sharey = True, constrained_layout = True)
ax = axes.flatten()
ax[0].set_title("Mean")
q25 = np.quantile(weeks_ratios, q= 0.25, axis = 0)
q75 = np.quantile(weeks_ratios, q= 0.25, axis = 0)
median = np.quantile(weeks_ratios, q= 0.5, axis = 0)
mean = np.mean(weeks_ratios, axis = 0)
std = np.std(weeks_ratios, axis = 0)
ax[0].plot(range(7), mean[:7], c="r")
ax[0].fill_between(range(7), mean[:7]-std[:7], mean[:7]+std[:7], color = "grey",alpha = 0.2)
ax[4].plot(range(7), mean[7:], c="r")
ax[4].fill_between(range(7), mean[7:]-std[7:], mean[7:]+std[7:], color = "grey",alpha = 0.2)  

each_cluster =[]
for i in range(1,4):
    ax[i].set_title(f"Cluster {i}")
    print(f"cluster {i} has {np.sum(labels == i-1)} points")
    inner_cluster = weeks_ratios[labels == i-1]
    each_cluster.append(np.arange(30)[labels == i-1])
#     inner_max = weeks_diff_ratios.max(axis = 0)
#     inner_min = weeks_diff_ratios.min(axis = 0)
    inner_std = inner_cluster.std(axis = 0)
    inner_mean = inner_cluster.mean(axis = 0)
    inner_mid = np.quantile(inner_cluster, q= 0.5, axis = 0)
    inner_q25 = np.quantile(inner_cluster,q=0.25,axis = 0)
    inner_q75 = np.quantile(inner_cluster, q = 0.75, axis = 0)
    #Median & quantile
    ax[i].plot(range(7), inner_mid[:7], c= 'r')
    ax[i].fill_between(range(7), inner_q25[:7], inner_q75[:7], color = "grey",alpha = 0.2)
    ax[i+4].plot(range(7), inner_mid[7:], c= 'r')
    ax[i+4].fill_between(range(7), inner_q25[7:], inner_q75[7:], color = "grey",alpha = 0.2)
    # Mean & Std
#     ax[i].plot(range(7), inner_cluster[:,:7].mean(axis = 0), c="r")
# #     ax[i].fill_between(range(7), inner_min[:7], inner_max[:7], color = "grey",alpha = 0.2)
#     ax[i].fill_between(range(7), inner_cluster[:,:7].mean(axis = 0)-inner_std[:7], inner_cluster[:,:7].mean(axis = 0)+inner_std[:7], color = "grey",alpha = 0.2)  
#     ax[i+4].plot(range(7), centers[i-1,7:], c="r")
# #     ax[i+4].fill_between(range(7), inner_min[7:], inner_max[7:], color = "grey",alpha = 0.2)
#     ax[i+4].fill_between(range(7), inner_cluster[:,7:].mean(axis = 0)-inner_std[7:], inner_cluster[:,7:].mean(axis = 0)+inner_std[7:], color = "grey",alpha = 0.2)  
    ax[i+4].set_xticks(range(7))
    ax[i+4].set_xticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
fig.supylabel("Detection Ratio")
ax[0].set_ylabel("Phone")
ax[4].set_ylabel("Watch")
fig.supxlabel('''Day of Week

Red lines mean center of cluster and shadows show how points in cluster varied''')

plt.savefig("../Fig/009.png")

cls_info = []
for i in range(3):
    cls_info.append(survey[["user","age","active_level", "work_start","work_end","sleep","wake","w_day","p_look_walk","w_usage","p_usage","afterwork_active_level","weekend_active_level"]].query(f"user in [{','.join([str(tmp) for tmp in each_cluster[i]])}]"))
plt.clf()
n_cols = 5
fig, axes = plt.subplots(nrows = 1, ncols = n_cols, figsize = (16, 4),sharex=True, constrained_layout = True)
ax = axes.flatten()
for idx,val in enumerate(["active_level", "w_usage","p_usage","afterwork_active_level", "weekend_active_level"]):
    ax[idx].boxplot([cls_info[0][val],cls_info[1][val],cls_info[2][val]])
    if val =="w_usage":
        ax[idx].set_title("watch usage time per day")
    elif val =="p_usage":
        ax[idx].set_title("phone usage time per day")
    elif val == "afterwork_active_level":
        ax[idx].set_title("active level after work")
    elif val == "weekend_active_level":
        ax[idx].set_title("active level in weekend")
    elif val == "active_level":
        ax[idx].set_title("active level")
    ax[idx].set_xticks(range(1,4))

fig.supxlabel('''Each Clusters

BoxPlot for comparing survey results''')
plt.savefig("../Fig/009-1.png")
# cls_info = pd.concat(cls_info, keys = [0,1,2], ignore_index= True)
# cls_info["cluster"] = cls_info.index
