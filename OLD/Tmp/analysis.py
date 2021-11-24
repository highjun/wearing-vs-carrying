from util import *
from matplotlib.lines import Line2D

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]
users = list(set(df['users']))

nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =( 6.4*ncols, 4.8 * nrows))
weekday = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

individual = True
user = '013'

bin_size = 30
user_df = df.query(f"users == '{user}'")  #70, 12, 16
nonwear_date = user_df.groupby('date').agg(phone = ('phone','sum'), watch = ('watch','sum'))
nonwear_date = nonwear_date[nonwear_date["watch"] == 0].index
for date in nonwear_date:
    user_df = user_df[user_df["date"]!= date] #58,35,6
# user_df = user_df[user_df["hour"]>= 6]
# user_df = user_df[user_df["hour"]< 20] # 48, 47,3

# nonwear_date = user_df.groupby('date').agg(phone = ('phone','sum'), watch = ('watch','sum'))
# nonwear_date = nonwear_date[nonwear_date["watch"] == 0].index
# for date in nonwear_date:
#     user_df = user_df[user_df["date"]!= date] #65,27,6

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
colors= [color["both"] if bin[idx][0] >0 and bin[idx][1] > 0 else (color["phone"] if bin[idx][0]>0 else (color["watch"] if bin[idx][1]> 0 else "white")) for idx in range(24*2*n_day)]
xmin = [ idx%48 for idx in range(len(y))]
xmax = [ idx%48 + 1 for idx in range(len(y))]
ax[0].hlines(y= y, xmin = xmin, xmax = xmax, colors=colors)
ax[0].set_yticks(np.arange(n_day))
ax[0].set_yticklabels([f"{idx.month}-{idx.day},{weekday[idx.weekday()]}"for idx in [first_date + dt.timedelta(days = i) for i in range(n_day)]], fontsize = 6)
ax[0].set_xticks(np.arange(0,48, 2))
ax[0].set_xticklabels(np.arange(0,24), fontsize = 6)
ax[0].set_xlabel('Hour')
legend_elements = [Line2D([0], [0], color=color['phone'], lw=4, label='Phone'),
                   Line2D([0], [0], color=color['watch'], lw=4, label='Watch'),
                   Line2D([0], [0], color=color['both'], lw=4, label='Both'),]
ax[1].legend(handles = legend_elements,loc="upper left")
data = [np.sum(user_df.query("bout_type=='b'")["step"]),
        np.sum(user_df.query("bout_type=='p'")["step"]),
        np.sum(user_df.query("bout_type=='w'")["step"])]
ax[1].barh(y= 0,width = data[0]/np.sum(data),label= "both", color = color["both"])
ax[1].barh(y= 0,width = data[1]/np.sum(data), left =data[0]/np.sum(data), label= "phone", color = color["phone"])
ax[1].barh(y= 0,width = data[2]/np.sum(data), left=(data[0]+data[1])/np.sum(data), label= "watch", color = color["watch"])
ax[1].text(data[0]/np.sum(data)/2, y= 0, s=str(int(data[0]/np.sum(data)*100)), va='center', ha = 'center')
ax[1].text(data[0]/np.sum(data) + data[1]/np.sum(data)/2, y= 0, s=str(int(data[1]/np.sum(data)*100)), va='center', ha = 'center')
ax[1].text(data[0]/np.sum(data) + data[1]/np.sum(data) + data[2]/np.sum(data)/2, y= 0, s=str(int(data[2]/np.sum(data)*100)), va='center', ha = 'center')
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_xlabel('Ratio of Step count')
ax[1].set_ylim([-2,2])
plt.savefig(os.path.join(os.getcwd(), "_.png"))