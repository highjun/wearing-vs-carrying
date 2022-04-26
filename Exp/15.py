from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()
df = df.reset_index()
total_diff = np.sum(np.abs(df['pstep'] - df['wstep']))
phone_diff = np.sum(df.query("btype == 'p'")['pstep'])
watch_diff = np.sum(df.query("btype == 'w'")['wstep'])
both_diff = np.sum(np.abs(df.query("btype=='b'")['pstep'] - df.query("btype=='b'")['wstep']))


# Single Device Day
threshold = .95
boutdf = getBoutInfo(df, ['uid','date'])
single = boutdf.query("pstep_ratio > @threshold or wstep_ratio > @threshold")
tmp = df.set_index(['uid','date'])
mask = tmp.index.isin(single.index)
single = tmp.loc[mask, 'index'].values

# Exercise Behavior
threshold= 100 
df['SPM'] = [step/duration for step, duration in df[['step','duration']].to_numpy()]
exercise = df.query("SPM > 125 or step > 3000")
exercise = exercise.query("btype != 'b'")
exercise = exercise['index']

#Single Timezone
df = loadDF()
df = df.reset_index()
threshold = .95
boutdf = getBoutInfo(df, ['uid','date'])
nonsingle = boutdf.query("not (pstep_ratio > @threshold or wstep_ratio > @threshold)")
tmp = df.set_index(['uid','date'])
mask = tmp.index.isin(nonsingle.index)
nonsingle = tmp.loc[mask, 'index'].values
timezone = getBoutInfo(df.query("index in @nonsingle"), ['uid','date','hour'])
timezone = timezone.query("wstep_ratio > @threshold or pstep_ratio > @threshold")
tmp = df.set_index(['uid','date','hour'])
mask = tmp.index.isin(timezone.index)
timezone = tmp.loc[mask, 'index'].values

def find(index):
    if index in single:
        return True
    if index in exercise:
        return True
    if index in timezone:
        return True
    return False
df['find'] = [find(index) for index in  df['index'].to_numpy()]

print("Total Differences")
print("Both: {:.3f}, Phone: {:.3f}, Watch: {:.3f}".format(both_diff/total_diff, phone_diff/total_diff, watch_diff/total_diff))

total = total_diff
print("Single Day")
phone = df.query("index in @single").query("btype == 'p'")
watch = df.query("index in @single").query("btype == 'w'")
print("Differences = Phone: {:.3f}, Watch: {:.3f}".format(np.sum(phone['pstep'])/total, np.sum(watch['wstep'])/total))
print("number of User =  Phone: {}, Watch: {}".format(len(set(phone['uid'])), len(set(watch['uid']))))
print("Freq =  Phone: {}, Watch: {}".format(phone.groupby(['uid','date']).sum().shape[0], watch.groupby(['uid','date']).sum().shape[0]))

print("Single Timezone")
phone = df.query("index in @timezone").query("btype == 'p'")
watch = df.query("index in @timezone").query("btype == 'w'")
print("Differences = Phone: {:.3f}, Watch: {:.3f}".format(np.sum(phone['pstep'])/total, np.sum(watch['wstep'])/total))
print("number of User =  Phone: {}, Watch: {}".format(len(set(phone['uid'])), len(set(watch['uid']))))

print("Exercise")
phone = df.query("index in @exercise").query("btype == 'p'")
watch = df.query("index in @exercise").query("btype == 'w'")
print("Differences = Phone: {:.3f}, Watch: {:.3f}".format(np.sum(phone['pstep'])/total, np.sum(watch['wstep'])/total))
print("number of User =  Phone: {}, Watch: {}".format(len(set(phone['uid'])), len(set(watch['uid']))))
print("Freq =  Phone: {}, Watch: {}".format(phone.shape[0], watch.shape[0]))


print("Not Argued")
df = df.query("find == False")
phone = df.query("btype == 'p'")
watch = df.query("btype == 'w'")
print("Differences = Phone: {:.3f}, Watch: {:.3f}".format(np.sum(phone['pstep'])/total, np.sum(watch['wstep'])/total))
print("number of User =  Phone: {}, Watch: {}".format(len(set(phone['uid'])), len(set(watch['uid']))))
