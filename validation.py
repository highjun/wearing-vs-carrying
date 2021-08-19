#Validate the data from participants
import zipfile
import glob
import os
import pandas as pd
import datetime as dt
import numpy as np

path_to_zip = "./Zips"
path_to_raw = "./Raws"

ids ={}
all_uuid = ["VfS0qUERdZ", "Mk66SbFqK1"]


# for zip_file in sorted(glob.glob(f"{path_to_zip}/*.zip")):
#     print(zip_file)
#     with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#         zip_ref.extractall(f"{path_to_raw}/{os.path.basename(zip_file)}")

n_failed = 0
n_total = len(glob.glob(f"{path_to_raw}/*"))
for idx, folder in enumerate(sorted(glob.glob("Raws/*"))):
    try:
        uuids = pd.read_csv(glob.glob(f"{folder}/**/com.samsung.health.device_profile.*.csv", recursive= True)[0],
                        skiprows = [0,1], usecols = [12], header = 0, names=["device"])["device"]
        for uuid in uuids:
            if uuid in ids.keys():
                raise Exception(f"{folder} and {ids[uuid]} is repeated")
            elif uuid not in all_uuid:
                ids[uuid] = folder
        raw = pd.read_csv(glob.glob(f"{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv", recursive= True)[0],
                                        skiprows=[0,1], usecols = [0,2,3,4,5,9,10,11,12], header= 0, 
                                        names = ["duration", "run", "walk", "timestamp", "device", "step", "speed", "distance", "calorie"])
        raw["device"] = ["watch" if (row["device"] == 230002 or row["duration"] != row["duration"]) else "phone" for _, row in raw.iterrows()]
        raw["timestamp"] = [ timestamp  + dt.timedelta(hours = 9) for timestamp in pd.to_datetime(raw["timestamp"], format="%Y-%m-%d %H:%M")]
        raw.sort_values(["timestamp", "device"], inplace = True)
        start = raw.iloc[0]["timestamp"] 
        end = raw.iloc[-1]["timestamp"]

        diff = (end.date() - start.date()).days -1
        def total_day(x):
            x = set([i.date() for i in x])
            return len(x)
        total = raw.groupby("device").agg(days = ("timestamp",total_day))
        total.sort_values("days", inplace = True, ascending = False)
        if len(total.index) <2:
            raise Exception(f"{total.index[0]}만 검색되었습니다.")
        if diff <30:
            raise Exception(f"데이터의 일 수가 30일보다 적습니다.")
        if (total["days"][0]-2)/diff <3/7 or (total["days"][1]-2)/diff <3/7:
            raise Exception(f"Too less days: {total['days'][0]-2}, {total['days'][1]-2} for {start.date()} ~ {end.date()}:{diff}")
    except Exception as e:
        print(f"{folder}는 {e.args[0]}")
        n_failed += 1 
print(f"총 {n_total}개의 데이터 중 {n_failed}는 실패했습니다.")
