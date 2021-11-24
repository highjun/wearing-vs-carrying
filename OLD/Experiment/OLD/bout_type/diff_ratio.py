import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
data_path  = os.path.join(cwd, 'bout.csv')
df = pd.read_csv(data_path, index_col= 0, header = 0)
color = ['tab:blue', 'tab:orange', 'tab:green']

#step count distribution
df = df.groupby(['users','bout_idx']).agg(phone=('phone','sum'), watch=('watch','sum'), first=('timestamp','first'),last = ('timestamp','last'), bout_type=('bout_type','first'), duration=('bout_type','count'))
df = df.reset_index().rename({'level_0':'users','level_1':'bout_idx'})
# print(df)
fig, ax = plt.subplots(nrows =1, ncols = 1, figsize = (6,4),constrained_layout = True)

p_step = np.array(df.query(f"bout_type=='p'")["phone"])
w_step = np.array(df.query(f"bout_type=='w'")["watch"])
b_step = (np.array(df.query(f"bout_type=='b'")["phone"])+ np.array(df.query(f"bout_type=='b'")["watch"]))/2

p_step, bin =np.histogram(p_step,bins= np.arange(0,20*50,50))
w_step, bin = np.histogram(w_step,bins= np.arange(0,20*50,50))
b_step, bin = np.histogram(b_step,bins= np.arange(0,20*50,50))
data = np.array([p_step,w_step, b_step])
data_cum = data.cumsum(axis=0)
ax.bar(x= list(np.arange(0.5,20.5-1)), height = data[2,:]/data_cum[2,:], width = .8, bottom = data_cum[1]/data_cum[2,:],label='both', color = color[2])
ax.bar(x= list(np.arange(0.5,20.5-1)), height = data[1,:]/data_cum[2,:], width = .8, bottom = data_cum[0]/data_cum[2,:],label='watch', color = color[1])
ax.bar(x= list(np.arange(0.5,20.5-1)), height = data[0,:]/data_cum[2,:], width = .8,label='phone', color = color[0])
ax.set_xticks(np.arange(0,20))
ax.set_xticklabels(np.arange(0*50,20*50,50), fontsize =7)
ax.set_xlabel('Step',fontsize = 16)

# p_duration = np.array(df.query(f"bout_type=='p'")["duration"])
# w_duration = np.array(df.query(f"bout_type=='w'")["duration"])
# b_duration = np.array(df.query(f"bout_type=='b'")["duration"])

# # p_duration, bin = np.histogram(p_duration,bins =  np.arange(1,25))
# # w_duration, bin = np.histogram(w_duration,bins =  np.arange(1,25))
# # b_duration, bin = np.histogram(b_duration,bins =  np.arange(1,25))
# # data = np.array([p_duration,w_duration, b_duration])
# # data_cum = data.cumsum(axis=0)
# # ax[1].bar(x= list(np.arange(0.5,24.5-1)), height = data[2,:]/data_cum[2,:], width = .8, bottom = data_cum[1,:]/data_cum[2,:],label='both', color = color[2])
# # ax[1].bar(x= list(np.arange(0.5,24.5-1)), height = data[1,:]/data_cum[2,:], width = .8, bottom = data_cum[0,:]/data_cum[2,:],label='watch', color = color[1])
# # ax[1].bar(x= list(np.arange(0.5,24.5-1)), height = data[0,:]/data_cum[2,:], width = .8, label='phone', color = color[0])
ax.legend()
# # ax[1].set_xticks(np.arange(0.5,24.5-1))
# # ax[1].set_xticklabels(np.arange(1,24))
# # ax[1].set_xlabel('Duration')
plt.savefig(os.path.join(cwd,'Fig','bout_ty.png'))
