from util import *
cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()
users = list(set(df['uid']))

nrows, ncols = 2, 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (9, 4.8*nrows))

start, end, bsize = 0, 1000, 50
n_level = (end-start)//bsize
def getLevel(step):
    level = (step-start)//bsize
    if level >= n_level:
        return n_level
    return level
df['level'] = [getLevel(step) for step in df['step'].to_numpy()]
df = df.query('level < @n_level')
df = getBoutInfo(df, ['level'])
for i in range(n_level):
    print(f"Level {str(i).zfill(2)}")
    for btype in ['b','p','w']:
        print("# of {}: {:.2f}".format(btype, df.loc[i][btype+'weight']))
total = df['totalcount'].to_numpy()
bottom = np.zeros((end - start)//bsize)
for idx, btype in enumerate(['both','phone','watch']):
    ax[0].bar(bottom = bottom, height = df[btype[0]+'count'],x= np.arange((end-start)//bsize)+.5, label = btype, color = color[btype])
    ax[1].bar(bottom = bottom/total, height = df[btype[0]+'count']/total,x= np.arange((end-start)//bsize)+.5, label = btype, color = color[btype])
    bottom +=  df[btype[0]+'count']
for i in range(2):
    ax[i].set_xticks(np.arange((end-start)//bsize + 1))
    ax[i].set_xticklabels(np.arange(start, end + bsize, bsize), fontsize = 7)
    ax[i].set_xlabel("Step count")
    ax[i].legend()
    ax[i].set_ylabel("Frequency" if i == 0 else 'Ratio')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))
