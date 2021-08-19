import os,shutil
import datetime as dt
import pandas as pd
import glob
import numpy as np
import json

metadata = {}

detected_by_enum = ["none", "watch", "phone", "both"]

all_users = []
if not os.path.exists("Preprocess"):
    os.mkdir("Preprocess")
else:
    shutil.rmtree("Preprocess")
    os.mkdir("Preprocess")

for idx, folder in enumerate(sorted(os.listdir("Raws"))):
    raw = pd.read_csv(glob.glob(f"Raws/{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv", recursive= True)[0],
                                        skiprows=[0,1], usecols = [0,2,3,4,5,9,10,11,12], header= 0, 
                                        names = ["duration", "run", "walk", "timestamp", "device", "step", "speed", "distance", "calorie"])
    # device can be identified by its logging position, but for fir duration being na
    raw["device"] = ["watch" if (row["device"] == 230002 or row["duration"] != row["duration"]) else "phone" for _, row in raw.iterrows()]
    # sort by timestamp and device
    raw.sort_values(["timestamp", "device"], inplace = True)
    raw = raw.fillna(0)
    # Timestamp was logged as UTC+000, so convert it to UTC+900, also it was loaded as string, so convert to datetime object
    raw["timestamp"] = [ timestamp  + dt.timedelta(hours = 9) for timestamp in pd.to_datetime(raw["timestamp"], format="%Y-%m-%d %H:%M")]
    start = raw.iloc[0]["timestamp"] 
    end = raw.iloc[-1]["timestamp"]  
    def total_day(x):
            x = set([i.date() for i in x])
            return len(x)
    raw.insert(0, "day", [(timestamp.date()- start.date()).days for timestamp in raw["timestamp"]])
    raw = raw.query(f"day != 0 and day != {(end.date()-start.date()).days}")
    total = raw.groupby("device").agg(days = ("timestamp",total_day))
    # Log metadata for each participants
    metadata[idx] = {"start": (start.date() + dt.timedelta(days=1)).strftime('%Y-%m-%d'), "end": (end.date() -  dt.timedelta(days=1)).strftime('%Y-%m-%d'), "folder": folder, "phone_day": int(total["days"][0]) ,"watch_day": int(total["days"][1]), 'total': int((end.date()-start.date()).days-1)}
    # raw["date"] = [i.date() for i in raw["timestamp"]]
    # raw.insert(0, "day", [(timestamp.date()- start.date()).days for timestamp in raw["timestamp"]])
    # raw = raw.query(f"day != 0 and day != {(end.date()-start.date()).days}")
    #phone
    act_idx = -1
    last = None
    phone_acts = []
    for _, row in raw.iterrows():
        if row["device"] == 'phone':
            if last is None:
                last = row["timestamp"] 
                act_idx = 1
                phone_acts.append(act_idx)
            else:
                if (row["timestamp"] - last).days == 0 and (row["timestamp"] - last).seconds == 60:
                    phone_acts.append(act_idx)
                    last = row["timestamp"]
                else:
                    act_idx += 1
                    phone_acts.append(act_idx)
                    last = row["timestamp"]
        else:
            phone_acts.append(0)
    #watch
    act_idx = -1
    last = None
    watch_acts = []
    for _, row in raw.iterrows():
        if row["device"] == 'watch':
            if last is None:
                last = row["timestamp"] 
                act_idx = 1
                watch_acts.append(act_idx)
            else:
                if (row["timestamp"] - last).days == 0 and (row["timestamp"] - last).seconds == 60:
                    watch_acts.append(act_idx)
                    last = row["timestamp"]
                else:
                    act_idx += 1
                    watch_acts.append(act_idx)
                    last = row["timestamp"]
        else:
            watch_acts.append(0)
    #both
    act_idx = -1
    last = None
    both_acts = []
    for _, row in raw.iterrows():
        if last is None:
            last = row["timestamp"] 
            act_idx = 1
            both_acts.append(act_idx)
        else:
            if (row["timestamp"] - last).days == 0 and ((row["timestamp"] - last).seconds == 60 or (row["timestamp"]-last).seconds == 0):
                both_acts.append(act_idx)
                last = row["timestamp"]
            else:
                act_idx += 1
                both_acts.append(act_idx)
                last = row["timestamp"]
    
    raw.insert(0, "phone_chunk_idx", phone_acts)
    raw.insert(0, "watch_chunk_idx", watch_acts)
    raw.insert(0, "both_chunk_idx", both_acts)

    raw.insert(0, "weekday", [timestamp.weekday() for timestamp in raw["timestamp"]])
    raw.insert(0, "hour", [timestamp.hour for timestamp in raw["timestamp"]])
    raw.fillna(0, inplace = True)
    raw.reset_index(drop = True, inplace = True)
    raw.to_excel(f"Preprocess/{idx}.xlsx")
    all_users.append(raw)
    print(f"{folder} is done")

all = pd.concat(all_users, keys = list(range(len(all_users))))
all["user"] = all.index.get_level_values(0)
all.reset_index(drop = True, inplace = True)
all.to_excel(f"Preprocess/all_user.xlsx")
with open("meta_data.json", 'w') as outfile:
    json.dump(metadata, outfile)
