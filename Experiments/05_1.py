# 참가자 별로 얼마나 큰 차이가 날 수 있는지 보자.
from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = set(df["users"])
n_user = len(users)

nrows = 2
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*2*ncols, 4.8 * nrows))


data = getBoutRatio(df, normalize=False)
total = data.sum(axis = 1)
data= data.sort_values(by='b', ascending = False, key= lambda x: data['b']/total)
data = data.to_numpy()
data/= 10000
datacum = data.cumsum(axis = 1)
ax[0].bar(x= np.arange(n_user)+.5, height = data[:,0], label = 'both', color = color['both'])
ax[0].bar(x= np.arange(n_user)+.5, height = data[:,1], bottom = datacum[:,0], label = 'phone', color = color['phone'])
ax[0].bar(x= np.arange( n_user)+.5 , height = data[:,2], bottom = datacum[:,1], label = 'watch', color = color['watch'])
ax[0].set_xticks(np.arange(n_user)+.5)
ax[0].set_xticklabels(['']*n_user)
ax[0].set_ylabel("Frequency(x10000)")
ax[0].legend()

data = np.array([row/np.sum(row) for row in data])
datacum = data.cumsum(axis = 1)
ax[1].bar(x= np.arange(n_user)+.5, height = data[:, 0], label = 'both', color = color['both'])
ax[1].bar(x= np.arange(n_user)+.5, height = data[:, 1], bottom = datacum[:,0], label = 'phone', color = color['phone'])
ax[1].bar(x= np.arange(n_user)+.5 , height = data[:, 2], bottom = datacum[:,1], label = 'watch', color = color['watch'])
ax[1].set_xticks(np.arange(n_user)+.5)
ax[1].set_xticklabels(['']*n_user)
ax[1].set_ylabel("Ratio")

n_phone = np.sum(data[:,2]< 0.05)
n_watch = np.sum(data[:,1]< 0.05)
ar1 = data[:,2] < 0.05
ar2 = data[:,1] < 0.05
n_trust = np.sum(ar1 | ar2)
fig.supxlabel(f'''Users

One device can measure more than 95% of steps in {n_trust}({round(n_trust/n_user*100,1)}%) people({n_phone}({round(n_phone/n_user*100,1)}%) by phone, {n_watch}({round(n_watch/n_user*100,1)}%) by watch).
''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))