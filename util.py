import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy import stats
import os, glob

cwd = os.getcwd()
data_dir = os.path.join(cwd,'Data')
user_dir = os.path.join(data_dir, 'Users')
fig_dir = os.path.join(cwd,"Refactoring","Fig")
color = {'phone': '#1f77b4', 'watch':'#ff7f0e', 'both': '#2ca02c'}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def loadDF():
    df = pd.read_csv(os.path.join(os.getcwd(),"Data_",'bout.csv'), header = 0)
    for val in ['first','last','date']:
        df[val] = pd.to_datetime(df[val])
    tmp = df.groupby(['uid','btype']).agg(step = ('step','sum'))
    tmp = tmp.unstack(level = 1, fill_value = 0)
    tmp = tmp.apply(lambda x: x/np.sum(x), axis = 1)
    tmp.columns = ['b','p','w']
    valid_user = list(tmp.query('b != 0').index)
    df = df.query(f"uid in @valid_user")
    return df

def getBoutInfo(df, groupby):
    columns = []
    btypes = ['b','p','w']

    for metric in ['ratio', 'step','weight', 'count']:
            for btype in ['b','p','w']:
                columns.append(btype+metric)
    columns.append('totalstep')
    columns.append('totalcount')
    if df.shape[0] == 0:
        return pd.DataFrame([],columns= columns)
    tmp = df.groupby([*groupby,"btype"]).agg(step = ("step","sum"), number = ('step','count'))
    tmp = tmp.reindex(['b','p','w'],level = len(groupby))
    tmp = tmp.unstack(level=len(groupby), fill_value = 0)
    tmp = tmp.apply(lambda x: np.concatenate((x[:3]/np.sum(x[:3]), x[:3], x[3:]/np.sum(x[3:]), x[3:], np.sum(x[:3]).reshape(1), np.sum(x[3:]).reshape(1))),axis = 1,  result_type='expand')
    tmp.columns = columns
    return tmp

def comparingGroup(df, group, elem,ax):
    groups = set(df[group])
    n_group = len(groups)
    bratio = getBoutInfo(df, ['uid',group, elem])
    arrs = []
    for btype in ['b','p','w']:
        for is_group in groups:
            arrs.append(bratio.query(f'{group} == @is_group')[btype+'ratio'])
    
    ax.boxplot(x = arrs, positions=[*np.arange(n_group),*(np.arange(n_group)+n_group+1), *(np.arange(n_group)+2*n_group+2)], showfliers= False)
    ax.set_xticks([(n_group-1)/2, n_group*3/2 + 1/2, n_group*5/2 +3/2])
    ax.set_xticklabels(['Both','Phone','Watch'])
    for idx, btype in enumerate(['both','phone','watch']):
        F, pVal = stats.f_oneway(*arrs[idx*n_group:(idx+1)*n_group])
        print(f'{btype} ratio shows F: {F}, pVal: {"{:.3f}".format(pVal)}')