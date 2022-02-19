from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2.5*ncols, 4.8 * nrows))

df = filterWearingDate(df)
data = getBoutRatio(df)
data = data.sort_index(level =0, key= lambda x: [users.index(user) for user in x.to_numpy()])

for idx, btype in enumerate(["phone","watch"]):
    ax.bar(x = np.arange(n_user)*2.5+.5+idx, height = data[btype[0]].to_numpy()+ data['b'].to_numpy(), label = btype, color = color[btype])

ax.legend()
ax.set_xticks(np.arange(n_user)*2.5+1)
ax.set_xticklabels(users, fontsize = 6, rotation= 45, ha="right", rotation_mode="anchor")
ax.set_ylabel("Covering Ratio")
threshold = .95
supxlabel = "Users"
for idx, btype in enumerate(["phone","watch"]):
    n_coverable = np.sum((data[btype[0]].to_numpy() + data['b'].to_numpy()) > threshold)
    supxlabel += f"{btype} is coverable for {n_coverable}({round(n_coverable/n_user*100,1)}%), "
n_coverable = np.sum((data['w'].to_numpy() < 1-threshold)|(data['p'].to_numpy() < 1-threshold))
supxlabel +=f"total {n_coverable}({round(n_coverable/n_user*100,1)}%) are coverable"
fig.supxlabel(supxlabel)

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
