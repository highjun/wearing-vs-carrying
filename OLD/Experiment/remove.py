from Experiment.util import *

df = load_bout()
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = [(row['last']-row['first']).seconds/60+1 for idx, row in df.iterrows()]
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for idx, row in df.iterrows()]
scale = 10000
users = set(df['users'])

fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (8,4))

data = [[],[],[]]
for user in users:
    phone = np.sum(df.query(f"users=={user} and bout_type=='p'")["phone"])
    watch = np.sum(df.query(f"users=={user} and bout_type=='w'")["watch"])
    both = np.sum((np.array(df.query(f"users=={user} and bout_type=='b'")["phone"])+ np.array(df.query(f"users=={user} and bout_type=='b'")["watch"]))/2)
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)

data = np.array(data)/scale
data_cum = data.cumsum(axis = 0)
ax[0].barh([str(user) for user in users], data[2,:],left=data_cum[1,:], height = 0.5,label='both',color = color['both'])
ax[0].barh([str(user) for user in users], data[1,:], left = data_cum[0,:], height = 0.5,label='watch',color = color['watch'])
ax[0].barh([str(user) for user in users], data[0,:], height = 0.5,label='phone',color = color['phone'])
ax[0].set_xlabel('All')

data = [[],[],[]]
for user in users:
    phone = 0
    watch = 0
    both = 0
    tmp = df.query(f"users == {user}")
    #remove under 50 step counts
    # tmp = tmp.query("step >= 50")
    #remove under 5 minute step
    tmp = tmp.query("duration > 5")
    #remove jogging Assume more than 2000 is jogging
    tmp = tmp.query(f"bout_type!='w' or watch <2000")
    # remove non-wearing day
    # we assume watch was not weared if step count is less than 5% of total step count
    nonwearing = tmp.groupby(['date']).agg(phone=('phone','sum'),watch = ('watch','sum'))
    nonwearing = np.array(nonwearing.index)[np.array(nonwearing['watch'])/(np.array(nonwearing['phone'])+np.array(nonwearing['watch'])) > .05] 
    print(f"-------------{user}----------------")
    for date in nonwearing:
        print(tmp[tmp['date']==date].query("bout_type == 'p'")[["first","last","phone","watch","step","duration","bout_type"]])
        print(tmp[tmp['date']==date].query("bout_type == 'w'")[["first","last","phone","watch","step","duration","bout_type"]])
        phone += np.sum(tmp[tmp['date']==date].query(f"bout_type=='p'")["step"])
        watch += np.sum(tmp[tmp['date']==date].query(f"bout_type=='w'")["step"])
        both += np.sum(tmp[tmp['date']==date].query(f"bout_type=='b'")["step"])
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)
data = np.array(data)/10000
data_cum = data.cumsum(axis = 0)
ax[1].barh([str(user) for user in users], data[2,:],left=data_cum[1,:], height = 0.5,label='both',color = color['both'])
ax[1].barh([str(user) for user in users], data[1,:], left = data_cum[0,:], height = 0.5,label='watch',color = color['watch'])
ax[1].barh([str(user) for user in users], data[0,:], height = 0.5,label='phone',color = color['phone'])

for idx, val in enumerate(data[2]/data_cum[2,:]):
    print(f"{idx+1}:{val}")
ax[1].set_xlabel('Removed')
ax[-1].legend()
plt.savefig(os.path.join(os.getcwd(),'Fig','remove.png'))
