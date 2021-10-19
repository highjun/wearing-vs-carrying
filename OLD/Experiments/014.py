import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

all = pd.read_excel("../Preprocess/all_user.xlsx")

tmp = all.groupby(["user","day","hour","device"]).agg(step = ('step','sum'))
tmp = tmp.unstack(level= -1, fill_value= 0)
tmp.columns = ['phone','watch']

fig, ax = plt.subplots(nrows = 1, ncols= 1, constrained_layout = True)
plt.scatter(tmp.values[:,0], tmp.values[:,1], c =  list(tmp.index.get_level_values(0)))
plt.xlabel('''Phone Hourly Step

Scatter Plot of each device's Hourly step, color means different users''')
plt.ylabel("Watch Hourly Step")
plt.savefig("../Figure/014.png")