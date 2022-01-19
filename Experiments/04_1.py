from util import *
df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]
users = getSortedUser(df)

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows), sharex = True, sharey = True)

start = 0
end = 1000
bsize = 50
for idx, btype in enumerate(["both","phone","watch"]):
    tmp = df.query(f"btype=='{btype[0]}'")
    hist, _ = np.histogram(tmp['step'], bins = np.arange(start//bsize, end//bsize + 1)*bsize)
    hist = hist/np.sum(hist)
    plt.plot((np.arange(start//bsize, end//bsize)+.5)*bsize, hist, label = btype, color = color[btype])

plt.legend()
ax.set_ylabel("Prob")
ax.set_xlabel("Step\n\nPlot of Distribution over step count")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
