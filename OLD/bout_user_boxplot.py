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

fig, ax = plt.subplots(nrows = 1, ncols = 1,figsize = (12,5))
type = ['phone','watch','both']
for col in range(3):
    data = []
    for idx,user in enumerate(users):
        data.append(df.query(f"users == {user} and bout_type =='{type[col][0]}'")["step"])
    ax.boxplot(data, positions= np.arange(0,len(users))*4 + col, showfliers= False, showcaps= False)
ax.set_xticks(np.arange(0, 4*len(users)))
ax.set_xticklabels([(type[i%4][0] if i%4!=3 else '') + ('' if i%4!=1 else f'\n{users[i//4]}') for i in np.arange(0,4*len(users))])
ax.set_ylim([0,210])
ax.set_ylabel('Step Count')
ax.set_xlabel('Participants')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"New", f"{cur}.png"))

