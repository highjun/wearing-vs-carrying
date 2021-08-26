import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

phone_color = "#ff7f0e"
watch_color = "#1f77b4"

df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
tmp = df.groupby(["user","both_chunk_idx","device"]).agg(step = ("step","sum")).unstack(level="device").droplevel(level=0,axis = 1).fillna(0)
# tmp
x = df.groupby(["user","both_chunk_idx"]).agg(day=("day","first"), hour = ("hour","first"))
tmp["day"] = x["day"]
tmp["hour"] = x["hour"]
tmp = tmp.query("phone > 0  and watch > 0").groupby(["user","day","hour"]).sum()
# print(tmp.index.get_level_values(0))

fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (12,4), constrained_layout = True)
data = tmp.query("user == '001_andys600' and day >= 0 and day< 10").droplevel(level="user")
data = data.reindex(pd.MultiIndex.from_product([range(0,10),range(24)])).fillna(0)
plt.plot(range(24*10),data.values[:,0], label = "phone", c = phone_color)
plt.plot(range(24*10),data.values[:,1], label = "watch", c = watch_color)
plt.legend()
plt.xticks(range(0,24*10+6,6), [str(i%24).zfill(2) for i in range(0,24*10+6,6)])
plt.xlabel('''Hour

Difference of Both-detected Hourly step counts: P0 Day 1~10''')
plt.ylabel("Step counts")
plt.savefig("../Fig/004.png")