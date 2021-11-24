import numpy as np
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

cwd = os.getcwd()
tmp_dir = os.path.join(cwd, "tmp")
data_dir = os.path.join(cwd, "Data")


df = pd.read_csv(os.path.join(data_dir,"bout.csv"), index_col = 0, header = 0)
user_day = {}
for user in set(df["users"]):
    user_day[user] = len(set(pd.to_datetime(df["first"]).dt.date))

dfw = pd.read_csv(os.path.join(tmp_dir,"wearing.csv"), index_col = 0, header = 0)
dfw["first"] = pd.to_datetime(dfw["first"])
dfw["last"] = pd.to_datetime(dfw["last"])
dfw["date"] = dfw["first"].dt.date

dfc = pd.read_csv(os.path.join(tmp_dir,"carrying.csv"), index_col = 0, header = 0)
dfc["first"] = pd.to_datetime(dfc["first"])
dfc["last"] = pd.to_datetime(dfc["last"])
dfc["date"] = dfc["first"].dt.date
users = set(dfw["users"])
for user in users:
    user = 4
    date = pd.DataFrame(columns=["count"], index=pd.date_range(start="2021-11-11", periods = 24*60, freq = 'T'))
    date.index = [idx.time() for idx in date.index]
    date["count"] = np.zeros(24*60)
    tmp = dfw.query(f"users == {user}")
    # tmp = tmp[tmp['date'] == dt.date(2021, 7,15)]
    # print(dfw.query(f"users == {user}")['date'== dt.date(2021, 7,15)])
    for idx, row in tmp.iterrows():
        for time in pd.date_range(start =row["first"], end= row["last"], freq = 'T')[:-1]:
            date.loc[time.time(),'count'] += 1
    # 300 represents number of points to make between T.min and T.max
    data = np.array(date['count'])/user_day[user]

    fig, ax = plt.subplots(nrows = 1, ncols= 1, figsize= (6,3))
    plt.plot(data,label = "wearing")
    old = data
    date = pd.DataFrame(columns=["count"], index=pd.date_range(start="2021-11-11", periods = 24*60, freq = 'T'))
    date.index = [idx.time() for idx in date.index]
    date["count"] = np.zeros(24*60)
    tmp = dfc.query(f"users == {user}")
    for idx, row in tmp.iterrows():
        for time in pd.date_range(start =row["first"], end= row["last"], freq = 'T')[:-1]:
            date.loc[time.time(),'count'] += 1
    data = np.array(date['count'])/user_day[user]
    plt.plot(data,label = "carrying")

    plt.xticks(ticks= list(range(0, 24*60, 60)), labels= list(range(0, 24)))
    # plt.ylim([0,1])
    plt.legend()
    plt.savefig(os.path.join(cwd,"T",f"time_dist.png"))
    plt.close()
    break
