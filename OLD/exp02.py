from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
scale = 10000
users = set(df['users'])

data = [[],[],[]]
phone_act = np.zeros((len(users),24))
watch_act = np.zeros((len(users),24))
for idx,user in enumerate(users):
    tmp = df.query(f"users =={user}")
    tmp = tmp.query(f"step < 2000")
    nonwearing = tmp.groupby(['date']).agg(phone=('phone','sum'),watch = ('watch','sum'))
    nonwearing = np.array(nonwearing.index)[np.array(nonwearing['watch'])/(np.array(nonwearing['phone'])+np.array(nonwearing['watch'])) > .05] 
    n_day = 0
    for date in tmp['date']:
        if date.weekday() <5 and date in nonwearing:
            n_day += 1
            tmp_ = tmp[tmp['date']==date]
            for _,row in tmp_.iterrows():
                phone_act[idx][tmp_['hour']] += row['phone']
                watch_act[idx][tmp_['hour']] += row['watch']
            # for p in set(tmp_.query(f"bout_type=='p'")["first"].dt.hour):
            #     phone_act[idx][p] += 1
            # for w in set(tmp_.query(f"bout_type=='w'")["first"].dt.hour):
            #     watch_act[idx][w] += 1
    phone_act[idx]/= n_day*5000 if n_day >0 else 1
    watch_act[idx]/= n_day*5000 if n_day >0 else 1
print(phone_act)
print(watch_act)
# phone_act = phone_act > .6
# watch_act = watch_act > .6
# fig,ax = plt.subplots(nrows=1, ncols = 1, figsize=(6,12))
# def timelines(user, watch,phone, ax):
#     watch_color = np.array([(1,0,0,w if w<1 else 1) for w in watch])
#     phone_color = np.array([(0,0,1,p if p<1 else 1) for p in phone])
#     ax.hlines([2*user+1]*24, np.arange(0,24), np.arange(1,25), colors = watch_color)
#     ax.hlines([2*user]*24, np.arange(0,24), np.arange(1,25), colors = phone_color)
# for idx, user in enumerate(users):
#     timelines(idx, watch_act[idx],phone_act[idx],ax)

# ax.hlines(np.arange(-.5,len(users)*2-0.5,2),xmin = 0, xmax = 24,linestyles = '--', colors = 'k')
# ax.set_yticks(np.arange(.5, 2*len(users)+0.5,2))
# ax.set_yticklabels(users)
# ax.vlines(x=[0,6,12,18], ymin=0, ymax = 2*len(users), colors='r')
# ax.set_xticks(range(0,24,6))
# plt.savefig(os.path.join(os.getcwd(),f'{cur}.png'))




