from util import *

df = load_bout()
df["duration"] = [(row["last"]-row["first"]).total_seconds()//60 for idx, row in df.iterrows()]

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

ax.scatter(df["step"],df["speed"], color = "tab:olive", s = 4)
ax.set_xlabel("Step")
ax.set_ylabel(f'''Speed''')
print(f'''{"speed"} & Step: {int(np.corrcoef(df["speed"], df["step"])[0,1]*1000)/10}''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures","14.png"))
