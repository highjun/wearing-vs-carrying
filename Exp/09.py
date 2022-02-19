from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(9.6*ncols, 4.8 * nrows))

df = loadDF()
def sum_arr(x):
    return np.ones_like(x) * np.sum(x)
daily= df.groupby(['uid','date']).agg(step = ('step','sum'), cnt = ('step','count'))
def getLevel(val):
    if val < 3000:
        return 0
    elif val < 6000:
        return 1
    elif val  < 9000:
        return 2
    else:
        return 3
levels = np.concatenate([np.ones(int(cnt))*getLevel(val) for val,cnt in daily[['step','cnt']].to_numpy()],axis = 0).reshape(-1)
df['level'] = levels

comparingGroup(df,'level','date', ax)
ax.set_xlabel('Comparing Bout ratio of Daily Step Level')
ax.set_ylabel('Ratio')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))
