import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd
import numpy as np
import os

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'Preprocess')
n_day = 0
phones = np.zeros(24)
watches = np.zeros(24)
# diffs = [[] for _ in range(24)]
for csv in os.listdir(data_dir):
    data = pd.read_csv(os.path.join(data_dir,csv),index_col= 0, header = 0, encoding = 'utf-8')
    n_day = n_day+ len(set(np.array(data["date"])))
    grouping = data.query("weekday <5").groupby(['hour','device']).sum()
    grouping = grouping.reindex(pd.MultiIndex.from_product([list(range(24)), ['phone','watch']]), fill_value = 0)
    grouping.reset_index(inplace = True)
    phones += np.array(grouping.query("level_2 == 'phone'")["step"])
    watches += np.array(grouping.query("level_2 == 'watch'")["step"])
    # grouping = data.query("weekday <5").groupby(['date','hour','device']).sum()
    # grouping = grouping.reindex(pd.MultiIndex.from_product([list(set(np.array(data.query('weekday<5')['date']))),list(range(24)), ['phone','watch']]), fill_value = 0)
    # grouping.reset_index(inplace = True)
    # print(grouping)
    # for idx in range(24):
    #     phones = np.array(grouping.query(f"level_2 == 'phone' and level_1 == {idx}")["step"])
    #     watches = np.array(grouping.query(f"level_2 == 'watch' and level_1 == {idx}")["step"])
    #     for i in range(len(phones)):
    #         diffs[idx].append(phones[i] - watches[i])
phones /= n_day
watches /= n_day
print(np.sum(np.array(points[1]) == 0))
print(n_day)
plt.subplots(nrows=1, ncols=1, constrained_layout = True)
plt.plot(phones, label='phone')
plt.plot(watches, label='watch')
plt.legend()
plt.xticks(list(range(0,24,6)))
plt.xlabel('''Hour''')
plt.ylabel("Avg Step Count")
plt.savefig("Fig/time_plot.png")

# plt.subplots(nrows=1, ncols=1, constrained_layout = True)
# plt.boxplot(diffs)
# plt.xticks(list(range(1,25,6)), list(range(0,24,6)))
# plt.xlabel('''Hour''')
# plt.ylabel("Step Count difference")
# plt.savefig("Fig/time_boxplot.png")