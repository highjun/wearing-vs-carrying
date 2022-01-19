# 참가자 별로 얼마나 큰 차이가 날 수 있는지 보자.
from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2.5*ncols, 4.8 * nrows))


data = getBoutRatio(df, normalize=True)
data= data.sort_values(by='b', ascending = False)

for idx, btype in enumerate(["phone","watch"]):
    ax.bar(x= np.arange(n_user)*2.5 + .5 + idx, height = data[btype[0]].to_numpy() + data['b'].to_numpy(), label = btype, color = color[btype])
ax.hlines(y = .95, xmin = 0 , xmax = n_user*2.5, color = "red")
ax.legend()
ax.set_xticks(np.arange(n_user)*2.5 + 1)
ax.set_xticklabels(users, fontsize = 6, rotation= 45, ha="right", rotation_mode="anchor")
ax.set_ylabel("Covering Ratio")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

