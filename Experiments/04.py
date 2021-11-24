# 참가자 별로 얼마나 큰 차이가 날 수 있는지 보자.
from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = sorted(list(set(df['users'])))
def diff_ratio(user):
    both = np.sum(df.query(f"users == '{user}' and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == '{user}' and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == '{user}' and bout_type=='p'")["step"])
    ratio = (watch - phone)/(both+watch+phone)
    return ratio
# sorted_idx = sorted(range(len(users)), key=lambda k: diff_ratio(users[k]))
# sorted_idx = [str(idx+1).zfill(3) for idx in sorted_idx]
users = sorted(users, key= diff_ratio, reverse= True)

nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =( 6.4*ncols, 4.8 * nrows))


data = [[],[],[]]
for idx, user in enumerate(users):
    both = np.sum(df.query(f"users == '{user}' and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == '{user}' and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == '{user}' and bout_type=='p'")["step"])
    data[0].append(both)
    data[1].append(phone)
    data[2].append(watch)
data = np.array(data)/10000
datacum = data.cumsum(axis = 0)
ax[0].barh(y= np.arange(.5, len(users)+.5),width = data[0],label= "both", color = color["both"])
ax[0].barh(y= np.arange(.5, len(users)+.5),width = data[1], left =datacum[0], label= "phone", color = color["phone"])
ax[0].barh(y= np.arange(.5, len(users)+.5),width = data[2], left=datacum[1], label= "watch", color = color["watch"])
ax[0].set_yticks(np.arange(.5, len(users)+.5))
ax[0].set_yticklabels(users, fontsize = 6)
ax[0].set_xlabel('Step Count(x10000)')

data = data/datacum[2]
datacum = datacum/datacum[2]
ax[1].barh(y= np.arange(.5, len(users)+.5),width = data[0],label= "both", color = color["both"])
ax[1].barh(y= np.arange(.5, len(users)+.5),width = data[1], left =datacum[0], label= "phone", color = color["phone"])
ax[1].barh(y= np.arange(.5, len(users)+.5),width = data[2], left=datacum[1], label= "watch", color = color["watch"])
ax[1].set_yticks(np.arange(.5, len(users)+.5))
ax[1].set_yticklabels(users, fontsize = 6)
# ax[1].set_yticklabels(sorted_idx, fontsize = 6)
ax[0].set_ylabel('Participants')
ax[1].set_xlabel('Ratio of Step count')

ax[1].legend()

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

