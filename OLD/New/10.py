from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
users = sorted(set(df["users"]))
# weekday = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

nrows= 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))


for idx, user in enumerate(users):
    if idx <2:
        continue
    print(user)
    data = [[],[]]
    user_df = df.query(f"users =='{user}'")
    for wd in range(24):
        both = np.sum(user_df.query(f"bout_type=='b' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        watch = np.sum(user_df.query(f"bout_type=='w' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        phone = np.sum(user_df.query(f"bout_type=='p' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        total = both+watch+phone
        data[0].append((both+phone)/total)
        data[1].append((both+watch)/total)

    ax.bar(x= np.arange(0.5, 24*2.5,2.5), height = data[0], label = "phone", color = color["phone"])
    ax.bar(x= np.arange(1.5, 24*2.5,2.5), height = data[1], label = "watch", color = color["watch"])
    ax.legend()
    ax.set_xticks(np.arange(1, 24*2.5, 2.5))
    ax.set_xticklabels([str(x).zfill(2) +"-" + str(x+1).zfill(2) for x in range(24)], rotation= 45, ha="right", rotation_mode="anchor")
    ax.set_ylim([0,1])
    ax.set_ylabel("Ratio")
    break

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))