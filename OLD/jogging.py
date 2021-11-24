from numpy import histogram
from Experiment.util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
df['hour'] = df['first'].dt.hour
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = [(row['last']-row['first']).seconds/60+1 for _, row in df.iterrows()]
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
users = list(set(df['users']))

fig, ax = plt.subplots(nrows = 1, ncols = 1)
type = ['phone','watch','both']
data = []
phone = 0
watch = 0
for idx,user in enumerate(users):
    tmp = df.query(f"users=={user}")
    wear = tmp.groupby(['date','weekday']).agg(phone=('phone','sum'),watch = ('watch','sum'))
    wearing = wear[wear["watch"]/(wear["phone"]+wear["watch"]) > 0.05].index.get_level_values(0)
    for day in wearing:
        tmp_ = tmp[tmp['date'] == day]
        if tmp_.query("bout_type!='b' and step > 1000").shape[0] != 0:
            print(tmp_.query("bout_type!='b' and step > 1000"))
            data+= list(tmp_.query("bout_type!='b' and step > 1000")['hour'])
        phone+=np.sum(tmp_.query("bout_type=='p' and step > 1000")["step"])
        watch+=np.sum(tmp_.query("bout_type=='w' and step > 1000")["step"])
total_watch = np.sum(df.query("bout_type=='w'")["step"])
total_phone = np.sum(df.query("bout_type=='p'")["step"])
print(f"Difference Explained: watch={watch/total_watch*100}, phone={phone/total_phone*100}")
hours = np.zeros(24)
for d in data:
    hours[d] += 1
ax.bar(np.arange(0.5,24.5), hours)
ax.set_xticks(np.arange(0,25))
ax.set_ylabel('Frequency')
ax.set_xlabel('''Hour

Jogging time from all users''')
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"New", f"{cur}.png"))

