
from util import *

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]

nrows, ncols  = 6, 3
fig, axes = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 5.5*nrows), sharex= 'row', sharey= 'row')
for idx, metric in enumerate(["duration","dist","cal","speed",'run','walk']):
    for jdx, btype in enumerate(["both","phone","watch"]):
        tmp = df.query(f"btype == '{btype[0]}'")
        axes[idx][jdx].scatter(tmp["step"], tmp[metric], color = color[btype], label=btype, s = 1)
        if jdx == 0:
            axes[idx][0].set_ylabel(metric)
        axes[idx][jdx].set_xlabel(btype)
fig.supxlabel('''Bout Level Step Count and Additional Info Scatter Plot''')
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures",f"{cur}.png"))