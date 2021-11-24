import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_path  = os.path.join(cwd, 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['date'] = pd.to_datetime(df['timestamp']).dt.date

n_day = {}
n_step = {}
users = list(set(df["users"]))
for user in users:
    n_day[user] = len(set(df.query(f'users == {user}')['date']))
    tmp = np.sum(df.query(f'users=={user} and bout_type =="p"')['phone'])
    tmp += np.sum(df.query(f'users=={user} and bout_type =="w"')['watch'])
    tmp += np.sum(df.query(f'users=={user} and bout_type =="b"')['phone'])/2
    tmp += np.sum(df.query(f'users=={user} and bout_type =="b"')['watch'])/2
    steps = [np.sum(df.query(f'users=={user} and bout_type =="p"')['phone'])/tmp,
    np.sum(df.query(f'users=={user} and bout_type =="w"')['watch'])/tmp]
    n_step[user] = steps
users.sort(key = lambda x: n_step[x][0]- n_step[x][1])

color = ['tab:blue', 'tab:orange', 'tab:green']
#step count distribution
df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (12,6))#,constrained_layout = True)
data= [[],[],[]]
for user in users:
    phone = np.sum(df.query(f"users=={user} and bout_type=='p'")["phone"])
    watch = np.sum(df.query(f"users=={user} and bout_type=='w'")["watch"])
    both = np.sum((np.array(df.query(f"users=={user} and bout_type=='b'")["phone"])+ np.array(df.query(f"users=={user} and bout_type=='b'")["watch"]))/2)
    sum_ = phone+watch+both
    phone /= sum_
    watch /= sum_
    both /= sum_
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)
data = np.array(data)
data_cum = data.cumsum(axis=0)
ax[0].barh([str(user) for user in users], data[2,:], left=data_cum[1,:], height = 0.5,label='both',color = color[2])
# for idx in range(len(users)):
#     ax[0].text(data_cum[1,idx]+ data[2,idx]/2, idx, str(int(data[2,idx]*100)), ha='center',va='center',fontsize = 6, color = 'white')
ax[0].barh([str(user) for user in users], data[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
# for idx in range(len(users)):
#     ax[0].text(data_cum[0,idx]+ data[1,idx]/2, idx, str(int(data[1,idx]*100)), ha='center',va='center',fontsize = 6, color = 'white')
ax[0].barh([str(user) for user in users], data[0,:], left=data_cum[0,:]- data[0,:], height = 0.5,label='phone',color = color[0])
# for idx in range(len(users)):
#     ax[0].text( data[0,idx]/2, idx, str(int(data[0,idx]*100)), ha='center',va='center', color = 'white',fontsize = 6,)
data =[[],[],[]]
for user in users:
    phone = len(df.query(f"users=={user} and bout_type=='p'")["duration"])
    watch = len(df.query(f"users=={user} and bout_type=='w'")["duration"])
    both = len(df.query(f"users=={user} and bout_type=='b'")["duration"])
    sum_ = phone+watch+both
    phone /= sum_
    watch /= sum_
    both /= sum_
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)
data = np.array(data)
data_cum = data.cumsum(axis=0)
ax[1].barh([str(user) for user in users], data[2,:], left=data_cum[1,:], height = 0.5,label='both',color = color[2])
# for idx in range(len(users)):
#     ax[1].text(data_cum[1,idx]+ data[2,idx]/2, idx, str(int(data[2,idx]*100)), ha='center',va='center',fontsize = 6, color = 'white')
ax[1].barh([str(user) for user in users], data[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
# for idx in range(len(users)):
#     ax[1].text(data_cum[0,idx]+ data[1,idx]/2, idx, str(int(data[1,idx]*100)), ha='center',va='center',fontsize = 6, color = 'white')
ax[1].barh([str(user) for user in users], data[0,:], left=data_cum[0,:]- data[0,:], height = 0.5,label='phone',color = color[0])
# for idx in range(len(users)):
#     ax[1].text(data[0,idx]/2, idx, str(int(data[0,idx]*100)), ha='center',va='center', color = 'white',fontsize = 6)
# data= [[],[],[]]
# for user in users:
#     phone = len(df.query(f"users=={user} and bout_type=='p'")["duration"])
#     watch = len(df.query(f"users=={user} and bout_type=='w'")["duration"])
#     both = len(df.query(f"users=={user} and bout_type=='b'")["duration"])
#     sum_ = phone+watch+both
#     phone /= sum_
#     watch /= sum_
#     both /= sum_
#     data[0].append(phone)
#     data[1].append(watch)
#     data[2].append(both)
# data = np.array(data)
# data_cum = data.cumsum(axis=0)
# ax[2].barh([str(user) for user in users], data[2,:], left=data_cum[1,:], height = 0.5,label='both',color = color[2])
# ax[2].barh([str(user) for user in users], data[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
# ax[2].barh([str(user) for user in users], data[0,:], left=data_cum[0,:]- data[0,:], height = 0.5,label='phone',color = color[0])

ax[0].set_yticks(np.arange(0,len(users)))
ax[0].set_ylim([-1,32.5])
ax[0].set_yticklabels(users, fontsize = 12)
ax[0].set_xlabel('step count', fontsize = 16)
ax[0].set_xticks([])
ax[1].set_ylim([-1,32.5])
ax[1].set_xlabel('number', fontsize = 16)
ax[1].set_xticks([])
ax[1].set_yticks([])
# ax[2].set_xlabel('number')
# ax[2].set_xticks([])
# ax[2].set_yticks([])
ax[1].legend(ncol=3)
plt.tight_layout()
plt.savefig(os.path.join(cwd,'Fig','bout_AB_ratio.png'))