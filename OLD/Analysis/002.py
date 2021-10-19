import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)
daily_step = df.groupby(["user","day","device"]).agg(step = ("step","sum")).unstack(level="device").droplevel(level = 0, axis =1).fillna(0).values

diff = daily_step[:,0] - daily_step[:,1]
step = (diff.max()-diff.min())//20
hist, _ = np.histogram(diff, bins = np.arange(diff.min(), diff.max()+step, step))
# print(np.arange(diff.min(), diff.max()+step, step))
# plt.plot(np.arange(-1 + step/2, 1, step), hist)
xnew = np.linspace(diff.min(), diff.max(), 300) 

fig, ax = plt.subplots(nrows=2, ncols = 1,figsize = (6,6.5), gridspec_kw={'height_ratios': [4, 1]},sharex = True, constrained_layout = True)
spl = make_interp_spline(np.arange(diff.min() + step//2, diff.max()+step, step), hist, k=3)  # type: BSpline
power_smooth = spl(xnew)
ax[0].plot(xnew, power_smooth)

ax[0].vlines(x = 0, lw=.5, ymin =-30, ymax = power_smooth[xnew >0][0], color= "r")
ax[0].set_ylim([-30,520])
ax[1].boxplot(diff, vert=False, showfliers = False)
ax[1].set_yticks([])
fig.supxlabel('''Difference(P-W)

Distribution of Daily Step Difference and boxplot''')
fig.supylabel("Density")

plt.savefig("../Fig/002.png")

q25 =np.quantile(diff, 0.25)
q75 =np.quantile(diff, 0.75)
print(f"25% quantile is {q25}, 75% quantile is {q75}")
# 25% quantile is -1017.0, 75% quantile is 785.0