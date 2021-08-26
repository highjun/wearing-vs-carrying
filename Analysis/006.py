import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
import json

phone_color = "#ff7f0e"
watch_color = "#1f77b4"
diff_color = "#7f7f7f"
df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
step_count = df.groupby(["user","day","hour","device"]).agg(step = ("step","sum")).unstack(level = "device").droplevel(level = 0, axis = 1).fillna(0)
step_count = step_count.reset_index(level = ["user","day","hour"])
step_count["week"] = [row["day"]//7 + (1 if row["day"]%7 - row["weekday"] > 0 else 0) for idx,row in x.iterrows()]

with open("../meta_data.json")as f:
    j = json.load(f)
users = []
for val in j.values():
    users.append(val['folder'])
id = 3
day_start = 15
day_end = 20
day_count = day_end - day_start
data = step_count.query(f"user == '{users[id]}' and day >= {day_start} and day < {day_end}").droplevel(level = "user")
data = data.reindex(pd.MultiIndex.from_product([range(day_start,day_end), range(24)])).fillna(0).values

plt.subplots(nrows = 1,ncols = 1, figsize = (6,4), constrained_layout = True)
plt.plot(range(24*day_count), data[:,0], label = "phone", c = phone_color)
plt.plot(range(24*day_count), data[:,1], label = "watch", c = watch_color)
plt.plot(range(24*day_count), data[:,0]-data[:,1], label = "diff", c = diff_color)
for i in range(24, 24*day_count, 24):
    plt.axvline(x = i, ls = ":", c = "k", lw = .5)
plt.xlim([-3, 24*day_count])
plt.xticks(range(12, 24*day_count,24), [f"Day {i+1}" for i in range(day_count)])
plt.ylabel("Step Counts")
plt.xlabel(f'''

Step counts Plot of P{id+1}: Day {day_start+1} ~ {day_end}''')
plt.legend()
plt.savefig("../Fig/006.png")