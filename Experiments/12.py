from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
df["hour"]= df["first"].dt.hour
users = sorted(set(df["users"]))

nrows= 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows), sharex = True)

data = []
for idx, user in enumerate(users):
    if idx < 2:
        continue
    print(user)
    break
user_df = df.query(f"users =='{user}'")
step_df = user_df.query(f"step< 150").groupby("hour").count()
step_df = step_df.reindex(np.arange(24),fill_value = 0)
data = step_df["step"]
# break    
ax[0].bar(x= range(24), height = data, color ="tab:olive")
ax[0].set_xticks(np.arange(24))
ax[0].set_xticklabels([str(x).zfill(2) +"-" + str(x+1).zfill(2) for x in range(24)], rotation= 45, ha="right", rotation_mode ="anchor")
ax[0].set_xlabel("[0,150)")
ax[0].set_ylabel("Frequency")

step_df = user_df.query(f"step >= 1000").groupby("hour").count()
step_df = step_df.reindex(np.arange(24),fill_value = 0)
data = step_df["step"]
# break    
ax[1].bar(x= range(24), height = data, color ="tab:olive")
ax[1].set_xticks(np.arange(24))
ax[1].set_xticklabels([str(x).zfill(2) +"-" + str(x+1).zfill(2) for x in range(24)], rotation= 45, ha="right", rotation_mode ="anchor")
ax[1].set_xlabel("[1000,)")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))