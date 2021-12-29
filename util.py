import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy import stats

color = {'phone':'tab:blue', 'watch':'tab:orange', 'both':'tab:green'}
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def load_survey():
    df = pd.read_csv(os.path.join(os.getcwd(),"Data",'survey.csv'), header = 0)
    return df
def getSortedUser(df):
    return sorted(list(set(df["users"])), key = lambda x: getBoutRatio(df).loc[x]['b'], reverse = True)

def getBoutRatio(df, normalize = True):
    if df.shape[0] == 0:
        return pd.DataFrame([],columns=['b','p','w'])
    tmp = df.groupby(["users","bout_type"]).agg(step = ("step","sum"))
    tmp = tmp.reindex(pd.MultiIndex.from_product([list(set(df["users"])), ['b','p','w']]), fill_value = 0)
    tmp = tmp.unstack(level=1, fill_value = 0)
    tmp.columns = ['b','p','w']
    if normalize:
        tmp = tmp.apply(lambda x: x/np.sum(x), axis = 1)
    return tmp

# def filterNonWearingDate(df, drop= True):
#     tmp = df.groupby(["users", "date","bout_type"]).agg(step = ("step","sum"))
#     tmp = tmp.unstack(level=2, fill_value = 0)
#     tmp.columns = ['b','p','w']
#     tmp = tmp.apply(lambda x: x/np.sum(x),axis = 1)
#     if drop:
#         tmp = tmp.query("p < 0.95")
#     else:
#         tmp = tmp.query("p >= 0.95")
#     return df[df.apply(lambda x: (x["users"],x["date"]) in list(tmp.index),axis = 1)]

def load_bout():
    survey = load_survey()
    valid_user = list(set(survey.query("invalid != 1")["id"]))
    df = pd.read_csv(os.path.join(os.getcwd(),"Data",'bout.csv'), index_col=0, header = 0)
    users = getSortedUser(df)
    df = df.sort_values(by =["users"], key= lambda x: [users.index(user) for user in x.to_numpy()])
    df['first'] = pd.to_datetime(df['first'])
    df['last'] = pd.to_datetime(df['last'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.query(f"users in {valid_user}")
    return df

def getTotalRatio(users,df):
    tmp = df.query(f"users in {users}")
    return [getBoutRatio(tmp)]

def getWearingDayRatio(users,df):
    tmp = df.query(f"users in {users}")
    # if tmp.shape[0] == 0:
    #     return [pd.DataFrame([],columns=['b','p','w'])]
    # tmp = tmp.groupby(["users", "date","bout_type"]).agg(step = ("step","sum"))
    # tmp = tmp.unstack(level=2, fill_value = 0)
    # tmp.columns = ['b','p','w']
    # tmp = tmp.apply(lambda x: x/np.sum(x),axis = 1)
    tmp.insert(1,'wearing',[1 if p<0.95 else 0 for p in tmp['date_wearing_ratio']])
    tmp = tmp.groupby(["users","date"]).agg(wearing = ('wearing','first'))
    tmp = tmp.reset_index().groupby(["users"]).agg(wearing= ('wearing','mean'))
    return [tmp]

def getDayNightRatio(users, df):
    tmp = df.query(f"users in {users}")
    tmp = tmp.query("weekday < 5")
    # tmp['night'] = [1 if hour> 18 or hour < 9 else 0 for hour in tmp['hour']]
    # tmp = tmp.groupby(["users","night","bout_type"]).agg(step = ("step","sum"))
    # tmp = tmp.unstack(level=2, fill_value = 0)
    # tmp.columns = ['b','p','w']
    # tmp = tmp.apply(lambda x: x/np.sum(x),axis = 1)
    return [getBoutRatio(tmp.query("night == 0")), getBoutRatio(tmp.query("night == 1"))]

def getWeekendRatio(users, df):
    tmp = df.query(f"users in {users}")
    # tmp['weekend'] = [1 if weekday>=5 else 0 for weekday in tmp['weekday']]
    # tmp = tmp.groupby(["users","weekend","bout_type"]).agg(step = ("step","sum"))
    # tmp = tmp.unstack(level=2, fill_value = 0)
    # tmp.columns = ['b','p','w']
    # tmp = tmp.apply(lambda x: x/np.sum(x),axis = 1)
    return [getBoutRatio(tmp.query("weekend == 0")), getBoutRatio(tmp.query("weekend == 1"))]

def getRoutineRatio(users, df):
    tmp = df.query(f"users in {users}")
    tmp = tmp.query(f"weekday < 5")
    tmp_ = []
    for i in range(4):
        tmp_.append(getBoutRatio(tmp.query("routine == @i")))
    return tmp_

def getNotfUser():
    survey=load_survey()
    notf_user = list(survey.query("notf==1")["id"])
    not_notf_user = list(survey.query("notf==0")["id"])
    return [notf_user, not_notf_user]

def getTrackUser():
    survey=load_survey()
    track_user = list(survey.query("track==1")["id"])
    not_track_user = list(survey.query("track==0")["id"])
    return [track_user, not_track_user]

def getAgeUser():
    survey = load_survey()
    survey["age_level"] = [0 if age<20 else (age//10 - 1 if age//10 <= 3 else 3) for age in survey["age"]]
    users = []
    for i in range(4):
        users.append(list(survey.query("age_level == @i")["id"]))
    return users

def getGenderUser():
    survey = load_survey()
    man = list(survey.query("gender=='M'")["id"])
    woman = list(survey.query("gender == 'W'")["id"])
    return [man, woman]

def getActiveUser(df):
    low_th = 5000
    high_th = 8000
    tmp = df.groupby(["users","date"]).agg(step = ("step", "sum"))
    tmp = tmp.reset_index().groupby(["users"]).agg(step=("step","mean")).reset_index()
    tmp["level"] = [2 if step>= high_th else (1 if step>= low_th else 0) for step in tmp["step"]]
    users = []
    for i in range(3):
        users.append(list(tmp.query("level == @i")["users"]))
    return users

def getCarryingUser(t = 0):
    survey = load_survey()
    users = []
    for typ in ['b','p','w','n']:
        users.append(list(survey.query(f"w{t} == '{typ}'")['id']))
    return users