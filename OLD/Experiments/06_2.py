from util import *

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]
users = getSortedUser(df)
df = filterWearingDate(df)

start = 0
end = 1000
bsize = 50

nrows, ncols = 2, 1
# nrows, ncols = 1, 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

total, _ = np.histogram(df['step'], bins = np.arange(start//bsize, end//bsize + 1)*bsize)
for i in range(2):
    bottom = np.zeros((end-start)//bsize)
    for idx, btype in enumerate(["both","phone","watch"]):
        tmp = df.query(f"btype == '{btype[0]}'")
        hist, _ = np.histogram(tmp['step'], bins = np.arange(start//bsize, end//bsize + 1)*bsize)
        if i == 1:
            hist = hist / total
        ax[i].bar(x = np.arange((end-start)//bsize)+.5, height = hist, bottom = bottom, label = btype, color = color[btype])
        bottom += hist
    ax[i].set_xticks(np.arange((end-start)//bsize + 1))
    ax[i].set_xticklabels(np.arange(start, end + bsize, bsize), fontsize = 7)
    ax[i].set_xlabel("Step count")
    ax[i].set_ylabel("Frequency" if i == 0 else "Ratio")
    ax[i].legend()

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
