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
df["first"] = pd.to_datetime(df["first"])
df["last"] = pd.to_datetime(df["last"])

user_day = {}
for user in set(df["users"]):
    user_day[user] = len(set(pd.to_datetime(df["first"]).dt.date))
user = 10
df = df.query(f"users == {user}")
# df = df.query("bout_type != 'p'")
fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize = (12,4))
for idx in range(20): 
    if (dt.date(2021,7,15)+dt.timedelta(days=idx)).weekday() < 5:
        df_ = df.query("bout_type != 'p'")[df["first"].dt.date == dt.date(2021,7,15)+dt.timedelta(days=idx)]
        yes = np.zeros(24)
        for _, row in df_.iterrows():
            for h in range(row["first"].hour, row['last'].hour+1):
                yes[h] += 1
        ax[0].plot(np.arange(24), (np.array([yes != 0])*(idx+1)).reshape(-1), '.',label = str(dt.date(2021,7,15)+dt.timedelta(days=idx)))
        
        df_ = df.query("bout_type !='w'")[df["first"].dt.date == dt.date(2021,7,15)+dt.timedelta(days=idx)]
        yes = np.zeros(24)
        for _, row in df_.iterrows():
            for h in range(row["first"].hour, row['last'].hour+1):
                yes[h] += 1
        ax[1].plot(np.arange(24), (np.array([yes != 0])*(idx+1)).reshape(-1), '.',label = str(dt.date(2021,7,15)+dt.timedelta(days=idx)))

        df_ = df[df["first"].dt.date == dt.date(2021,7,15)+dt.timedelta(days=idx)]
        yes = np.zeros(24)
        for _, row in df_.iterrows():
            for h in range(row["first"].hour, row['last'].hour+1):
                yes[h] += 1
        ax[2].plot(np.arange(24), (np.array([yes != 0])*(idx+1)).reshape(-1), '.',label = str(dt.date(2021,7,15)+dt.timedelta(days=idx)))
# plt.legend()
plt.savefig("tmp.png")
