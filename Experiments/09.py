from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
users = sorted(set(df["users"]))
weekday = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

nrows= 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

data = [[],[]]
for idx, user in enumerate(users):
    user_df = df.query(f"users =='{user}'")
    both = np.sum(user_df.query(f"bout_type=='b' and weekday <5")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday <5")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday <5")["step"])
    total = both+watch+phone
    p_wd = (phone + both)/total
    w_wd = (watch + both)/total

    both = np.sum(user_df.query(f"bout_type=='b' and weekday >=5")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday >=5")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday >=5")["step"])
    total = both+watch+phone
    p_we = (phone + both)/total
    w_we = (watch + both)/total
    
    data[0].append(p_wd-p_we)
    data[1].append(w_wd-w_we)
print(data)
print(ax.boxplot(data, showfliers= True))
ax.set_xticks([1,2])
ax.set_xticklabels(["Phone","Watch"])

# ax.bar(x= np.arange(0.5, len(users)*2.5,2.5), height = data[0], label = "phone", color = color["phone"])
# ax.bar(x= np.arange(1.5, len(users)*2.5,2.5), height = data[1], label = "watch", color = color["watch"])
# ax.legend()
# ax.set_xticks(np.arange(1, len(users)*2.5, 2.5))
# ax.set_xticklabels(weekday, rotation= 45, ha="right", rotation_mode="anchor")
# ax.set_ylim([0,1])
ax.set_ylabel("Difference of Ratio")
# print(np.sum(np.array(data).max(axis = 0) > 0.9))

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))