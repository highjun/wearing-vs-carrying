from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = sorted(list(set(df['users'])))
def avg_step(user):
    both = np.sum(df.query(f"users == '{user}' and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == '{user}' and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == '{user}' and bout_type=='p'")["step"])
    total = (both+watch+phone)/ len(set(df.query(f"users == '{user}'")["date"]))
    return total
# sorted_idx = sorted(range(len(users)), key=lambda k: diff_ratio(users[k]))
# sorted_idx = [str(idx+1).zfill(3) for idx in sorted_idx]
users = sorted(users, key= avg_step, reverse= True)

nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =( 6.4*ncols, 4.8 * nrows))

data_p =[[],[],[]]
data_w =[[],[],[]]
for idx, user in enumerate(users):
    n_day =len(set(df.query(f"users == '{user}'")["date"]))
    both = np.sum(df.query(f"users == '{user}' and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == '{user}' and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == '{user}' and bout_type=='p'")["step"])
    total = both+watch+phone
    avg = total/n_day
    if avg < 5000:
        data_p[0].append((both+phone)/total)
        data_w[0].append((both+watch)/total)
    elif avg < 10000:
        data_p[1].append((both+phone)/total)
        data_w[1].append((both+watch)/total)
    else:
        data_p[2].append((both+phone)/total)
        data_w[2].append((both+watch)/total)
ax[0].boxplot(data_p, labels= ["low","medium","high"])
ax[0].set_xlabel("Phone")
ax[1].boxplot(data_w, labels= ["low","medium","high"])
ax[1].set_xlabel("Watch")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

