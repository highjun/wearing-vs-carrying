import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json
import os

pd.set_option("precision",2)
pd.set_option("expand_frame_repr", False)
pd.set_option("max_columns", 20)
np.printoptions(precision=2, suppress=True)

tmp_hour = pd.read_excel("../tmp_hour.xlsx")
tmp = tmp_hour.groupby("hour").agg(phone=("p_act","sum"), watch = ("w_act","sum"), both = ("b_act","sum"))
fig, ax = plt.subplots(nrows = 1, ncols = 1, constrained_layout = True)
plt.plot(range(24), tmp.values[:,0]/(tmp.values[:,0]+tmp.values[:,2]),label = "phone")
plt.plot(range(24), tmp.values[:,1]/(tmp.values[:,1]+tmp.values[:,2]),label = "watch")
# plt.plot(range(24), tmp.values[:,2],label = "both")
for i in [6,12,18]:
    plt.axvline(x = i, ls = "--", c='k')
plt.xticks(range(24), [str(i).zfill(2) for i in range(24)])
plt.legend()
plt.xlabel('''Time(Hour)

Ratio of single device detected on each hour''')
plt.ylabel('''single-detected ratio''')
plt.savefig("../Figure/019.png")