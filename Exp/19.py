from util import *

pd.options.display.float_format = "{:,.2f}".format

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()


total  = np.sum(np.abs(df['pstep'] - df['wstep']))
phone = np.sum(df.query("btype == 'p'")['pstep'])
watch = np.sum(df.query("btype == 'w'")['wstep'])
both = np.sum(np.abs(df.query("btype=='b'")['pstep'] - df.query("btype=='b'")['wstep']))

boutdf = getBoutInfo(df, ['uid','date'])

fig, ax = plt.subplots(nrows = 1, ncols = 1)
ax.scatter(boutdf['pstep_ratio'],boutdf['wstep_ratio'], s=2 )
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))