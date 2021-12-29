from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
users = sorted(set(df["users"]))
weekday = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

nrows= 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))


for idx, user in enumerate(users):
    if idx <2:
        continue
    print(user)
    data = [[],[]]
    user_df = df.query(f"users =='{user}'")
    for wd in range(7):
        both = np.sum(user_df.query(f"bout_type=='b' and weekday == {wd}")["step"])
        watch = np.sum(user_df.query(f"bout_type=='w' and weekday == {wd}")["step"])
        phone = np.sum(user_df.query(f"bout_type=='p' and weekday == {wd}")["step"])
        total = both+watch+phone
        data[0].append((both+phone)/total)
        data[1].append((both+watch)/total)

    ax.bar(x= np.arange(0.5, 7*2.5,2.5), height = data[0], label = "phone", color = color["phone"])
    ax.bar(x= np.arange(1.5, 7*2.5,2.5), height = data[1], label = "watch", color = color["watch"])
    ax.legend()
    ax.set_xticks(np.arange(1, 7*2.5, 2.5))
    ax.set_xticklabels(weekday, rotation= 45, ha="right", rotation_mode="anchor")
    ax.set_ylim([0,1])
    ax.set_ylabel("Ratio")
    break
print(np.sum(np.array(data).max(axis = 0) > 0.9))

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))