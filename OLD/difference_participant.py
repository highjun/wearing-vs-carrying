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
data = [[],[],[]]
for idx, user in enumerate(users):
    both = np.sum(df.query(f"users == {user} and bout_type=='b'")["step"])
    watch = np.sum(df.query(f"users == {user} and bout_type=='w'")["step"])
    phone = np.sum(df.query(f"users == {user} and bout_type=='p'")["step"])
    data[0].append(both)
    data[1].append(phone)
    data[2].append(watch)
data = np.array(data)/10000
p= np.sum(df.query(f"bout_type=='p'")["step"])
w = np.sum(df.query(f"bout_type=='w'")["step"])
p_= np.sum(df.query(f"0<hour<=6 and bout_type == 'p'")["step"])
w_= np.sum(df.query(f"0<hour<=6 and bout_type == 'w'")["step"])
print(f'Phone:{round(p_/p*100,1)}, Watch:{round(w_/w*100,1)}')

for idx in range(200):
    w_50 = np.sum(df.query(f"step < {(idx+1)*50} and step >= {idx*50} and bout_type=='w'")["step"])
    p_50 = np.sum(df.query(f"step < {(idx+1)*50} and step >= {idx*50} and bout_type=='p'")["step"])
    print(f'[{idx*50},{idx*50+50}) Phone:{round(p_50/p*100,1)}, Watch:{round(w_50/w*100,1)}')

datacum = data.cumsum(axis = 0)
ax.barh(y= np.arange(.5, len(users)+.5),width = data[0],label= "both", color = color["both"])
ax.barh(y= np.arange(.5, len(users)+.5),width = data[1], left =datacum[0], label= "phone", color = color["phone"])
ax.barh(y= np.arange(.5, len(users)+.5),width = data[2], left=datacum[1], label= "watch", color = color["watch"])
ax.legend()
ax.set_yticks(np.arange(.5, len(users)+.5))
ax.set_yticklabels(users)
ax.set_ylabel('Participants')
ax.set_xlabel('Step Count(x10000)')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"New", f"{cur}.png"))

