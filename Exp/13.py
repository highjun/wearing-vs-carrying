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

fig, axes= plt.subplots(nrows =2, ncols = 3, figsize = (3.2*3,3.2*2))
for btype in ['p','w']:
    both = df.query("btype == 'b' or btype ==@btype")
    mean_stat, mean_pVal = ks_2samp(both['step'],both[btype+'step'])
    max_stat, max_pVal = ks_2samp(both['max'],both[btype+'step'])
    min_stat, min_pVal = ks_2samp(both['min'],both[btype+'step'])
    
    print(btype)
    print("{},{:.3f}".format(mean_pVal, mean_stat), "{},{:.3f}".format(max_pVal, max_stat), "{},{:.3f}".format(min_pVal, min_stat))

    axs = axes[1 if btype =='p' else 0]
    lis = ['mean','max','min']
    for i in range(3):
        axs[i].scatter(np.sort(both[btype+'step']), np.sort(both[lis[i]]), s = 1)


plt.savefig(os.path.join(fig_dir, f"{cur}.png"))

# for btype in ['p','w']:
#     both = df.query("btype == @btype or btype == 'b'")
#     mean_lambda = 1/(np.mean(both['step']//50))
#     true_lambda = 1/(np.mean(both[btype+'step']//50))
#     max_lambda = 1/(np.mean(both['max']//50))
#     min_lambda = 1/(np.mean(both['min']//50))
#     print(btype)
#     print("{:.3f}".format(true_lambda), "{:.3f}".format(mean_lambda), "{:.3f}".format(max_lambda), "{:.3f}".format(min_lambda))
