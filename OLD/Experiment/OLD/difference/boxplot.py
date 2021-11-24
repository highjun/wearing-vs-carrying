import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'Preprocess')
individuals = []
for csv in os.listdir(data_dir):
    data = pd.read_csv(os.path.join(data_dir,csv),index_col= 0, header = 0)
    day = data.groupby(['date','device']).sum()['step'].unstack(level = 1, fill_value = 0)
    zero_date = day.query('watch != 0').index
    grouping = data.query(f'date.isin(@zero_date)').query("weekday <5").groupby(['date','device']).sum()["step"]
    grouping = grouping.unstack(level = 1, fill_value=0)
    individuals.append([csv,np.array(grouping["phone"])-np.array(grouping["watch"])])
def custom_key(s):
    return np.median(s[1])
individuals =sorted(individuals, key = custom_key, reverse= True)
plt.subplots(nrows=1, ncols=1, constrained_layout = True)
plt.boxplot([ind[1] for ind in individuals])
plt.xticks(range(1,len(os.listdir(data_dir))+1), [int(os.path.splitext(ind[0])[0]) for ind in individuals])
plt.xlabel('''Each participants''')
plt.ylabel("Count")
plt.savefig(os.path.join(cwd,'Fig','diff_boxplot.png'))