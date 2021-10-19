import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
import json

phone_color = "#ff7f0e"
watch_color = "#1f77b4"
diff_color = "#7f7f7f"
df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
step_count = df.groupby(["user","day","weekday","device"]).agg(step = ("step","sum")).unstack(level = "device").droplevel(level = 0, axis = 1).fillna(0)
step_count = step_count.reset_index(level = ["user","weekday", "day"])
step_count["week"] = [row["day"]//7 + (1 if row["day"]%7 - row["weekday"] > 0 else 0) for idx,row in step_count.iterrows()]
with open("../meta_data.json")as f:
    j = json.load(f)
users = []
for val in j.values():
    users.append(val['folder'])
id = 0
week_start = 0
week_end = 5
week_count = week_end - week_start
data = step_count.query(f"user == '{users[id]}' and week >= {week_start} and week < {week_end}")
print(data.shape)
data = data.set_index(["week", "weekday"])
data = data.reindex(pd.MultiIndex.from_product([range(week_start,week_end), range(7)])).fillna(0).values

plt.subplots(nrows = 1,ncols = 1, figsize = (6,4), constrained_layout = True)
plt.plot(range(7*week_count), data[:,2], label = "phone", c = phone_color)
plt.plot(range(7*week_count), data[:,3], label = "watch", c = watch_color)
plt.plot(range(7*week_count), data[:,2]-data[:,3], label = "diff", c = diff_color)
for i in range(7, 7*week_count, 7):
    plt.axvline(x = i, ls = ":", c = "k", lw = .5)
plt.xlim([-3, 7*week_count])
plt.xticks(np.arange(3.5, 7*week_count,7), [f"week {i+1}" for i in range(week_count)])
plt.ylabel("Step Counts")
plt.xlabel(f'''

Step counts Plot of P{id+1}: Week {week_start+1} ~ {week_end}''')
plt.legend()
plt.savefig("../Fig/007.png")