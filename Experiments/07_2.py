from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 1, 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*ncols, 4.8 * nrows), sharex  =True, sharey = True)

datas = getWeekendRatio(users, df)
datas = [data.sort_index(level = 0, key=lambda x: [users.index(user) for user in x.to_numpy()]) for data in datas]

for idx, btype in enumerate(["phone","watch"]):
    ax[idx].scatter(datas[0]['b'].to_numpy() + datas[0][btype[0]].to_numpy(),
    datas[1]['b'].to_numpy() + datas[1][btype[0]].to_numpy(), s= 4, color = "tab:olive")
    ax[idx].set_xlabel(f"{btype} Covering Ratio for Weekday")
    ax[idx].set_ylabel(f"{btype} Covering Ratio for Weekend")
fig.supxlabel("Scatter Plot between Weekday/Weekend Covering Ratio")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

