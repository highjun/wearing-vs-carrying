from util import pd, os, data_dir, user_dir
all_users = []
for uid, csv in enumerate(sorted(os.listdir(user_dir))):
    data = pd.read_csv(os.path.join(user_dir,csv),
                    index_col= 0, header = 0, encoding = 'utf-8')
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(['timestamp','device'], inplace= True)
    data.reset_index(inplace= True)
    data['uid'] = [csv.split('.')[0]]*data.shape[0]
    all_users.append(data)
all_users = pd.concat(all_users, ignore_index= True)
all_users.to_csv(os.path.join(data_dir,'integrate.csv'), index= False)