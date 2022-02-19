from util import *

# cwd = os.getcwd()
# raw_dir = os.path.join(cwd, "Raws")
# raws = []
# for idx, folder in enumerate(sorted(os.listdir(raw_dir))):
#     try:
#         if len(glob.glob(os.path.join(raw_dir, f"{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv"), recursive= True)) != 0:
#             used = pd.read_csv(
#                 glob.glob(
#                     os.path.join(
#                         raw_dir,
#                         f"{folder}/**/com.samsung.shealth.tracker.pedometer_step_count.*.csv",
#                     ),
#                     recursive=True,
#                 )[0],
#                 skiprows=[0],
#                 header=0,
#                 index_col = False
#             )
#             used = list(set(used['com.samsung.health.step_count.deviceuuid']))
#         else:
#             used = pd.read_csv(
#                 glob.glob(
#                     os.path.join(
#                         raw_dir,
#                         f"{folder}/**/com.samsung.health.step_count.*.csv",
#                     ),
#                     recursive=True,
#                 )[0],
#                 skiprows=[0],
#                 header=0,
#                 index_col = False
#             )
#             used = list(set(used['deviceuuid']))
        
#         raw = pd.read_csv(
#             glob.glob(
#                 os.path.join(
#                     raw_dir,
#                     f"{folder}/**/com.samsung.health.device_profile.*.csv",
#                 ),
#                 recursive=True,
#             )[0],
#             skiprows=[0],
#             header= 0,
#             index_col= False
#         )
#         raw['device_name'] = [model if name == 'My Device' else name for name, model in raw[['name','model']].to_numpy()]
#         raw['device_group'] = ['smartphone' if val == 360001 else 'wearable' for val in raw['device_group'].to_numpy()]
#         # print(raw)
#         # break
#         raw['uid'] = folder
#         raw = raw.query("deviceuuid in @used")[['uid', 'device_group','device_name', 'deviceuuid']]
#         raws.append(raw)
#     except Exception as e:
#         print(f"Error in {folder}: {e}")
#     # break
# devices = pd.concat(raws, ignore_index= True)
# devices.to_csv("Device.csv", index  = False)

# def listed(x):
#     return ', '.join(list(set(x)))


# devices = devices.groupby(['uid','device_group']).agg(cnt = ('device_name',listed))
# devices = devices.unstack(level = 1)
# devices.columns = ['Smartphone', 'Wearable']
# # devices = devices.groupby(['uid','device_group']).agg(cnt = ('device_name','count')).reset_index()
# # devices = devices.groupby(['uid']).agg(cnt = ('device_group','count'))
# # print(devices.shape[0])
# # print(devices.query('cnt == 1').index)
# # print(devices.query('cnt == 2').shape[0])
# devices.to_csv("Stat.csv")

survey = pd.read_csv("survey.csv", index_col = False, header = 0, encoding = "euc-kr")
device = pd.read_csv("Stat.csv", index_col = False, header = 0)

total =pd.concat([survey.set_index('UID'), device.set_index('UID')], axis = 1).reset_index()
total = total[['UID','VER','VALID', 'Age', 'Gender','Smartphone', 'Wearable', 'Q1','Q2.1','Q2.2','Q2.3','Q2.4', 'Q3','Q3.1','Q3.2','Q3.3','Q3.4','Q4','Q5','Q6','Q7','Q8','Q9','Q10']]
total.to_csv("total.csv", encoding = "utf-8", index = False)