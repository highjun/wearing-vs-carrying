from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2.5*ncols, 4.8 * nrows))

df.insert(1,'wearing',[1 if p<0.95 else 0 for p in df['date_wearing_ratio']])
df = df.query("wearing == 1")

data = getBoutRatio(df)
# print(data.head())
data = data.sort_index(level =0, key= lambda x: [users.index(user) for user in x.to_numpy()])
ax.bar(x= np.arange(n_user)*2.5+.5, height = 1- data['w'].to_numpy(), label = "phone", color = color["phone"])
ax.bar(x= np.arange(n_user)*2.5+1.5, height = 1- data['p'].to_numpy(), label = "watch", color = color["watch"])
ax.legend()
ax.set_xticks(np.arange(n_user)*2.5+1)
ax.set_xticklabels(len(users)*[''])
# ax.set_xticklabels(users, fontsize = 6, rotation= 45, ha="right", rotation_mode="anchor")
# ax.set_ylim([-.1,1.1])
ax.set_xlim([-1, n_user*2.5+1])
ax.set_ylabel("Covering Ratio")
data = data.to_numpy()
n_phone = np.sum(data[:,2] < 0.05)
n_watch = np.sum(data[:,1] < 0.05)
n_trust = np.sum((data[:,2] < 0.05)|(data[:,1] < 0.05))
fig.supxlabel(f'''Users

One device can measure more than 95% of steps in {n_trust}({round(n_trust/n_user*100,1)}%) people({n_phone}({round(n_phone/n_user*100,1)}%) by phone, {n_watch}({round(n_watch/n_user*100,1)}%) by watch).''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
