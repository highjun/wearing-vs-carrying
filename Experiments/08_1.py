from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 2, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2.5*ncols, 4.8 * nrows))

day, night = getDayNightRatio(users, df)
day = day.sort_index(level= 0, key=lambda x:[users.index(user) for user in x.to_numpy()] )
night = night.sort_index(level= 0, key=lambda x:[users.index(user) for user in x.to_numpy()] )

for idx, label in enumerate(["Phone","Watch"]):
    ax[idx].bar(x= np.arange(n_user)*2.5+.5, height = 1-day['w' if idx == 0 else 'p'].to_numpy(), label = "day", color = "tab:olive")
    ax[idx].bar(x= np.arange(n_user)*2.5+ 1.5, height = 1-night['w' if idx == 0 else 'p'].to_numpy(), label = "night", color = "tab:brown")
    ax[idx].set_xlabel(label)
    ax[idx].set_xlim([-1, n_user*2.5+1])
    ax[idx].set_ylim([0,1])
    ax[idx].set_xticks(np.arange(n_user)*2.5+1)
    ax[idx].set_xticklabels(['']*n_user)
    # ax[idx].set_xticklabels(users, fontsize = 6, rotation= 45, ha="right", rotation_mode="anchor")

ax[0].legend()
fig.supylabel("Covering Ratio")
w_strong_end = np.sum((day['p'].to_numpy() - night['p'].to_numpy()) > .1)
w_week_end = np.sum((day['p'].to_numpy() - night['p'].to_numpy()) < -.1)
p_strong_end = np.sum((day['w'].to_numpy() - night['w'].to_numpy()) > .1)
p_week_end = np.sum((day['w'].to_numpy() - night['w'].to_numpy()) < -.1)


fig.supxlabel(f'''Covering Ratio Change
Watch night > day: {w_strong_end}, opposite: {w_week_end}
Phone night > day: {p_strong_end}, opposite: {p_week_end}
''')


plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

