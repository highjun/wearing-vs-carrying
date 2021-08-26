import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
tmp = df.groupby(["user","both_chunk_idx","device"]).agg(step = ("step","sum")).unstack(level="device").fillna(0).droplevel(level=0, axis=1)

total_difference = np.abs(tmp.values[:,0] - tmp.values[:,1])
tmp = tmp.query("phone > 0  and watch > 0")
both_difference = np.abs(tmp.values[:,0]-tmp.values[:,1])

print(f"total_difference is {np.sum(total_difference)}, both_difference is {np.sum(both_difference)}, and ratio is {round(np.sum(both_difference)/np.sum(total_difference),3)}")
# total_difference is 2913243.0, both_difference is 889052.0, and ratio is 0.305