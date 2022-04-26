from util import *
from sklearn.decomposition import LatentDirichletAllocation
from scipy.sparse import csr_matrix
import matplotlib as mpl
from colorsys import hls_to_rgb as hls2rgb

import pickle
from itertools import product
import os, shutil

df = loadDF()

df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
coverage = getBoutInfo(df, ['uid', 'date', 'weekday','30min'])

columns = []
for metric in ['step_ratio', 'step','count_ratio', 'count']:
    for btype in ['b','p','w']:
        columns.append(btype+metric)
columns.append('totalstep')
columns.append('totalcount')

ncolors = 13
color_match = [
    (0, hls2rgb(0,1,0)),
    (1/(ncolors-1), hls2rgb(120/360,80/100,57/100)),
    (2/(ncolors-1), hls2rgb(205/360,90/100,70/100)), 
    (3/(ncolors-1), hls2rgb(28/360,90/100,100/100)), 
    (4/(ncolors-1), hls2rgb(0/360,80/100,0/100)), 

    (5/(ncolors-1), hls2rgb(120/360,60/100,57/100)),
    (6/(ncolors-1), hls2rgb(205/360,70/100,70/100)), 
    (7/(ncolors-1), hls2rgb(28/360,70/100,100/100)), 
    (8/(ncolors-1), hls2rgb(0/360,40/100,0/100)),
    
    (9/(ncolors-1), hls2rgb(120/360,40/100,57/100)),
    (10/(ncolors-1), hls2rgb(205/360,50/100,70/100)), 
    (11/(ncolors-1), hls2rgb(28/360,50/100,100/100)), 
    (12/(ncolors-1), hls2rgb(0/360,0/100,0/100)),
    ]
descriptions = [
    "inactive", 
    *[" ".join([a,b]) for a, b in list(product(["small","middle","large"],["both","phone","watch","not-dominant"]))]]
cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', color_match, len(color_match))
patches = []
import matplotlib.patches as mpatches
for i in range(ncolors):
    patches.append(mpatches.Patch(color = color_match[i][1], label = descriptions[i]))

def get_color(row):
    # White
    if row[columns.index('totalstep')] ==0:
        return 0
    else:
        level = None
        if row[columns.index('totalstep')] < 50:
            level = 0
        elif row[columns.index('totalstep')] < 250:
            level =1
        else:
            level = 2
        if row[columns.index('bstep_ratio')] >.95:
            return level*4+ 1
        # Phone
        elif row[columns.index('pstep_ratio')] >.95:
            return level*4+ 2
        # Watch
        elif row[columns.index('wstep_ratio')] >.95:
            return level*4+ 3
        else:
            return level*4+ 4

coverage['color'] = [get_color(row) for row in coverage.values]
coverage_plot = coverage[['color']].unstack(level = 3, fill_value= 0)/(ncolors -1)
fig, ax = plt.subplots(nrows  = 1, ncols = 1, figsize = (9.6,3.2*100))
uids = list(coverage_plot.index.get_level_values(0))
prev, now =  None, 0
ticks = []
ticklabels = []
distincts= []
prev,idx = None, None
for idx, uid in enumerate(uids):
    if prev != uid:
        if len(distincts) > 0:
            ticks.append((idx + distincts[-1])/2)
            ticklabels.append(prev)
        distincts.append(idx)
        prev = uid
ax.hlines(distincts,xmin = 0, xmax = 48, colors = ['black']*len(distincts))
ticks.append((coverage_plot.shape[0] + ticks[-1]/2))
ticklabels.append(prev)
ax.set_yticks(ticks)
ax.set_yticklabels(ticklabels)


ax.set_xticks(np.arange(0,48+12, 12))
ax.set_xticklabels(np.arange(0,24+6, 6))
ax.pcolor(coverage_plot, cmap = cmap)
fig.legend(handles = patches, loc = 'upper center')
fig.supxlabel("24 Hour timeline divided into 30min")
fig.supylabel("Days")
plt.savefig(f"days.png")
plt.close()