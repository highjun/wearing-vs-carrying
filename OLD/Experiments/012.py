#Clustering Analysis for Probability Vector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

all = pd.read_excel("../Preprocess/all_user.xlsx")

def from_what(x):
    x= x.values
    if len(x) == 2:
        return 'both'
    elif len(x) == 1:
        return x[0]
tmp = all.groupby(["user","timestamp"]).agg(cnt = ('device',from_what))
tmp = tmp.groupby("user").agg(phone= ('cnt', lambda x: np.sum(x == 'phone')/len(x)), watch = ('cnt', lambda x: np.sum(x == 'watch')/len(x)), both = ('cnt', lambda x: np.sum(x == 'both')/len(x)))

fig, ax = plt.subplots(nrows = 1, ncols = 1, constrained_layout = True, figsize = (6,6))
plt.scatter(tmp.values[:,0], tmp.values[:,1])
plt.xlabel('''Only phone ratio

Scatter Plot using probability vector of detected device for each user''')
plt.ylabel("Only watch ratio")
plt.savefig("../Figure/012.png")