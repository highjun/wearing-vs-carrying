from Experiment.util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = [(row['last']-row['first']).seconds/60+1 for _, row in df.iterrows()]
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
scale = 10000
users = set(df['users'])

fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (8,4))

data = [[],[],[]]
for user in users:
    phone = np.sum(df.query(f"users=={user} and bout_type=='p'")["step"])
    watch = np.sum(df.query(f"users=={user} and bout_type=='w'")["step"])
    both = np.sum(df.query(f"users=={user} and bout_type=='b'")["step"])
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)

data0 = np.array(data)/scale
data_cum = data0.cumsum(axis = 0)
ax[0].barh([str(user) for user in users], data0[2,:],left=data_cum[1,:], height = 0.5,label='both',color = color['both'])
ax[0].barh([str(user) for user in users], data0[1,:], left = data_cum[0,:], height = 0.5,label='watch',color = color['watch'])
ax[0].barh([str(user) for user in users], data0[0,:], height = 0.5,label='phone',color = color['phone'])
ax[0].set_xlabel('All')
ax[0].set_xlim([0,40])

data = [[],[],[]]
for idx, user in enumerate(users):
    phone = 0
    watch = 0
    both = 0
    tmp = df.query(f"users == {user}")
    # remove under 50 step counts
    # tmp = tmp.query("duration >= 3")
    #remove under 5 minute step
    # tmp = tmp.query("duration > 10")
    #remove jogging Assume more than 2000 is jogging
    tmp = tmp.query(f"step < 1000")
    # tmp = tmp.query(f"weekday < 5")
    # remove non-wearing day
    # we assume watch was not weared if step count is less than 5% of total step count
    nonwearing = tmp.groupby(['date']).agg(phone=('phone','sum'),watch = ('watch','sum'))
    nonwearing = np.array(nonwearing.index)[np.array(nonwearing['watch'])/(np.array(nonwearing['phone'])+np.array(nonwearing['watch'])) > .05] 
    print(f"-------------{user}----------------")
    for date in nonwearing:
        # if tmp[tmp['date']==date].query("bout_type == 'p'").shape[0]> 0:
        #     print(tmp[tmp['date']==date].query("bout_type == 'p'")[["first","last","phone","watch","step","duration"]])
        # if tmp[tmp['date']==date].query("bout_type == 'w'").shape[0]> 0:
        #     print(tmp[tmp['date']==date].query("bout_type == 'w'")[["first","last","phone","watch","step","duration"]])
        phone += np.sum(tmp[tmp['date']==date].query(f"bout_type=='p'")["step"])
        watch += np.sum(tmp[tmp['date']==date].query(f"bout_type=='w'")["step"])
        both += np.sum(df[df['date']==date].query(f"users == {user} and weekday< 5").query(f"bout_type=='b'")["step"])
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)
data = np.array(data)/10000
data_cum = data.cumsum(axis = 0)
ax[1].barh([str(user) for user in users], data[2,:],left=data_cum[1,:], height = 0.5,label='both',color = color['both'])
ax[1].barh([str(user) for user in users], data[1,:], left = data_cum[0,:], height = 0.5,label='watch',color = color['watch'])
ax[1].barh([str(user) for user in users], data[0,:], height = 0.5,label='phone',color = color['phone'])
ax[1].set_xlabel('Removed')
ax[1].set_xlim([0,40])
print("******************")
print("줄어든 비율")
for idx, user in enumerate(users):
    print(f"{user}:phone={1-data[0][idx]/data0[0][idx]}, watch={1-data[1][idx]/data0[1][idx]}")
print("******************")
for idx, _ in enumerate(users):
    print(f"{idx} phone: {int(data[0][idx]/data_cum[2][idx]*100)}, watch: {int(data[1][idx]/data_cum[2][idx]*100)}, both: {int(data[2][idx]/data_cum[2][idx]*100)}")
ax[-1].legend()
plt.savefig(os.path.join(os.getcwd(),f'{cur}.png'))
