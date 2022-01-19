from util import *

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]

nrows = 2
ncols = 3
fig, axes = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

for idx, metric in enumerate(["duration","dist","cal","speed",'run','walk']):
    axes[idx%2][idx//2].scatter(df['step'],df[metric], color = "tab:olive", s = 1)
    axes[idx%2][idx//2].set_ylabel(metric)
    axes[idx%2][idx//2].set_xlabel("step\n" + r"$\rho$" + f" = {round(np.corrcoef(df[metric],df['step'])[0,1],3)}")
fig.supxlabel("Scatter Plot between step and Additional Info")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures",f"{cur}.png"))
