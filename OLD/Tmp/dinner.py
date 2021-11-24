# 참가자 별로 얼마나 큰 차이가 날 수 있는지 보자.
from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

work = {
    '001': [8,18],
    '002': [9.5, 21],
    '003': [9, 18],
    '004': [8, 16],
    '005': [11, 18],
    '006': [9,18],
    '007': [9,18],
    '008': [9,22],
    '009': [9,18],
    '010': [8.5,22],
    '011': [9, 16],
    '012': [8.5, 22.5],
    '013': [12, 24],
    '014': [11, 22],
    '015': [8, 18],
    '016': [9, 20],
    '017': [8, 17],
    '018': [7, 18],
    '019': [9, 18],
    '020': [9,18],
    '021': [9,20.5],
    '022': [8.5, 21],
    '023': [9,22],
    '024': [9.5, 16],
    '025': [10, 19.5],
    '026': [12, 21],
    '027': [8, 17],
    '028': [9, 20],
    '029': [9, 17],
    '030': [13, 17.5],
    '031': [11, 23.5],
    'lsl4497': [10.5, 21],
    'dbsdmsgh0709': [6.5,17.5],
    'hunmin007': [9, 22],
    'isaacok0919': [8,18],
    'junseo141560': [9,16],
    'coals817': [8, 22],
    'any7863': [6, 19],
    'rlatjdud0301': [8.5, 13],
    'youjian9868':[8, 16.5],
    'ysh5813': [0,24],
    'badkjin':[7.5,18]
}


df = load_bout()
users = sorted(list(set(df['users'])))
def diff_ratio(user):
    both = np.sum(df.query(f"users == '{user}' and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == '{user}' and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == '{user}' and bout_type=='p'")["step"])
    ratio = (watch - phone)/(both+watch+phone)
    return ratio
users = sorted(users, key= diff_ratio, reverse= True)

nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =( 6.4*ncols, 4.8 * nrows))


data = [[],[],[]]
for idx, user in enumerate(users):
    user_df = df.query(f"users == '{user}'")
    nonwear_date = user_df.groupby('date').agg(phone = ('phone','sum'), watch = ('watch','sum'))
    nonwear_date = nonwear_date[nonwear_date["watch"] == 0].index
    for date in nonwear_date:
        user_df = user_df[user_df["date"]!= date] #58,35,6
    both = np.sum(user_df.query(f"weekday < 5 and hour>={work[user][0]} and hour<={work[user][1]} and bout_type=='b'")["step"])
    watch = np.sum(user_df.query(f"weekday < 5 and hour>={work[user][0]} and hour<={work[user][1]} and bout_type=='w'")["step"])
    phone = np.sum(user_df.query(f"weekday < 5 and hour>={work[user][0]} and hour<={work[user][1]} and bout_type=='p'")["step"])
    data[0].append(both)
    data[1].append(phone)
    data[2].append(watch)
data = np.array(data)/10000
datacum = data.cumsum(axis = 0)

data = data/datacum[2]
datacum = datacum/datacum[2]
ax[0].barh(y= np.arange(.5, len(users)+.5),width = data[0],label= "both", color = color["both"])
ax[0].barh(y= np.arange(.5, len(users)+.5),width = data[1], left =datacum[0], label= "phone", color = color["phone"])
ax[0].barh(y= np.arange(.5, len(users)+.5),width = data[2], left=datacum[1], label= "watch", color = color["watch"])
ax[0].set_yticks(np.arange(.5, len(users)+.5))
ax[0].set_yticklabels(users, fontsize = 6)
ax[0].set_xlabel('Step Count in Day Time')

data = [[],[],[]]
for idx, user in enumerate(users):
    user_df = df.query(f"users == '{user}'")
    nonwear_date = user_df.groupby('date').agg(phone = ('phone','sum'), watch = ('watch','sum'))
    nonwear_date = nonwear_date[nonwear_date["watch"] == 0].index
    for date in nonwear_date:
        user_df = user_df[user_df["date"]!= date] #58,35,6
    both = np.sum(user_df.query(f"weekday < 5 and step < 1500 and hour>{work[user][1]} and bout_type=='b'")["step"])
    both += np.sum(user_df.query(f"weekday < 5 and step < 1500 and hour<{work[user][0]} and bout_type=='b'")["step"])
    watch = np.sum(user_df.query(f"weekday < 5 and step < 1500 and hour>{work[user][1]} and bout_type=='w'")["step"])
    watch +=  np.sum(user_df.query(f"weekday < 5 and step < 1500 and hour<{work[user][0]} and bout_type=='w'")["step"])
    phone = np.sum(user_df.query(f"weekday < 5 and step < 1500 and hour>{work[user][1]} and bout_type=='p'")["step"])
    phone += np.sum(user_df.query(f"weekday < 5 and step < 1500 and hour<{work[user][0]} and bout_type=='p'")["step"])
    data[0].append(both)
    data[1].append(phone)
    data[2].append(watch)
data = np.array(data)/10000
datacum = data.cumsum(axis = 0)
data = data/datacum[2]
datacum = datacum/datacum[2]

ax[1].barh(y= np.arange(.5, len(users)+.5),width = data[0],label= "both", color = color["both"])
ax[1].barh(y= np.arange(.5, len(users)+.5),width = data[1], left =datacum[0], label= "phone", color = color["phone"])
ax[1].barh(y= np.arange(.5, len(users)+.5),width = data[2], left=datacum[1], label= "watch", color = color["watch"])
ax[1].set_yticks(np.arange(.5, len(users)+.5))
ax[1].set_yticklabels(users, fontsize = 6)
ax[1].set_xlabel('Step Count in Night Time')

ax[1].legend()

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

