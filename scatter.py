import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd
import numpy as np
import os

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'Preprocess')
n_day = 0
points = [[],[]]
for csv in os.listdir(data_dir):
    data = pd.read_csv(os.path.join(data_dir,csv),index_col= 0, header = 0, encoding = 'utf-8')
    n_day = n_day+ len(set(np.array(data["date"])))
    grouping = data.query("weekday <5").groupby(['date','device']).sum()["step"]
    grouping = grouping.unstack(level = 1, fill_value=0)
    points[0] += list(grouping["phone"])
    points[1] += list(grouping["watch"])
print(st.wilcoxon(points[0], points[1]))
# print(np.sum(np.array(points[1]) == 0))
print(n_day)
plt.subplots(nrows=1, ncols=1, constrained_layout = True)
plt.scatter(points[0], points[1], s= 4)
plt.xlabel('''Phone''')
plt.ylabel("Watch")
plt.savefig("Fig/comparison.png")