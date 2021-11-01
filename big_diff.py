import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'Preprocess')
n_day = 0
point = [[],[],[],[],[]]
fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout = True)
for csv in os.listdir(data_dir):
    if int(os.path.splitext(csv)[0]) not in [3,4,10,11,12,14,24,29, 26]:
        data = pd.read_csv(os.path.join(data_dir,csv),index_col= 0, header = 0)
        day = data.groupby(['date','device']).sum()['step'].unstack(level = 1, fill_value = 0)
        zero_date = day.query('watch != 0').index
        grouping = data.query(f'date.isin(@zero_date)').groupby(['date','weekday', 'hour','device']).sum()["step"]
        grouping = grouping.unstack(level = 3, fill_value=0)
        point[0]+= list(grouping["phone"])
        point[1] += list(grouping["watch"])
        #individual
        point[2] += [int(os.path.splitext(csv)[0])] * len(list(grouping["phone"]))
        #weekday
        point[3] += list(grouping.index.get_level_values(1))
        #hour
        point[4] += list(grouping.index.get_level_values(2))
point = np.array(list(zip(*point)))
print(point.shape)
point = pd.DataFrame(point, columns=['phone','watch','participant','weekday','hour'])
point['diff'] = diff = np.abs(np.array(point["phone"])-np.array(point['watch']))
point['sum'] = sum_ = (np.array(point["phone"])+ np.array(point['watch']))/2
point['ratio'] = [diff[idx]/sum_[idx] if sum_[idx]>100 else pd.NA for idx in range(len(diff))]
point.sort_values('diff', ascending= False,inplace= True)
big_diff = point.query('ratio > .5')
#big_diff의 participant 분포
# ax[0].hist(big_diff['participant'],bins = list(range(33)), label="participant")
#big_diff의 시간 분포
# pariticpant_no = 2
# ax[1].hist(big_diff.query(f'participant == {pariticpant_no}')['hour'],bins = list(range(25)), label="hour")
# ax[1].set_xlabel(f'participant: {pariticpant_no}')
# ax[1].set_xticks(list(np.arange(.5, 24,6)))
# ax[1].set_xticklabels(list(np.arange(0,24,6)))
# pariticpant_no = 30
ax.hist(big_diff.query(f'diff > 500')['hour'],bins = list(range(25)), label="hour")
ax.set_xlabel(f'histogram for difference more than 500')
ax.set_xticks(list(np.arange(.5, 24,6)))
ax.set_xticklabels(list(np.arange(0,24,6)))
plt.savefig('Fig/big_diff.png')
print(f"{'-'*40}")
# print(point)
print(f"{'-'*40}")
print(point.query('diff > 500'))