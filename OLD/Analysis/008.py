import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster

phone_color = "#ff7f0e"
watch_color = "#1f77b4"
diff_color = "#7f7f7f"
df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
survey = pd.read_excel("../survey_result.xlsx")

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
weeks_first = chunks.query("user == '001_andys600'").groupby(["week_first","weekday_first"]).agg(p_act = ("detected", n_phone),w_act = ("detected", n_watch),b_act = ("detected", n_both))
weeks_first.index.rename(["week","weekday"],inplace=True)
weeks_last = chunks.query("user == '001_andys600'").groupby(["week_last","weekday_last"]).agg(p_act = ("detected", n_phone),w_act = ("detected", n_watch),b_act = ("detected", n_both))
weeks_last.index.rename(["week","weekday"],inplace=True)

weeks = weeks_first.add(weeks_last, fill_value=0)
print(weeks.head())
weeks = weeks.reindex(pd.MultiIndex.from_product([range(6), range(7)], names =["week","weekday"])).fillna(0)

fig, ax =plt.subplots(nrows = 6, ncols = 1, figsize = (4, 5), sharex = True, constrained_layout = True)
for i in range(6):
    ax[i].set_ylabel(f"W{i+1}", rotation = 0, labelpad  =20)
    ax[i].plot(weeks.values[7*i:7*(i+1),0], label = "phone" , c= phone_color)
    ax[i].plot(weeks.values[7*i:7*(i+1),1], label = "watch" , c= watch_color)    
    ax[i].plot(weeks.values[7*i:7*(i+1),2], label = "both" , c= diff_color)
    ax[i].set_yticks([])
ax[5].legend()
ax[5].set_xticks(range(7))
ax[5].set_xticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
plt.savefig("../Fig/008.png")

p_ratio = (weeks.values[:,0]/(weeks.values[:,0]+weeks.values[:,2])).reshape(-1,7)
w_ratio = (weeks.values[:,1]/(weeks.values[:,1]+weeks.values[:,2])).reshape(-1,7)
# p_std = np.std(p_ratio[~np.isnan(p_ratio)], axis = 0)
# w_std = np.std(w_ratio[~np.isnan(w_ratio)], axis = 0)
p_mean = np.mean(p_ratio[~np.isnan(p_ratio)], axis = 0)
w_mean = np.mean(w_ratio[~np.isnan(w_ratio)], axis = 0)
print(p_mean,w_mean)
# print(p_std, w_std)
for i in range(7):
    p_ratio[:,i][np.isnan(p_ratio[:,i])]= np.mean(p_ratio[:,i][~np.isnan(p_ratio[:,i])])
    w_ratio[:,i][np.isnan(w_ratio[:,i])]= np.mean(w_ratio[:,i][~np.isnan(w_ratio[:,i])])
plt.clf()
fig, ax =plt.subplots(nrows = 1, ncols = 1, figsize = (4, 2), constrained_layout = True)
plt.plot(range(7),p_ratio.mean(axis = 0), label="phone", c= phone_color)
plt.plot(range(7),w_ratio.mean(axis = 0), label="watch", c= watch_color)
plt.ylabel("Ratio")
plt.xticks(range(7),["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
plt.savefig("../Fig/008-1.png")