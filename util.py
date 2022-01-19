import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy import stats

color = {'phone':'tab:blue', 'watch':'tab:orange', 'both':'tab:green'}
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('mode.chained_assignment',  None) 

def load_survey():
    df = pd.read_csv(os.path.join(os.getcwd(),"Data",'survey.csv'), header = 0)
    return df

def load_bout():
    df = pd.read_csv(os.path.join(os.getcwd(),"Data",'bout.csv'), header = 0)
    for val in ['first','last','date']:
        df[val] = pd.to_datetime(df[val])
    tmp = df.groupby(['uid','btype']).agg(step = ('step','sum'))
    tmp = tmp.unstack(level = 1, fill_value = 0)
    tmp = tmp.apply(lambda x: x/np.sum(x), axis = 1)
    tmp.columns = ['b','p','w']
    valid_user = list(tmp.query('b != 0').index)
    df = df.query(f"uid in @valid_user")
    return df

def getBoutRatio(df, normalize = True):
    if df.shape[0] == 0:
        return pd.DataFrame([],columns=['b','p','w'])
    tmp = df.groupby(["uid","btype"]).agg(step = ("step","sum"))
    tmp = tmp.reindex(pd.MultiIndex.from_product([list(set(df["uid"])), ['b','p','w']]), fill_value = 0)
    tmp = tmp.unstack(level=1, fill_value = 0)
    tmp.columns = ['b','p','w']
    if normalize:
        tmp = tmp.apply(lambda x: x/np.sum(x), axis = 1)
    return tmp

def getSortedUser(df):
    return sorted(list(set(df["uid"])), key = lambda x: getBoutRatio(df).loc[x]['b'], reverse = True)

def getTotalRatio(users,df):
    tmp = df.query(f"uid in @users")
    return [getBoutRatio(tmp)]

def getDayNightRatio(users, df):
    tmp = df.query(f"uid in @users")
    tmp['is_night'] = [1 if val >= 18 else 0 for val in tmp['hour']]
    return [getBoutRatio(tmp.query("is_night == @i")) for i in range(2)]

def getWeekendRatio(users, df):
    tmp = df.query(f"uid in @users")
    tmp['is_weekend'] = [1 if val >= 5 else 0 for val in tmp['hour']]
    return [getBoutRatio(tmp.query("is_weekend == @i")) for i in range(2)]

def getNotfUser():
    survey=load_survey()
    return [list(survey.query("notf == @i")["uid"]) for i in range(2)]


def getTrackUser():
    survey=load_survey()
    return [list(survey.query("track == @i")["uid"]) for i in range(2)]


def getAgeUser():
    survey = load_survey()
    survey["age_level"] = [0 if age<20 else (age//10 - 1 if age//10 <= 3 else 3) for age in survey["age"]]
    return [list(survey.query("age_level == @i")["uid"]) for i in range(4)]

def getGenderUser():
    survey = load_survey()
    return [list(survey.query("gender == @gender")['uid']) for gender in ["M","W"]]

def getActiveUser(df):
    low_th = 5000
    high_th = 8000
    tmp = df.groupby(["uid","date"]).agg(step = ("step", "sum"))
    tmp = tmp.reset_index().groupby(["uid"]).agg(step=("step","mean")).reset_index()
    tmp["level"] = [2 if step>= high_th else (1 if step>= low_th else 0) for step in tmp["step"]]
    return [list(tmp.query("level == @i")['uid']) for i in range(3)]

def getCarryingUser(t = 0):
    survey = load_survey()
    return [list(survey.query(f"w{t} == @btype")['uid']) for btype in ['b','p','w','n']]

def filterWearingDate(df, ret_wearing = True):
    tmp = df.groupby(["uid", "date","btype"]).agg(step = ("step","sum"))
    tmp = tmp.unstack(level=2, fill_value = 0)
    tmp.columns = ['b','p','w']
    tmp = tmp.apply(lambda x: x/np.sum(x),axis = 1)
    if ret_wearing:
        tmp = tmp.query("p < 0.95 and w < 0.95")
    else:
        tmp = tmp.query("p >= .95 or w >= .95 ")
    df_ = df.set_index(["uid","date"])
    df_ = df_[df_.index.isin(tmp.index)]
    df_ =df_.reset_index()
    return df_