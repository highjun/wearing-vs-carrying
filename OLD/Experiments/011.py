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

#Interarrival 구하기
#10시부터 6시
tmp = data.query("watch_act_idx!=0 and device == 'watch'").groupby(["user","watch_act_idx"]).agg(start = ("timestamp","first"), end = ("timestamp","last"), hour = ("hour","first"))
tmp = tmp.query("hour > 9 and hour <= 18")
tmp = tmp.query("user == 1").values[1:,0]- tmp.query("user ==1").values[:-1, 1]
tmp = np.array([i.seconds//60 -2 for i in tmp])
print(plt.hist(tmp, bins = np.arange(60)+.5))
plt.xlim([-1, 60])
f = 0.5
plt.plot(np.arange(60)+1,np.exp(-f*np.arange(60))*50)
plt.savefig("../Figure/011.png")