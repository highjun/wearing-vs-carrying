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

nrows = len(users)
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*1, 4.8*3), sharex = True)


data = [[],[],[]]
for idx, user in enumerate(users):
    user_df = df.query(f"users == '{user}'")
    nonwear_date = user_df.groupby('date').agg(phone = ('phone','sum'), watch = ('watch','sum'))
    nonwear_date = nonwear_date[nonwear_date["watch"] == 0].index
    for date in nonwear_date:
        user_df = user_df[user_df["date"]!= date] #58,35,6
    both = np.sum(user_df.query(f"weekday < 5 and hour>={9} and hour<={18} and bout_type=='b'")["step"])
    watch = np.sum(user_df.query(f"weekday < 5 and hour>={9} and hour<={18} and bout_type=='w'")["step"])
    phone = np.sum(user_df.query(f"weekday < 5 and hour>={9} and hour<={18} and bout_type=='p'")["step"])
    all = both+watch+phone
    both /= all
    watch /= all
    phone /= all
    ax[idx].barh(y= 1, height = 0.8,width = both, label= "both", color = color["both"])
    ax[idx].barh(y= 1, height = 0.8,width = phone, left =both, label= "phone", color = color["phone"])
    ax[idx].barh(y= 1, height = 0.8,width = watch, left=both+phone, label= "watch", color = color["watch"])

    both = np.sum(user_df.query(f"weekday < 5 and hour>{18} and bout_type=='b'")["step"])
    both += np.sum(user_df.query(f"weekday < 5 and hour<{9} and bout_type=='b'")["step"])
    watch = np.sum(user_df.query(f"weekday < 5 and hour>{18} and bout_type=='w'")["step"])
    watch +=  np.sum(user_df.query(f"weekday < 5 and hour<{9} and bout_type=='w'")["step"])
    phone = np.sum(user_df.query(f"weekday < 5 and hour>{18} and bout_type=='p'")["step"])
    phone += np.sum(user_df.query(f"weekday < 5 and hour<{9} and bout_type=='p'")["step"])
    all = both+watch+phone
    both /= all
    watch /= all
    phone /= all
    ax[idx].barh(y= 0, height = 0.8,width = both, label= "both", color = color["both"])
    ax[idx].barh(y= 0, height = 0.8,width = phone, left =both, label= "phone", color = color["phone"])
    ax[idx].barh(y= 0, height = 0.8,width = watch, left=both+phone, label= "watch", color = color["watch"])
    # ax[idx].set_ylim([-1,2])
    ax[idx].set_yticks([0.5])
    ax[idx].set_yticklabels([user])

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

