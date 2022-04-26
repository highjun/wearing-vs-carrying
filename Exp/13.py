from util import *
from scipy.stats import ks_2samp

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()
def get_min(x,y):
    if x*y >0:
        return min(x,y)
    elif x==0:
        return y
    elif y==0:
        return x

df['max'] = [ max(pstep,wstep) for pstep, wstep in  df[['pstep','wstep']].values]
df['min'] = [ get_min(pstep,wstep) for pstep, wstep in  df[['pstep','wstep']].values]
df['mean'] = df['step']

for btype in ['p','w']:
    each = df.query("btype == 'b' or btype == @btype")
    print(f"{btype} distribution are simular ")
    for way in ['min','max','mean']:
        stat, pVal = ks_2samp(each[stat],each[btype+'step'])
        print("{way}: p = {:.3f}, stat ={}".format(way, pVal, stat))
