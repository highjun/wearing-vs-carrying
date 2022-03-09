from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()

total_diff = np.sum(np.abs(df['pstep'] - df['wstep']))

threshold = .95
boutdf = getBoutInfo(df, ['uid','date','weekday']).reset_index()
singlep = boutdf.query("pstep_ratio > @threshold")
singlew = boutdf.query("wstep_ratio > @threshold")

print("Phone Single Day difference: {:.3f} users: {}, days:{}".format(np.sum(singlep['pstep'])/total_diff, len(set(singlep['uid'])), singlep.shape[0]))
print(singlep[['uid','date']])
print("Weekend: {}({})".format(singlep.query("weekday >= 5").shape[0], singlep[['pstep','weekday']].groupby('weekday').count().to_numpy()/singlep.shape[0]))


print("Watch Single Day difference: {:.3f} users: {}, days:{}".format(np.sum(singlew['wstep'])/total_diff, len(set(singlew['uid'])), singlew.shape[0]))
print("Weekend: {}({})".format(singlew.query("weekday >= 5").shape[0],  singlew[['wstep','weekday']].groupby('weekday').count().to_numpy()/singlep.shape[0]))
print(singlew[['uid','date','weekday','wstep','wcount']])



