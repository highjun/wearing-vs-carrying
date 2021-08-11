import os,shutil
import datetime as dt
import pandas as pd
import glob
import json

with open("./setting.json") as f:
    setting = json.load(f)
detected_by_enum = ["none", "watch", "phone", "both"]


if not os.path.exists("Preprocess"):
    os.mkdir("Preprocess")
else:
    shutil.rmtree("Preprocess")
    os.mkdir("Preprocess")

for id in os.listdir("Raw"):
    start = dt.datetime.strptime(setting[id][0], '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(setting[id][1], '%Y-%m-%d %H:%M')
    raw_data = pd.read_csv(glob.glob(f"Raw/{id}/com.samsung.shealth.tracker.pedometer_step_count.*.csv")[0],
                                        skiprows=[0,1], usecols = [0,2,3,4,5,9,10,11,12], header= 0, 
                                        names = ["duration", "run", "walk", "timestamp", "device", "step", "speed", "distance", "calorie"]).fillna(0)
    # device can be identified by its logging position, 230002 means device is in the wrist.
    raw_data["device"].replace(to_replace = 230002, value = "watch", inplace = True)
    raw_data["device"].replace(to_replace = 0,value= "phone", inplace = True)
    # sort by timestamp and device
    raw_data.sort_values(["timestamp", "device"], inplace = True)
    # Timestamp was logged as UTC+000, so convert it to UTC+900, also it was loaded as string, so convert to datetime object
    raw_data["timestamp"] = [ timestamp  + dt.timedelta(hours = 9) for timestamp in pd.to_datetime(raw_data["timestamp"], format="%Y-%m-%d %H:%M")]
    # For each timestamp, add a row if not exist for watch and phone.
    raw_data=raw_data.set_index(["timestamp","device"]).reindex(pd.MultiIndex.from_product([pd.date_range(start = start, end = end, freq = '1Min'), ["phone","watch"]], names= ["timestamp", "device"])).reset_index().fillna(0)
    
    # Preprocess Activity as chunk
    act_idx1 = 0 #phone
    act_idx2 = 0 #watch
    act_idx3 = 0 #combined
    phone_act_idx = []
    watch_act_idx = []
    comb_act_idx = []
    phone_detected = False
    watch_detected = False
    detected_by = []
    comb_dut = 0
    for idx in range(0,raw_data.shape[0], 2):
        n_phone_step = raw_data.iloc[idx]["step"]
        n_watch_step = raw_data.iloc[idx+1]["step"]
        n_combined_step = n_phone_step + n_watch_step
        if n_phone_step > 0:
            if idx >= 2 and raw_data.iloc[idx-2]["step"] >0:
                phone_act_idx += [act_idx1,act_idx1]
            else:
                act_idx1 += 1
                phone_act_idx += [act_idx1, act_idx1]
        else:
            phone_act_idx += [0, 0]
        if n_watch_step > 0:
            if idx >= 1 and raw_data.iloc[idx-1]["step"] >0:
                watch_act_idx += [act_idx2, act_idx2]
            else:
                act_idx2 += 1
                watch_act_idx += [act_idx2, act_idx2]
        else:
            watch_act_idx += [0, 0]
        if n_combined_step > 0:
            if idx >= 2 and raw_data.iloc[idx-1]["step"]+raw_data.iloc[idx-2]["step"] >0:
                comb_dut += 1
                if n_phone_step>0:
                    phone_detected = True
                if n_watch_step>0:
                    watch_detected = True
                comb_act_idx += [act_idx3, act_idx3]
            else:
                comb_dut += 1
                act_idx3 += 1
                if n_phone_step>0:
                    phone_detected = True
                if n_watch_step>0:
                    watch_detected = True
                comb_act_idx += [act_idx3, act_idx3]
        else:
            if comb_dut > 0:
                idx_ = (2 if phone_detected else 0) + (1 if watch_detected else 0)
                detected_by += [detected_by_enum[idx_]]*2*comb_dut
                phone_detected = watch_detected = False
                comb_dut = 0
            comb_act_idx += [0, 0]
            detected_by += ["none","none"]
    if comb_dut > 0:
        idx_ = (2 if phone_detected else 0) + (1 if watch_detected else 0)
        detected_by += [detected_by_enum[idx_]]*2*comb_dut
        phone_detected = watch_detected = False
        comb_dut = 0
    raw_data.insert(0, "phone_act_idx", phone_act_idx)
    raw_data.insert(0, "watch_act_idx", watch_act_idx)
    raw_data.insert(0, "comb_act_idx", watch_act_idx)
    raw_data.insert(0, "by", detected_by)


    raw_data.insert(0, "weekday", [timestamp.weekday() for timestamp in raw_data["timestamp"]])
    raw_data.insert(0, "hour", [timestamp.hour for timestamp in raw_data["timestamp"]])
    raw_data.insert(0, "day", [(timestamp- start).days for timestamp in raw_data["timestamp"]])

    raw_data.to_excel(f"Preprocess/{id}.xlsx")
