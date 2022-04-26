import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
cwd = os.getcwd()
data_dir = os.path.join(cwd, "Data")
data_path  = os.path.join(data_dir, 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
df['first'] = pd.to_datetime(df['first'])
df['last'] = pd.to_datetime(df['last'])


color = ['tab:blue', 'tab:orange', 'tab:green']
#step count distribution
# df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
# df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
users= set(df["users"])
for user in users:
    user = 16
    df_ = df.query(f'users == {user}')

    df_['hour'] = df_['first'].dt.hour
    df_['weekday'] = df_['first'].dt.weekday
    df_['date'] = df_['first'].dt.date
    df_ = df_[df_['date']==dt.date(2021,7,16)]


    fig, ax = plt.subplots(nrows =1, ncols = 1, figsize = (6,3))#,constrained_layout = True)
    tmp = df_.groupby(['users','date']).sum()
    tmp = tmp.reset_index().rename(columns={'level_0':'users','level_1':'date'})
    n_day = tmp.shape[0]

    tmp = df_.groupby(['hour','bout_type']).agg(phone = ('phone','sum'), watch = ('watch','sum'),count = ('bout_type','count'))
    tmp = tmp.reindex(pd.MultiIndex.from_product([list(range(24)), ['p','w','b']]), fill_value = 0)
    tmp = tmp.reset_index().rename(columns={'level_0':'hour','level_1':'bout_type'})

    p_bout = np.array(tmp.query("bout_type == 'p'")['count'])#["phone"])/n_day
    w_bout = np.array(tmp.query("bout_type == 'w'")['count'])#["watch"])/n_day
    b_bout = np.array(tmp.query("bout_type == 'b'")['count'])
    # b_bout = (np.array(tmp.query("bout_type == 'b'")["watch"])+ np.array(tmp.query("bout_type == 'b'")["phone"]))/n_day/2
    data = np.array([p_bout,w_bout,b_bout])
    data_cum = data.cumsum(axis = 0)
    ax.bar(x= list(np.arange(0.5,24.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
    ax.bar(x= list(np.arange(0.5,24.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
    ax.bar(x= list(np.arange(0.5,24.5)), height = data[0,:], width = .8, label='phone', color = color[0])

    ax.set_xticks(np.arange(0.5,24.5))
    ax.set_xticklabels([str(idx).zfill(2) for idx in range(24)])
    ax.set_xlabel('Hour')
    ax.set_ylabel('step count')
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(cwd,'Fig','Time',f'bout_time_ratio.png'))
    plt.close()
    break


    # fig, ax = plt.subplots(nrows =2, ncols = 2, figsize = (12,6))#,constrained_layout = True)


    # tmp = df_.groupby(['users','date']).sum()
    # tmp = tmp.reset_index().rename(columns={'level_0':'users','level_1':'date'})
    # n_day = tmp.shape[0]
    
    # tmp = df_.groupby(['hour','bout_type']).agg(phone = ('phone','sum'), watch = ('watch','sum'), duration =('duration','sum'),count = ('bout_type','count'))
    # tmp = tmp.reindex(pd.MultiIndex.from_product([list(range(24)), ['p','w','b']]), fill_value = 0)
    # tmp = tmp.reset_index().rename(columns={'level_0':'hour','level_1':'bout_type'})
    # p_bout = np.array(tmp.query("bout_type == 'p'")["count"])/n_day
    # w_bout = np.array(tmp.query("bout_type == 'w'")["count"])/n_day
    # b_bout = np.array(tmp.query("bout_type == 'b'")["count"])/n_day
    # data = np.array([p_bout,w_bout,b_bout])
    # data_cum = data.cumsum(axis = 0)
    # ax[0][0].bar(x= list(np.arange(0.5,24.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
    # ax[0][0].bar(x= list(np.arange(0.5,24.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
    # ax[0][0].bar(x= list(np.arange(0.5,24.5)), height = data[0,:], width = .8, label='phone', color = color[0])

    # p_bout = np.array(tmp.query("bout_type == 'p'")["phone"])/n_day
    # w_bout = np.array(tmp.query("bout_type == 'w'")["watch"])/n_day
    # b_bout = (np.array(tmp.query("bout_type == 'b'")["watch"])+ np.array(tmp.query("bout_type == 'b'")["phone"]))/n_day/2
    # data = np.array([p_bout,w_bout,b_bout])
    # data_cum = data.cumsum(axis = 0)
    # ax[1][0].bar(x= list(np.arange(0.5,24.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
    # ax[1][0].bar(x= list(np.arange(0.5,24.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
    # ax[1][0].bar(x= list(np.arange(0.5,24.5)), height = data[0,:], width = .8, label='phone', color = color[0])

    # ax[1][0].set_xticks(np.arange(0.5,24.5))
    # ax[1][0].set_xticklabels([str(idx).zfill(2) for idx in range(24)])
    # ax[1][0].set_xlabel('Hour')

    # ax[0][0].set_ylabel('number of bout')
    # ax[1][0].set_ylabel('step count')

    # tmp = df_.groupby(['weekday','users','date']).sum()
    # tmp = tmp.reset_index().rename(columns={'level_0':'weekday','level_1':'users','level_2':'date'})
    # n_day = np.array(tmp.groupby(['weekday']).agg(count = ('phone','count'))['count'])

    # tmp = df_.groupby(['weekday','bout_type']).agg(phone = ('phone','sum'), watch = ('watch','sum'), duration =('duration','sum'),count = ('bout_type','count'))
    # tmp = tmp.reindex(pd.MultiIndex.from_product([list(range(7)), ['p','w','b']]), fill_value = 0)
    # tmp = tmp.reset_index().rename(columns={'level_0':'weekday','level_1':'bout_type'})
    # p_bout = np.array(tmp.query("bout_type == 'p'")["count"])/n_day
    # w_bout = np.array(tmp.query("bout_type == 'w'")["count"])/n_day
    # b_bout = np.array(tmp.query("bout_type == 'b'")["count"])/n_day
    # data = np.array([p_bout,w_bout,b_bout])
    # data_cum = data.cumsum(axis = 0)
    # ax[0][1].bar(x= list(np.arange(0.5,7.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
    # ax[0][1].bar(x= list(np.arange(0.5,7.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
    # ax[0][1].bar(x= list(np.arange(0.5,7.5)), height = data[0,:], width = .8, label='phone', color = color[0])

    # # p_bout = np.array(tmp.query("bout_type == 'p'")["duration"])/n_day
    # # w_bout = np.array(tmp.query("bout_type == 'w'")["duration"])/n_day
    # # b_bout = np.array(tmp.query("bout_type == 'b'")["duration"])/n_day
    # # data = np.array([p_bout,w_bout,b_bout])
    # # data_cum = data.cumsum(axis = 0)
    # # ax[1][1].bar(x= list(np.arange(0.5,7.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
    # # ax[1][1].bar(x= list(np.arange(0.5,7.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
    # # ax[1][1].bar(x= list(np.arange(0.5,7.5)), height = data[0,:], width = .8, label='phone', color = color[0])

    # p_bout = np.array(tmp.query("bout_type == 'p'")["phone"])/n_day
    # w_bout = np.array(tmp.query("bout_type == 'w'")["watch"])/n_day
    # b_bout = (np.array(tmp.query("bout_type == 'b'")["watch"])+ np.array(tmp.query("bout_type == 'b'")["phone"]))/n_day/2
    # data = np.array([p_bout,w_bout,b_bout])
    # data_cum = data.cumsum(axis = 0)
    # ax[1][1].bar(x= list(np.arange(0.5,7.5)), height = data[2,:], width = .8, bottom = data_cum[1,:],label='both', color = color[2])
    # ax[1][1].bar(x= list(np.arange(0.5,7.5)), height = data[1,:], width = .8, bottom = data_cum[0,:],label='watch', color = color[1])
    # ax[1][1].bar(x= list(np.arange(0.5,7.5)), height = data[0,:], width = .8, label='phone', color = color[0])

    # ax[1][1].set_xticks(np.arange(0.5,7.5))
    # ax[1][1].set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
    # ax[1][1].set_xlabel('Day of Week')

    # ax[0][0].set_xticks([])
    # ax[0][1].set_xticks([])

    # ax[0][1].legend()
    # plt.tight_layout()
    # plt.savefig(os.path.join(cwd,'Fig','Time',f'bout_time_ratio_{user}.png'))
    # plt.close()
