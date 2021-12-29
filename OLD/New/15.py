from util import *

df = load_bout()

nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

users = sorted(set(df["users"]))
short = df.query("distance <= 150")
big = df.query("distance > 150")

short_data = [[],[],[]]
big_data = [[],[],[]]

for idx, user in enumerate(users):
    user = "018"
    short_user = short.query(f"users =='{user}'")
    big_user = big.query(f"users =='{user}'")    
    for wd in range(24):
        both = np.sum(short_user.query(f"bout_type=='b' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        watch = np.sum(short_user.query(f"bout_type=='w' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        phone = np.sum(short_user.query(f"bout_type=='p' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        total = both+watch+phone
        short_data[0].append(both)
        short_data[1].append(phone)
        short_data[2].append(watch)
    for wd in range(24):
        both = np.sum(big_user.query(f"bout_type=='b' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        watch = np.sum(big_user.query(f"bout_type=='w' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        phone = np.sum(big_user.query(f"bout_type=='p' and weekday < 6 and hour >= {wd} and hour <{wd+1}")["step"])
        total = both+watch+phone
        big_data[0].append(both)
        big_data[1].append(phone)
        big_data[2].append(watch)
    break

short_data = np.array(short_data)
short_datacum = short_data.cumsum(axis = 0)
# data = data/datacum[2]
# datacum = datacum/datacum[2]
ax[0].bar(x= np.arange(.5, 24+.5),height = short_data[0],label= "both", color = color["both"])
ax[0].bar(x= np.arange(.5, 24+.5),height = short_data[1], bottom=short_datacum[0], label= "phone", color = color["phone"])
ax[0].bar(x= np.arange(.5, 24+.5),height = short_data[2], bottom=short_datacum[1], label= "watch", color = color["watch"])
ax[0].set_xticks(np.arange(.5, 24+.5))
ax[0].set_xticklabels([str(i).zfill(2) for i in range(24)], fontsize = 6)
ax[0].set_xlabel('Hour')
ax[0].set_ylabel("Step count")

big_data = np.array(big_data)
big_datacum = big_data.cumsum(axis = 0)
# data = data/datacum[2]
# datacum = datacum/datacum[2]
ax[1].bar(x= np.arange(.5, 24+.5),height = big_data[0],label= "both", color = color["both"])
ax[1].bar(x= np.arange(.5, 24+.5),height = big_data[1], bottom=big_datacum[0], label= "phone", color = color["phone"])
ax[1].bar(x= np.arange(.5, 24+.5),height = big_data[2], bottom=big_datacum[1], label= "watch", color = color["watch"])
ax[1].set_xticks(np.arange(.5, 24+.5))
ax[1].set_xticklabels([str(i).zfill(2) for i in range(24)], fontsize = 6)
ax[1].set_xlabel('Hour')
ax[1].set_ylabel("Step count")
ax[1].legend()
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures","15.png"))

