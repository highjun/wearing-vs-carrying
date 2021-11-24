import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_path  = os.path.join(cwd,'Data', 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['first'] = pd.to_datetime(df['first'])
df['last'] = pd.to_datetime(df['last'])
df['date'] = df['first'].dt.date

color = ['tab:blue', 'tab:orange', 'tab:green']
# df['date'] = pd.to_datetime(df['timestamp']).dt.date
# n_day = {}
# n_step = {}
# for user in set(list(df['users'])):
#     n_day[user] = len(set(df.query(f'users == {user}')['date']))
#     tmp = np.sum(df.query(f'users=={user} and bout_type =="p"')['phone'])
#     tmp += np.sum(df.query(f'users=={user} and bout_type =="w"')['watch'])
#     tmp += np.sum(df.query(f'users=={user} and bout_type =="b"')['phone'])/2
#     tmp += np.sum(df.query(f'users=={user} and bout_type =="b"')['watch'])/2
#     n_step[user] = tmp/n_day[user]
#step count distribution
# df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
# df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (12,8),constrained_layout = True)
users = list(set(df["users"]))
# users.sort(key = lambda x: n_step[x])
# print(n_step)
data= [[],[],[]]
for user in users:
    phone = np.sum(df.query(f"users=={user} and bout_type=='p'")["phone"])
    watch = np.sum(df.query(f"users=={user} and bout_type=='w'")["watch"])
    both = np.sum((np.array(df.query(f"users=={user} and bout_type=='b'")["phone"])+ np.array(df.query(f"users=={user} and bout_type=='b'")["watch"]))/2)
    data[0].append(phone)#/n_day[user])
    data[1].append(watch)#/n_day[user])
    data[2].append(both)#/n_day[user])
# print([n_step[user] for user in users])
# print(np.array(data).cumsum(axis=0)[2,:])
data = np.array(data)/10000
data_cum = data.cumsum(axis=0)
ax[0].barh([str(user) for user in users], data[2,:], left=data_cum[2,:]-data[2,:], height = 0.5,label='both',color = color[2])
ax[0].barh([str(user) for user in users], data[1,:], left = data_cum[1,:]-data[1,:], height = 0.5,label='watch',color = color[1])
ax[0].barh([str(user) for user in users], data[0,:], left=data_cum[0,:]- data[0,:], height = 0.5,label='phone',color = color[0])
# data =[[],[],[]]
# for user in users:
#     phone = np.sum(df.query(f"users=={user} and bout_type=='p'")["duration"])
#     watch = np.sum(df.query(f"users=={user} and bout_type=='w'")["duration"])
#     both = np.sum(df.query(f"users=={user} and bout_type=='b'")["duration"])
#     data[0].append(phone/n_day[user])
#     data[1].append(watch/n_day[user])
#     data[2].append(both/n_day[user])
# data = np.array(data)
# data_cum = data.cumsum(axis=0)
# ax[1].barh([str(user) for user in users], data[2,:], left=data_cum[1,:], height = 0.5,label='both',color = color[2])
# ax[1].barh([str(user) for user in users], data[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
# ax[1].barh([str(user) for user in users], data[0,:], left=data_cum[0,:]- data[0,:], height = 0.5,label='phone',color = color[0])
data= [[],[],[]]
for user in users:
    phone = len(df.query(f"users=={user} and bout_type=='p'")["phone"])
    watch = len(df.query(f"users=={user} and bout_type=='w'")["watch"])
    both = len(df.query(f"users=={user} and bout_type=='b'")["phone"])
    data[0].append(phone)#/n_day[user])
    data[1].append(watch)#/n_day[user])
    data[2].append(both)#/n_day[user])
data = np.array(data)
data_cum = data.cumsum(axis=0)
ax[1].barh([str(user) for user in users], data[2,:], left=data_cum[1,:], height = 0.5,label='both',color = color[2])
ax[1].barh([str(user) for user in users], data[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
ax[1].barh([str(user) for user in users], data[0,:], left=data_cum[0,:]- data[0,:], height = 0.5,label='phone',color = color[0])
ax[0].set_yticks(np.arange(0,len(users)))
ax[0].set_yticklabels(users)
ax[0].set_xlabel('step count')
# ax[0].set_xticks([])
# ax[1].set_xlabel('duration')
# # ax[1].set_xticks([])
# ax[1].set_yticks([])
ax[1].set_xlabel('number')
# ax[2].set_xticks([])
ax[1].set_yticks([])
ax[1].legend(ncol=3)
plt.savefig(os.path.join(cwd,'Fig','bout_AB_compare.png'))
