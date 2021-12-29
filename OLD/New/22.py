from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
df["is_small"] = [1 if step< 120 else 0 for step in df["step"]]
survey = load_survey()
users = sorted(set(df["users"]))

nrows= 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

type2int = {"n":1, "p":1,"w":2,"b":2}
survey["day"]= [type2int[idx] for idx in  survey["cw_day"]]
survey["night"]= [type2int[idx] for idx in  survey["cw_night"]]

labels = ['always','day','no']
data = []
watch_biased = []
phone_biased =[]
unbiased = []
for user in users:
    user_df = df.query(f"users =='{user}'")
    both = np.sum(user_df.query(f"bout_type=='b' and weekday< 5")["step"])
    watch = np.sum(user_df.query(f"bout_type=='w' and weekday< 5")["step"])
    phone = np.sum(user_df.query(f"bout_type=='p' and weekday< 5")["step"])
    total = both+watch+phone
    p = (phone)/(total if total > 0 else 1)
    w = (watch)/(total if total > 0 else 1)
    b = (both)/(total if total > 0 else 1)
    if b> .9:
        unbiased.append(user)
    elif w > p:
        watch_biased.append(user)
    else:
        phone_biased.append(user)
labels = ["unbiased","watch-biased","phone-biased"]
for idx,users_ in enumerate([unbiased, watch_biased, phone_biased]):
    data = []
    for user in users_:
        user_df = df.query(f"users =='{user}'")
        both = np.sum(user_df.query(f"bout_type=='b' and weekday< 5 and hour < 18 and hour >= 9")["step"])
        watch = np.sum(user_df.query(f"bout_type=='w' and weekday< 5 and hour < 18 and hour >= 9")["step"])
        phone = np.sum(user_df.query(f"bout_type=='p' and weekday< 5 and hour < 18 and hour >= 9")["step"])
        total = both+watch+phone
        p_wd_d = (phone+ both)/(total if total > 0 else 1)
        w_wd_d = (watch+ both)/(total if total > 0 else 1)
        both = np.sum(user_df.query(f"bout_type=='b' and weekday< 5 and hour >= 18")["step"])
        watch = np.sum(user_df.query(f"bout_type=='w' and weekday< 5 and hour >= 18")["step"])
        phone = np.sum(user_df.query(f"bout_type=='p' and weekday< 5 and hour >= 18")["step"])
        total = both+watch+phone
        p_wd_n = (phone+ both)/(total if total > 0 else 1)
        w_wd_n = (watch+ both)/(total if total > 0 else 1)
        data.append([p_wd_d, w_wd_d, p_wd_n, w_wd_n])
    data = np.array(data)
    ax[0].scatter(data[:,0], data[:,2],label= labels[idx],s = 4)
    ax[1].scatter(data[:,1], data[:,3],label= labels[idx],s = 4)
ax[0].set_xlim([0,1])
ax[1].set_xlim([0,1])
ax[0].set_ylim([0,1])
ax[1].set_ylim([0,1])
ax[0].set_xlabel("Phone Day")
ax[1].set_xlabel("Watch Day")
ax[0].set_ylabel("Night")
ax[1].legend()
data = np.array(data)
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))