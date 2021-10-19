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
# plt.hist(tmp_hour.query('p_step>0')['weekday'],bins = np.arange(-0.5, 7.5, 1))
# plt.xticks(range(7),['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize= (5,5), constrained_layout = True)
hist, bin_edges= np.histogram(tmp_hour.query('p_step>0')['weekday'],bins = np.arange(-0.5, 7.5, 1))
plt.plot(range(7), hist, label = "phone")
hist, bin_edges= np.histogram(tmp_hour.query('w_step>0')['weekday'],bins = np.arange(-0.5, 7.5, 1))
plt.plot(range(7), hist, label = "watch")
plt.xticks(range(7),['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
plt.legend()
plt.ylabel("Numbers")
plt.xlabel('''Time(Day of Week)

Single device detected numbers on each day of week''')
plt.savefig("../Figure/017.png")