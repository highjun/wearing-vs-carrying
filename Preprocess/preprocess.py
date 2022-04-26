import shutil
from util import *
from tqdm import tqdm

cwd = os.getcwd()
raw_dir = os.path.join(cwd, "Raws")
data_dir = os.path.join(cwd, "Data")
target = os.path.join(data_dir, "Users")
if os.path.exists(target):
    shutil.rmtree(target)
os.makedirs(target)
errors = []
meta = pd.read_csv(os.path.join(data_dir, "meta.csv"), index_col= False)
uids = sorted(meta.query("VALID == True")['UID'].values)
for folder in tqdm(uids):
    try:
        csvs = glob.glob(os.path.join(raw_dir, f"{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv"), recursive= True)
        meta_csv = glob.glob(os.path.join(raw_dir, f"{folder}/**/com.samsung.health.device_profile.*.csv"),recursive=True,)[0]
        if len(csvs) != 0:
            raw = pd.read_csv(csvs[0],
                skiprows=[0],
                index_col = False,
                header = 0
            )
            raw.columns = [col.split('.')[-1] for col in raw.columns]
            # Timestamp was logged as UTC+000, so convert it to UTC+900, also it was loaded as string, so convert to datetime object
            raw["timestamp"] = [
                timestamp + dt.timedelta(hours=9)
                for timestamp in pd.to_datetime(raw["start_time"], format="%Y-%m-%d %H:%M")
            ]
        else:
            csvs = glob.glob(os.path.join(raw_dir, folder, f"**/com.samsung.health.step_count.*.csv"), recursive= True)
            if len(csvs) != 0:
                raw = pd.read_csv(csvs[0],
                    skiprows = [0],
                    header = 0,
                    index_col= False,
                )
                ts =[] 
                for timestamp in raw['start_time']:
                    if '오후' in timestamp:
                        timestamp = ''.join(timestamp.split("오후"))
                        tmp = dt.datetime.strptime(timestamp,"%Y. %m. %d.  %I:%M:%S")
                        tmp += dt.timedelta(hours = 21)
                        ts.append(tmp)
                    elif '오전' in timestamp:
                        timestamp = ''.join(timestamp.split("오전"))
                        tmp = dt.datetime.strptime(timestamp,"%Y. %m. %d.  %I:%M:%S")
                        tmp += dt.timedelta(hours = 9)
                        ts.append(tmp)
                    else:
                        tmp = dt.datetime.strptime(timestamp,"%Y. %m. %d. %H:%M:%S")
                        tmp += dt.timedelta(hours = 9)
                        ts.append(tmp)
                raw['timestamp'] = ts
            else:
                raise Exception("No Step count folder exist")
        # device profile의 uuid와 Device_group을 통해서 wearable과 Mobile 분류
        device_profile = pd.read_csv(meta_csv,
            skiprows=[0],
            index_col= False,
            header=0,
        )
        wearable = list(device_profile.query("device_group == 360003")["deviceuuid"].values)
        mobile = list(device_profile.query("device_group == 360001")["deviceuuid"].values)
        raw["device"] = [
            "watch" if str(uuid) in wearable else "phone" for uuid in raw['deviceuuid'].to_numpy()
        ]
        raw.rename({'count': 'step'},axis = 1, inplace= True)
        # sort by timestamp and device
        raw.sort_values(["timestamp", "device"], inplace=True)
        raw = raw.groupby(["timestamp", "device","deviceuuid"]).sum()
        raw.reset_index(inplace=True)
        raw = raw.groupby(["timestamp", "device"]).mean()
        raw.reset_index(inplace=True)
        
        raw["hour"] = raw["timestamp"].dt.hour
        raw["date"] = raw["timestamp"].dt.date
        raw["weekday"] = raw["timestamp"].dt.weekday
        start = raw.iloc[0]["date"]
        end = raw.iloc[-1]["date"]
        raw = raw[(raw["date"] > start) & (raw["date"] < end)]
        raw.reset_index(drop=True, inplace=True)
        raw[['timestamp', 'step','device']].to_csv(os.path.join(target, f"{folder}.csv"), encoding="utf-8")
    except Exception as e:
        errors.append(f"Error in {folder}: {e}")
for error in errors:
    print(error)