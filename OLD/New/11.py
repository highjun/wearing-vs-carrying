from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
users = sorted(set(df["users"]))

nrows= 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

data = [[],[]]
for idx, user in enumerate(users):
    user_df = df.query(f"users =='{user}'")
    both = np.sum(user_df.query(f"bout_type=='b' and hour < 18 and hour > 9")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and hour < 18 and hour > 9")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and hour < 18 and hour > 9")["step"])
    total = both+watch+phone
    p_wd = (phone + both)/total
    w_wd = (watch + both)/total

    both = np.sum(user_df.query(f"bout_type=='b' and hour > 18")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and hour > 18")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and hour > 18")["step"])
    total = both+watch+phone
    p_we = (phone + both)/total
    w_we = (watch + both)/total
    
    data[0].append(p_wd-p_we)
    data[1].append(w_wd-w_we)
print(data)
print(ax.boxplot(data, showfliers= True))
ax.set_xticks([1,2])
ax.set_xticklabels(["Phone","Watch"])
ax.set_ylabel("Difference of Ratio")

print(np.sum(np.abs(np.array(data[0])) > 0.05)/len(data[0]))
print(np.sum(np.abs(np.array(data[1])) > 0.05)/len(data[1]))

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))