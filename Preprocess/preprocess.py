from util import *

cwd = os.getcwd()
raw_dir = os.path.join(cwd, "Raws")
preprocess_dir = os.path.join(cwd, "Data/Users")

for idx, folder in enumerate(sorted(os.listdir(raw_dir))):
    try:
        if len(glob.glob(os.path.join(raw_dir, f"{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv"), recursive= True)) != 0:
            raw = pd.read_csv(
                glob.glob(
                    os.path.join(
                        raw_dir,
                        f"{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv",
                    ),
                    recursive=True,
                )[0],
                skiprows=[0],
                usecols=[
                    ord("C") - ord("A"),
                    ord("D") - ord("A"),
                    ord("E") - ord("A"),
                    ord("J") - ord("A"),
                    10,
                    11,
                    12,
                    ord("O") - ord("A"),
                ],
                header=0,
                names=[
                    "run",
                    "walk",
                    "timestamp",
                    "step",
                    "speed",
                    "distance",
                    "calorie",
                    "uuid",
                ],
            )
            # Timestamp was logged as UTC+000, so convert it to UTC+900, also it was loaded as string, so convert to datetime object
            raw["timestamp"] = [
                timestamp + dt.timedelta(hours=9)
                for timestamp in pd.to_datetime(raw["timestamp"], format="%Y-%m-%d %H:%M")
            ]
            # device profile의 uuid와 Device_group을 통해서 wearable과 Mobile 분류
            device_profile = pd.read_csv(
                glob.glob(
                    os.path.join(
                        raw_dir, f"{folder}/**/com.samsung.health.device_profile.*.csv"
                    ),
                    recursive=True,
                )[0],
                skiprows=[0],
                usecols=[ord("G") - ord("A"), ord("M") - ord("A")],
                header=0,
                names=["device_group", "uuid"],
            )
        else:
            raise Exception("No Step count folder exist")
        
        wearable = list(device_profile.query("device_group == 360003")["uuid"].values)
        mobile = list(device_profile.query("device_group == 360001")["uuid"].values)
        raw["device"] = [
            "watch" if str(uuid) in wearable else "phone" for uuid in raw['uuid'].to_numpy()
        ]
        # sort by timestamp and device
        raw.sort_values(["timestamp", "device"], inplace=True)
        raw = raw.groupby(["timestamp", "device", "uuid"]).sum()
        raw.reset_index(inplace=True)
        raw["hour"] = raw["timestamp"].dt.hour
        raw["date"] = raw["timestamp"].dt.date
        raw["weekday"] = raw["timestamp"].dt.weekday
        start = raw.iloc[0]["date"]
        end = raw.iloc[-1]["date"]
        raw = raw[(raw["date"] > start) & (raw["date"] < end)]
        raw.reset_index(drop=True, inplace=True)
        raw.to_csv(os.path.join(preprocess_dir, f"{folder}.csv"), encoding="utf-8")
        print(f"{folder} preprocessed")
    except Exception as e:
        print(f"Error in {folder}: {e}")