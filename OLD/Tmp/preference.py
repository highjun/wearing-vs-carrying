from util import *
from matplotlib.lines import Line2D

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]
users = list(set(df['users']))

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =( 6.4*ncols, 4.8 * nrows))
weekday = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']


data = [[],[],[]]
for idx, user in enumerate(users):
    bin_size = 30
    user_df = df.query(f"users == '{user}'")  #70, 12, 16
    
    first_date = sorted(set(user_df["date"]))[0]
    last_date = sorted(set(user_df["date"]))[-1]
    n_day = (last_date-first_date).days +1
    bin = np.zeros((n_day*24*60//bin_size,2))
    def timeasbin(datetime_):
        day = (datetime_.date() - first_date).days
        n_bin = (datetime_.hour*60 + datetime_.minute)//bin_size
        nbin = n_bin + day*24*60//bin_size
        return nbin
    for idx, row in user_df.iterrows():
        first_bin = timeasbin(row["first"])
        last_bin = timeasbin(row["last"])
        for idx in range(first_bin,last_bin+1):
            bin[idx][0] += row["phone"]
            bin[idx][1] += row["watch"]
    y= np.repeat(np.arange(0,n_day),24*60//bin_size)
    colors= np.array(['b' if bin[idx][0] >0 and bin[idx][1] > 0 else ('p' if bin[idx][0]>0 else ('w' if bin[idx][1]> 0 else "white")) for idx in range(24*2*n_day)])
    both = len(colors[colors=='b'])
    phone = len(colors[colors=='p'])
    watch = len(colors[colors=='w'])
    print(both, phone, watch)
    data[0].append(both)
    data[1].append(phone)
    data[2].append(watch)
data = np.array(data)
datacum = data.cumsum(axis =0)
data = data/datacum[2]
datacum = datacum/datacum[2]
ax.barh(y= np.arange(.5, len(users)+.5),width = data[0],label= "both", color = color["both"])
ax.barh(y= np.arange(.5, len(users)+.5),width = data[1], left =datacum[0], label= "phone", color = color["phone"])
ax.barh(y= np.arange(.5, len(users)+.5),width = data[2], left=datacum[1], label= "watch", color = color["watch"])
ax.set_yticks(np.arange(.5, len(users)+.5))
ax.set_yticklabels(users, fontsize = 6)
ax.set_xlabel('PWB Ratio')
ax.legend()


plt.savefig(os.path.join(os.getcwd(), "_.png"))