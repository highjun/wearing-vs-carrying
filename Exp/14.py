from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()
df = df.query("weekday < 5")

boutdf = getBoutInfo(df, ['uid','date'])
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (15, 4.8))
boutdf = boutdf.reset_index()
boxplots = []
users = set(boutdf['uid'])
def sortbyIQR(uid):
    x = boutdf.query('uid == @uid')['bstep_ratio'].to_numpy()
    q1, q3= np.percentile(x, [25, 75])
    return q3-q1
users = sorted(users,key= lambda uid: sortbyIQR(uid))
for uid in users:
    x = boutdf.query('uid == @uid')['bstep_ratio'].to_numpy()
    print(uid, sortbyIQR(uid))
    boxplots.append(x)
ax.boxplot(boxplots, labels= users)
ax.set_xticklabels(users, rotation =45, ha='center', fontsize= 7)
ax.set_xlabel('Participants')
ax.set_ylabel('Ratio')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))