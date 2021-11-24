import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from pandas.core.groupby.generic import DataFrameGroupBy
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

data_path = os.path.join(os.getcwd(),"Data","bout.csv")
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['first'] = pd.to_datetime(df['first'])
df['last'] = pd.to_datetime(df['last'])
df["date"]= df['first'].dt.date
df["weekday"]= df['first'].dt.weekday


color = ['tab:blue', 'tab:orange', 'tab:green']
users = set(df['users'])

fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (8,4),constrained_layout = True)

# data0 =[[],[]]
# for user in users:
#     p_step = np.sum(df.query(f"users=={user} and bout_type=='p' and phone < 50")["phone"])
#     w_step = np.sum(df.query(f"users=={user} and bout_type=='w' and watch < 50")["watch"])
#     data0[0].append(p_step)
#     data0[1].append(w_step)
# data0 = np.array(data0)/10000
# data_cum = data0.cumsum(axis=0)
# ax[0].barh([str(user) for user in users], data0[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
# ax[0].barh([str(user) for user in users], data0[0,:], height = 0.5,label='phone',color = color[0])
# ax[0].set_xlabel('[0,50)')

# data1 = [[],[]]
# df["weekday"]= df['first'].dt.weekday
# for user in users:
#     p_step = np.sum(df.query(f"users=={user} and weekday < 5 and bout_type=='p'")["phone"])
#     w_step = np.sum(df.query(f"users=={user} and weekday < 5 and bout_type=='w'")["watch"])
#     data1[0].append(p_step)
#     data1[1].append(w_step)
# data1 = np.array(data1)/10000
# data_cum = data1.cumsum(axis=0)
# ax[1].barh([str(user) for user in users], data1[1,:], left=data_cum[0,:], height = 0.5,label='watch',color = color[1])
# ax[1].barh([str(user) for user in users], data1[0,:], height = 0.5,label='phone',color = color[0])
# ax[1].set_xlabel('Weekend')

# data2 = []
# df["date"] =df['first'].dt.date
# for user in users:
#     tmp = df.query(f"users == {user}").groupby(['date']).agg(phone=('phone','sum'),watch = ('watch','sum'))
#     p_step = np.sum(np.array(tmp['phone'])[tmp['watch']/(tmp['phone']+tmp['watch']) < .05])
#     data2.append(p_step)
# data2 = np.array(data2)/10000
# ax[2].barh([str(user) for user in users], data2, height = 0.5,label='phone',color = color[0])
# ax[2].set_xlabel('Non wearing')

data3 = [[],[],[]]
for user in users:
    tmp = df.query(f"users == {user}")
    phone = np.sum(df.query(f"users=={user} and bout_type=='p'")["phone"])
    watch = np.sum(df.query(f"users=={user} and bout_type=='w'")["watch"])
    both = np.sum((np.array(df.query(f"users=={user} and bout_type=='b'")["phone"])+ np.array(df.query(f"users=={user} and bout_type=='b'")["watch"]))/2)
    data3[0].append(phone)
    data3[1].append(watch)
    data3[2].append(both)

data3 = np.array(data3)/10000
data_cum = data3.cumsum(axis = 0)
ax[0].barh([str(user) for user in users], data3[2,:],left=data_cum[1,:], height = 0.5,label='both',color = color[2])
ax[0].barh([str(user) for user in users], data3[1,:], left = data_cum[0,:], height = 0.5,label='watch',color = color[1])
ax[0].barh([str(user) for user in users], data3[0,:], height = 0.5,label='phone',color = color[0])

ax[0].set_xlabel('All')

data = [[],[],[]]
for user in users:
    print(f'---------------{user}--------------')
    tmp = df.query(f"users == {user}").groupby(['date']).agg(phone=('phone','sum'),watch = ('watch','sum'))
    # print(np.array(tmp.index)[np.array(tmp['watch'])/(np.array(tmp['phone'])+np.array(tmp['watch'])) < .05])
    phone = 0
    watch = 0
    both = 0
    print(tmp.index)
    print(np.array(tmp['watch'])/(np.array(tmp['phone'])+np.array(tmp['watch'])))
    print(np.array(tmp.index)[np.array(tmp['watch'])/(np.array(tmp['phone'])+np.array(tmp['watch'])) > .05])
    for date in np.array(tmp.index)[np.array(tmp['watch'])/(np.array(tmp['phone'])+np.array(tmp['watch'])) > .05]:
        # p_step = tnp.array(tmp['phone'])[tmp['watch']/(tmp['phone']+tmp['watch']) < .05]
        print(df[df['date']==date].query(f"users=={user} and bout_type=='p' and phone >= 50 and weekday < 5"))
        phone += np.sum(df[df['date']==date].query(f"users=={user} and bout_type=='p' and phone >= 50 and weekday < 5")["phone"])
        watch += np.sum(df[df['date']==date].query(f"users=={user} and bout_type=='w' and watch >= 50 and weekday < 5")["watch"])
        both += np.sum((np.array(df[df['date']==date].query(f"users=={user} and bout_type=='b' and weekday < 5")["phone"])+ np.array(df[df['date']==date].query(f"users=={user} and bout_type=='b' and weekday < 5")["watch"]))/2)
    
    data[0].append(phone)
    data[1].append(watch)
    data[2].append(both)
data = np.array(data)/10000
data_cum = data.cumsum(axis = 0)
ax[1].barh([str(user) for user in users], data[2,:],left=data_cum[1,:], height = 0.5,label='both',color = color[2])
ax[1].barh([str(user) for user in users], data[1,:], left = data_cum[0,:], height = 0.5,label='watch',color = color[1])
ax[1].barh([str(user) for user in users], data[0,:], height = 0.5,label='phone',color = color[0])

ax[1].set_xlabel('Removed')

ax[-1].legend()
# ax[1].set_xlabel('[50,\infty)',fontsize = 16)


plt.savefig(os.path.join(os.getcwd(),'tmp','ratio_from.png'))
