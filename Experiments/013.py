import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


all = pd.read_excel("../Preprocess/all_user.xlsx")

tmp = all.groupby(["user","day","device"]).agg(step = ('step','sum'))
tmp = tmp.unstack(level= -1, fill_value= 0)
tmp.columns = ['phone','watch']

fig, ax = plt.subplots(nrows= 1, ncols=1 , constrained_layout = True)
plt.scatter(tmp.values[:,0], tmp.values[:,1], c =  list(tmp.index.get_level_values(0)))
plt.xlabel('''Phone Daily Step

Scatter Plot of each device's daily step, color means different users''')
plt.ylabel("Watch Daily Step")
plt.savefig("../Figure/013.png")