from util import *

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]


nrows = 1
ncols = 4
fig, axes = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

metric = ["duration","distance","calorie","speed"]
for idx,ax in enumerate(axes.flatten()):
    ax.scatter(df["step"], df[metric[idx]], color = "tab:olive", s = 2)
    ax.set_ylabel(f'''{metric[idx]}''')
    ax.set_xlabel(r"$\rho$" + " = " + str(int(np.corrcoef(df[metric[idx]], df["step"])[0,1]*1000)/1000))
fig.supxlabel('''Step

Correlation between Step and other variable''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures",f"{cur}.png"))
