from util import *

pd.options.display.float_format = "{:,.2f}".format

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()


total  = np.sum(np.abs(df['pstep'] - df['wstep']))
phone = np.sum(df.query("btype == 'p'")['pstep'])
watch = np.sum(df.query("btype == 'w'")['wstep'])
both = np.sum(np.abs(df.query("btype=='b'")['pstep'] - df.query("btype=='b'")['wstep']))

# Exclude Single Device Day
threshold = .95
boutdf = getBoutInfo(df, ['uid','date'])
total_day = boutdf.shape[0]
notsingle = boutdf.query("not (pstep_ratio > @threshold or wstep_ratio > @threshold)")
tmp = df.reset_index().set_index(['uid','date'])
mask = tmp.index.isin(notsingle.index)
df = tmp.loc[mask]
df = df.reset_index()

threshold = .95
boutdf = getBoutInfo(df, ['uid','date','hour'])
boutdf = boutdf.query("wstep_ratio > @threshold or pstep_ratio > @threshold")
boutdf = boutdf.reset_index()

fig, ax = plt.subplots(nrows = 1, ncols = 1)
ax.bar(x = np.arange(24), height = boutdf.query("pstep_ratio > @threshold").groupby('hour').count()['date'].values/total_day, label = 'phone', color = color['phone'], alpha = .5)
ax.bar(x = np.arange(24), height = boutdf.query("wstep_ratio > @threshold").groupby('hour').count()['date'].values/total_day,label = "watch", color = color['watch'], alpha = .5)
ax.set_xticks(np.arange(24))
ax.set_xticklabels([str(i).zfill(2) for i in range(24)], rotation = 45, ha = 'center')
ax.set_xlabel("Timeslot")
ax.set_ylabel("Ratio of Day")
ax.set_ylim([0,.5])
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))