import os,shutil
import datetime as dt
import pandas as pd
import glob
import numpy as np
import json

if not os.path.exists("Preprocess"):
    os.mkdir("Preprocess")
else:
    shutil.rmtree("Preprocess")
    os.mkdir("Preprocess")
cols ={'C':'run_step','D': 'walk_step','E':'timestamp','J':'count','K':'speed','L':'distance','M':'calorie','O':'uuid'}
for idx, folder in enumerate(sorted(os.listdir("Datas"))):
    try:
        raw = pd.read_csv(glob.glob(f"Datas/{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv", recursive= True)[0], 
                          skiprows=[0], 
                          usecols =[ord(key)-ord('A') for key in cols.keys()], 
                          header= 0, 
                          names = cols.values())
        device_profile = pd.read_csv(glob.glob(f"Datas/{folder}/**/com.samsung.health.device_profile.*.csv", recursive= True)[0],
                                     skiprows=[0], usecols = [ord("G")-ord("A"),ord("M")-ord("A")],
                                     header= 0, 
                                     names = ["device_group","uuid"])
        # device group에서 360003은 companion or wearable, 360001은 mobile device
        mobile = device_profile.query("device_group == 360001")["uuid"].values
        wearable = device_profile.query("device_group == 360003")["uuid"].values
        
        raw["device"] = ["watch" if row["uuid"] in wearable else "phone" for _, row in raw.iterrows()]
        # Timestamp가 UTC+000으로 UTC+900으로 변환 작업
        raw["timestamp"] = [dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")  + dt.timedelta(hours = 9) for timestamp in raw["timestamp"]]
        raw.sort_values(["timestamp", "device"], inplace = True)
        raw.reset_index(drop = True, inplace = True)
        # 시작일과 끝일의 경우, 24시간이 기록되지 않았으므로 제거
        start = raw.iloc[0]["timestamp"].date()
        end = raw.iloc[-1]["timestamp"].date()
        raw = raw.query(f"'{start}'< timestamp and timestamp < '{end}'")
        # raw.reset_index(drop = True, inplace = True)
        raw.to_csv(f"Preprocess/{str(idx).zfill(4)}.csv")
        print(f"[{folder}] is done")
    except Exception as e:
        print(f"[{folder}]: {e}")
