# 참가자 별로 얼마나 큰 차이가 날 수 있는지 보자.
from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

# nrows = 2
nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2*ncols, 4.8 * nrows))

is_normalized = False

data = getBoutRatio(df, normalize=is_normalized)
data = data.sort_index(level = 0, key = lambda x: [users.index(user) for user in x])

if not is_normalized:
    n_date = df.groupby(["uid","date"]).agg(tmp =("step","count"))
    n_date = n_date.reset_index().groupby(["uid"]).agg(ndate = ("date","count"))
    n_date = n_date.sort_index(level = 0, key = lambda x: [users.index(user) for user in x])
    data/= n_date.to_numpy()    

bottom = np.zeros(n_user)
for btype in ['both','phone','watch']:
    ax.bar(x = np.arange(n_user)+.4, height = data[btype[0]],bottom = bottom, label = btype, color = color[btype])
    bottom += data[btype[0]].to_numpy()
ax.set_xticks(np.arange(n_user)+.5)
ax.set_xticklabels(["P" + str(user).zfill(2) for user in users], rotation =90, ha='center', fontsize= 8)
ax.legend()

threshold = .95
n_trust = [0,0]
data = getBoutRatio(df, normalize=True)
statement = '''Users\n\n'''
for idx, btype in enumerate(['phone','watch']):
    n_trust[idx] = np.sum((data[btype[0]].to_numpy() + data['b'].to_numpy() ) > .95)
    statement += f"{btype} is coverable for {btype}: {n_trust[idx]}({round(n_trust[idx]/n_user*100,1)}%)" 
n_coverable = np.sum(((data['p'].to_numpy() + data['b'].to_numpy() ) > .95) | ((data['w'].to_numpy() + data['b'].to_numpy() ) > .95))
statement += f"\n total {n_coverable}({round(n_coverable/n_user*100,1)}%)"
fig.supxlabel(statement)

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))



# total = data.sum(axis = 1)

# data = data.to_numpy()
# data/= 10000
# datacum = data.cumsum(axis = 1)
# ax[0].bar(x= np.arange(n_user)+.5, height = data[:,0], label = 'both', color = color['both'])
# ax[0].bar(x= np.arange(n_user)+.5, height = data[:,1], bottom = datacum[:,0], label = 'phone', color = color['phone'])
# ax[0].bar(x= np.arange( n_user)+.5 , height = data[:,2], bottom = datacum[:,1], label = 'watch', color = color['watch'])
# ax[0].set_xticks(np.arange(n_user)+.5)
# ax[0].set_xticklabels(['']*n_user)
# ax[0].set_ylabel("Frequency(x10000)")
# ax[0].legend()

# data = np.array([row/np.sum(row) for row in data])
# datacum = data.cumsum(axis = 1)
# ax[1].bar(x= np.arange(n_user)+.5, height = data[:, 0], label = 'both', color = color['both'])
# ax[1].bar(x= np.arange(n_user)+.5, height = data[:, 1], bottom = datacum[:,0], label = 'phone', color = color['phone'])
# ax[1].bar(x= np.arange(n_user)+.5 , height = data[:, 2], bottom = datacum[:,1], label = 'watch', color = color['watch'])
# ax[1].set_xticks(np.arange(n_user)+.5)
# # ax[1].set_xticklabels(['']*n_user)
# ax[1].set_xticklabels(users, rotation =45, ha='right', fontsize= 8)
# ax[1].set_ylabel("Ratio")
