from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
users = sorted(set(df["users"]))

nrows= 8
ncols = 8
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

data = []
for idx, user in enumerate(users):
    user_df = df.query(f"users =='{user}'")
    both = np.sum(user_df.query(f"bout_type=='b' and weekday< 5 and hour < 18 and hour >= 9")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday< 5 and hour < 18 and hour >= 9")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday< 5 and hour < 18 and hour >= 9")["step"])
    total = both+watch+phone
    p_wd_d = (phone+ both)/total
    w_wd_d = (watch+ both)/total
    both = np.sum(user_df.query(f"bout_type=='b' and weekday< 5 and hour >= 18")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday< 5 and hour >= 18")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday< 5 and hour >= 18")["step"])
    total = both+watch+phone
    p_wd_n = (phone+ both)/total
    w_wd_n = (watch+ both)/total
    
    both = np.sum(user_df.query(f"bout_type=='b' and weekday< 5")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday< 5")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday< 5")["step"])
    total = both+watch+phone
    p_wd = (phone + both)/total
    w_wd = (watch + both)/total

    both = np.sum(user_df.query(f"bout_type=='b' and weekday>=5")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday>=5")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday>=5")["step"])
    total = both+watch+phone
    p_we = (phone + both)/total
    w_we = (watch + both)/total
    data.append([p_wd_d, w_wd_d, p_wd_n, w_wd_n, p_wd, w_wd, p_we, w_we])
data = np.array(data)
data = data.reshape(8, -1)
labels = ["Phone Ratio for Day time","Watch Ratio for Day time", 
        "Phone Ratio for Night time","Watch Ratio for Night time",
        "Phone Ratio for Weekday", "Watch Ratio for Weekday",
        "Phone Ratio for Weekend", "Watch Ratio for Weekend"]
for i in range(8):
    for j in range(8):
        ax[i][j].scatter(data[i],data[j], s=4)
        ax[i][j].set_xlabel(labels[i])
        ax[i][j].set_ylabel(labels[j])
        ax[i][j].set_xlim([0,1])
        ax[i][j].set_ylim([0,1])
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))