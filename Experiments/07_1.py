from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 2, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(20, 8), sharey = True, sharex  =True)

datas = getWeekendRatio(users, df)
datas = [data.sort_index(level = 0, key=lambda x: [users.index(user) for user in x.to_numpy()]) for data in datas]

color = {"weekday":"tab:olive", "weekend":"tab:brown"}
for idx, btype in enumerate(["phone","watch"]):
    for jdx, weekday in enumerate(["weekday","weekend"]):
        ax[idx].bar(x=np.arange(n_user)*2.5 + .5 + jdx, height = datas[jdx][btype[0]].to_numpy() + datas[jdx]['b'].to_numpy(), label = weekday , color = color[weekday])
    ax[idx].set_ylabel(f"{btype} covering Ratio")
    ax[idx].set_xticks(np.arange(n_user)*2.5+1)
    ax[idx].set_xticklabels(users, rotation= 90, ha = 'center')

ax[0].legend(loc='upper left', bbox_to_anchor=(1, 1))
fig.supxlabel("User\n\nComparision of Covering Ratio between Weekend and Weekday")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

