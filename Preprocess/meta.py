from util import *

cwd = os.getcwd()
src = os.path.join(cwd, "Raws")
target = os.path.join(cwd, "Data")

dics = []
for idx, folder in enumerate(sorted(os.listdir(src))):
    dic = {}
    valid = True
    try:
        csvs =  glob.glob(os.path.join(src,folder,f"**/com.samsung.shealth.tracker.pedometer_step_count.*.csv",),recursive=True,)
        typeB = False
        if len(csvs) == 0:
            csvs += glob.glob(os.path.join(src,folder,f"**/com.samsung.health.step_count.*.csv",),recursive=True,)
            typeB = True
        raw = pd.read_csv(
                csvs[0],
                skiprows=[0],
                index_col= False,
                header=0,
        )
        used = list(raw['com.samsung.health.step_count.deviceuuid' if not typeB else 'deviceuuid'].unique())
        # device profile의 uuid와 Device_group을 통해서 wearable과 Mobile 분류
        device_profile = pd.read_csv(
            glob.glob(
                os.path.join(
                    src, folder, f"**/com.samsung.health.device_profile.*.csv"
                ),
                recursive=True,
            )[0],
            skiprows=[0],
            header=0,
            index_col= False,
        )
        device_profile = device_profile.query("deviceuuid in @used")
        wearable = set(device_profile.query("device_group == 360003")['name'].values)
        mobile = set(device_profile.query("device_group == 360001")['model'].values)
        dic['Wearable'] =  ', '.join(wearable)
        dic['Smartphone'] =  ', '.join(mobile)
        dic['typeB'] = typeB
        if len(wearable) == 0 or len(mobile) == 0:
            valid = False
            raise Exception("No device found for wearable or mobile")
    except Exception as e:
        print(f"Error in {folder}: {e}")
        valid = False
    dic['UID'] =  folder
    dic['VALID'] = valid    
    dics.append(dic)
meta = pd.DataFrame(dics)
meta.to_csv(os.path.join(target,"meta.csv"), index = False)