import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

all = pd.read_excel("../Preprocess/all_user.xlsx")
tmp = all.groupby(["user","timestamp"]).agg(day = ('day','first'), weekday = ('weekday','first'), hour = ('hour','first'), p_idx = ('phone_chunk_idx','sum'), w_idx = ('watch_chunk_idx','sum'), p_step = ('step','first'), w_step = ('step','last'))
def f(x):
    d = {}
    d['p_act'] = np.sum(x['w_idx']==0)
    d['p_step'] = np.sum(x['p_step'][x['w_idx']==0])
    d['w_act'] = np.sum(x['p_idx']==0)
    d['w_step'] = np.sum(x['w_step'][x['p_idx']==0])
    d['b_act'] = np.sum((x.values[:,4]*x.values[:,3])!=0)
    d['bp_step'] = np.sum(x['p_step'][x['p_idx']!=0]) - d['p_step']
    d['bw_step'] = np.sum(x['w_step'][x['w_idx']!=0]) - d['w_step']

    return pd.Series(d, index=['p_act', 'p_step', 'w_act', 'w_step','b_act','bp_step','bw_step'])

tmp_hour = tmp.groupby(["user","day","weekday","hour"]).apply(f)
tmp_day = tmp.groupby(["user","day","weekday"]).apply(f)
tmp_hour.reset_index(inplace = True)
tmp_day.reset_index(inplace = True)

day_start = 10
day_end = 20
day_count = day_end - day_start
tmp_ = tmp_hour.query(f"user == 3 and day <{day_end} and day >= {day_start}")
fig, ax=plt.subplots(figsize = (16,4),constrained_layout = True)
plt.plot(tmp_.values[:,1]*24 + tmp_.values[:,3]-24*day_start,tmp_["bw_step"], label='watch', c= "firebrick")
plt.plot(tmp_.values[:,1]*24 + tmp_.values[:,3]-24*day_start, tmp_["bp_step"], label = 'phone',c = "cornflowerblue")
plt.legend()
plt.xticks(range(0,24*day_count,6), ["00","06","12","18"]*day_count)
plt.xlabel('''Time(Hour)

Difference of step counts for both detected: P2's Day 10 ~ 20
''')
plt.ylabel("number of steps")
plt.savefig("../Figure/015.png")