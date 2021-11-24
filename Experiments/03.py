from util import *

df = load_bout()
df["duration"] = [(row["last"]-row["first"]).total_seconds()//60 for idx, row in df.iterrows()]

nrows = 1
ncols = 3
fig, axes = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

metric = ["duration","distance","calorie"]
for idx,ax in enumerate(axes.flatten()):
    ax.scatter(df[metric[idx]],df["step"], color = "tab:olive", s = 4)
    ax.set_ylabel("Step")
    ax.set_xlabel(f'''{metric[idx]}''')
    print(f'''{metric[idx]} & Step: {int(np.corrcoef(df[metric[idx]], df["step"])[0,1]*1000)/10}''')
fig.supxlabel('Correleation between Step and other variable')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures","03.png"))
