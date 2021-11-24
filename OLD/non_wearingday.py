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
watch = 0
phone = 0
for idx,user in enumerate(users):
    wear = df.query(f"users =={user}").groupby(['date','weekday']).agg(phone=('phone','sum'),watch = ('watch','sum'))
    n_day = wear.shape[0]
    non_wearing = wear[wear["watch"]/(wear["phone"]+wear["watch"]) < 0.05].index.get_level_values(0)
    print(wear[wear["watch"]/(wear["phone"]+wear["watch"]) < 0.05])
    tmp = df.query(f"users=={user}")
    for day in non_wearing:
        tmp_ = tmp[tmp['date'] == day]
        watch += np.sum(tmp_.query("bout_type=='w'")["step"])
        phone += np.sum(tmp_.query("bout_type=='p'")["step"])
    data.append(len(non_wearing) / n_day)
total_watch = np.sum(df.query("bout_type=='w'")["step"])
total_phone = np.sum(df.query("bout_type=='p'")["step"])
print(f"Difference Explained: watch={watch/total_watch*100}, phone={phone/total_phone*100}")
ax.boxplot(data, positions=[0])
ax.scatter(np.ones_like(data), data, s= 4)
ax.set_xlim([-1,2])
ax.set_xticks([])
ax.set_ylabel('Ratio of Non-wearing day')
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"New", f"{cur}.png"))

