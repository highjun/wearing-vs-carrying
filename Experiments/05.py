# 참가자 별로 얼마나 큰 차이가 날 수 있는지 보자.
from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = list(set(df['users']))
n_user = len(users)

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2.5*ncols, 4.8 * nrows))


data = getBoutRatio(df, normalize=True)
data= data.sort_values(by='b', ascending = False).to_numpy()

ax.bar(x= np.arange(n_user)*2.5 + .5, height = 1-data[:,2], label = "phone", color = color["phone"])
ax.bar(x= np.arange(n_user)*2.5 + 1.5, height = 1-data[:,1], label = "watch", color = color["watch"])
ax.legend()
ax.set_xticks(np.arange(n_user)*2.5 + 1)
ax.set_xticklabels(n_user*[''])

# ax.set_xticklabels(users, fontsize = 6, rotation= 45, ha="right", rotation_mode="anchor")
ax.set_ylim([0,1])
ax.set_xlim([-1, n_user*2.5+1])
ax.set_ylabel("Ratio")
data = np.array(data)
n_phone = np.sum(data[:,2] < 0.05)
n_watch = np.sum(data[:,1] < 0.05)
ar1 = data[:,2] < 0.05
ar2 = data[:,1] < 0.05
n_trust = np.sum(ar1 | ar2)
fig.supxlabel(f'''Users

One device can measure more than 95% of steps in {n_trust}({round(n_trust/n_user*100,1)}%) people({n_phone}({round(n_phone/n_user*100,1)}%) by phone, {n_watch}({round(n_watch/n_user*100,1)}%) by watch).
''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

