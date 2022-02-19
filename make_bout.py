from util import data_dir, os, pd, np

data_path  = os.path.join(data_dir, 'integrate.csv')
df = pd.read_csv(data_path, index_col= False, header = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])

features = ['step','distance','speed','calorie','run','walk']
btypes = ['phone','watch']
df = df.set_index(['uid', 'timestamp','device'])[features]
df  =df.unstack(level = 2)
df = df.reset_index()
columns =['uid','timestamp']
for feature in features:
    for btype in btypes: 
        columns.append(btype+ '_' + feature)
df.columns = columns
df.sort_values(["uid","timestamp"], inplace= True)

threshold = 1
bidx = []
for user in sorted(set(df['uid'])):
    udf = df.query(f"uid == @user")
    diff = udf['timestamp'].diff().dt.total_seconds()//60
    diff = np.array([1 if val > threshold else 0 for val in diff])
    bidx += list(diff.cumsum())
df['bidx'] = bidx # bout idx

for feature in features:
    df[feature] = df[['phone_'+feature, 'watch_'+feature]].mean(axis = 1)

summable = ['step', 'distance', 'run', 'walk', 'calorie']
meanable = ['speed']
dict = {'first':('timestamp','first'), 'last':('timestamp','last')}
for feature in features:
    for prefix in ['watch_','phone_','']:
        dict[(prefix[0] if prefix != '' else '')+feature] = (prefix + feature,'sum' if feature in summable else 'mean')
df =df.groupby(['uid','bidx']).agg(**dict).reset_index()

df['btype'] = ['b' if val[0] > 0 and val[1]> 0 else ('p' if val[0]> 0 else 'w') for val in df[['pstep','wstep']].to_numpy()] 
df['hour'] = df['first'].dt.hour
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = (df[['first','last']].diff(axis = 1)['last'].dt.total_seconds()//60) + 1

df.to_csv(os.path.join(data_dir,'bout.csv'))