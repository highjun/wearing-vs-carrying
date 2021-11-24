import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#A는 carrying을 W or B 이후 최초의 W 1분 전까지로 본다.
#B는 carrying을 W or B 이후 최초의 W가 나오기 전 마지막 W or B까지로 본다.
space_type = "B"

cwd = os.getcwd()
data_dir = os.path.join(cwd,"Data")


df = pd.read_csv(os.path.join(data_dir,"bout.csv"), index_col = 0, header = 0)
df["first"] = pd.to_datetime(df["first"])
df["last"] = pd.to_datetime(df["last"])
users = set(df["users"])
if space_type =="A":
    carrying = pd.DataFrame(columns=["users", "first", "last"])
    add = {}
    for user in users:
        add["users"] = user
        tmp = df.query(f"users =={user}")
        for idx, row in tmp.iterrows():
            if row['bout_type'] != 'w':
                if 'first' not in add.keys():
                    add['first'] = row['first']
            else:
                if 'first' in add.keys():
                    add['last'] = row['first']
                    carrying = carrying.append(add, ignore_index= True)   
                    add = {'users': user}
    carrying.to_csv(os.path.join(cwd,"tmp","carrying.csv"))
if space_type =="B":
    carrying = pd.DataFrame(columns=["users", "first", "last"])
    add = {}
    for user in users:
        add["users"] = user
        tmp = df.query(f"users =={user}")
        for idx, row in tmp.iterrows():
            if row['bout_type'] != 'w':
                if 'first' not in add.keys():
                    add['first'] = row['first']
                add['last'] = row['last']
            else:
                if 'first' in add.keys():
                    carrying = carrying.append(add, ignore_index= True)   
                    add = {'users': user}
    carrying.to_csv(os.path.join(cwd,"tmp","carrying.csv"))
