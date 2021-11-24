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
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =( 6.4*2*ncols, 4.8 * nrows))


data = [[],[]]
for idx, user in enumerate(users):
    both = np.sum(df.query(f"users == '{user}' and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == '{user}' and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == '{user}' and bout_type=='p'")["step"])
    total = both+watch+phone
    data[0].append((both+phone)/total)
    data[1].append((both+watch)/total)

ax.bar(x= np.arange(0.5, len(users)*2.5,2.5), height = data[0], label = "phone", color = color["phone"])
ax.bar(x= np.arange(1.5, len(users)*2.5,2.5), height = data[1], label = "watch", color = color["watch"])
ax.legend()
ax.set_xticks(np.arange(1, len(users)*2.5, 2.5))
ax.set_xticklabels(users, fontsize = 6, rotation= 45, ha="right", rotation_mode="anchor")
ax.set_ylim([0,1])
ax.set_ylabel("Ratio")
print(np.sum(np.array(data).max(axis = 0) > 0.9))

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

