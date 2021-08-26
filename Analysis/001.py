import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster

phone_color = "#ff7f0e"
watch_color = "#1f77b4"
diff_color = "#7f7f7f"
df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
survey = pd.read_excel("../survey_result.xlsx")

#Scatter Plot of Different Scale
minute_level = df.groupby(["user","timestamp","device"]).agg(step = ("step","sum")).unstack(level= "device").droplevel(level = 0, axis = 1).fillna(0)
activity_level = df.groupby(["user","both_chunk_idx","device"]).agg(step = ("step","sum")).unstack(level= "device").droplevel(level = 0, axis = 1).fillna(0)
hour_level = df.groupby(["user","day","hour","device"]).agg(step = ("step","sum")).unstack(level= "device").droplevel(level = 0, axis = 1).fillna(0)
day_level = df.groupby(["user","day","device"]).agg(step = ("step","sum")).unstack(level= "device").droplevel(level = 0, axis = 1).fillna(0)
fig, axs = plt.subplots(nrows = 1, ncols = 4, figsize= (12,4), constrained_layout = True)
axs[0].scatter(day_level.values[:,0],day_level.values[:,1], s= .5)
axs[0].plot([0,25000], [0,25000], color = 'r', lw = .5)
axs[1].scatter(hour_level.values[:,0],hour_level.values[:,1], s= .5)
axs[1].plot([0,8000], [0,8000], color = 'r', lw = .5)
axs[2].scatter(activity_level.values[:,0],activity_level.values[:,1], s= .5)
axs[2].plot([0,25000], [0,25000], color = 'r', lw = .5)
axs[3].scatter(minute_level.values[:,0],minute_level.values[:,1], s= .5)
axs[3].plot([0,250], [0,250], color = 'r', lw = .5)

fig.supylabel("Watch Step Count")
fig.supxlabel('''Phone Step Count

Figure shows the scatter plot between phone and watch step count for Day, Hour, Chunk, Minute Level''')
fig.show()
plt.savefig("../Fig/001.png")