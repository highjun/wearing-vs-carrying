from util import *

pd.options.display.float_format = "{:,.2f}".format

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()

state = []
for user in sorted(set(df['uid'])):
    udf = df.query(f"uid == @user")
    udf['btype_idx'] = [['b','p','w'].index(val) for val in udf['btype'].values]
    diff_btype = udf['btype_idx'].diff()
    diff_date = udf['date'].diff().dt.total_seconds()
    diff_time = udf['last'].diff().dt.total_seconds()//60 - udf['duration']

    diff = np.array([1 if bt != 0 or time > 120 else 0  for bt, time in list(zip(diff_btype, diff_time))])

    # diff = np.array([1 if bt != 0 or time != 0 else 0  for bt, time in list(zip(diff_btype, diff_date))])
    state += list(diff.cumsum())
df['state'] = state


total_diff = np.sum(np.abs(df['pstep'] - df['wstep']))
phone_diff = np.sum(df.query("btype == 'p'")['pstep'])
watch_diff = np.sum(df.query("btype == 'w'")['wstep'])
both_diff = np.sum(np.abs(df.query("btype=='b'")['pstep'] - df.query("btype=='b'")['wstep']))

# Exclude Single Device Day
threshold = .95
boutdf = getBoutInfo(df, ['uid','date'])
total_day = boutdf.shape[0]
single = boutdf.query("(pstep_ratio > @threshold or wstep_ratio > @threshold)")
phone = np.sum(single['pstep'])
watch = np.sum(single['wstep'])
print("For Single Device, Phone: {:.3f}, Watch: {:.3f}".format( phone/total_diff, watch/total_diff))
notsingle = boutdf.query("not (pstep_ratio > @threshold or wstep_ratio > @threshold)")
tmp = df.reset_index().set_index(['uid','date'])
mask = tmp.index.isin(notsingle.index)
df = tmp.loc[mask]
df = df.reset_index()


coarse_timeslot = [(0,7),(7,9),(9,11),(11,13),(13,17),(17,19),(19,24)]
coarse = []
for val in df['first'].dt.hour:
    for i in range(len(coarse_timeslot)):
        if val < coarse_timeslot[i][1]:
            coarse.append(coarse_timeslot[i])
            break
df['coarse'] = coarse
threshold = .5
boutdf = getBoutInfo(df, ['uid','date','hour'])
boutdf = boutdf.query("wstep_ratio > @threshold or pstep_ratio > @threshold")
boutdf = boutdf.reset_index()

fig, ax = plt.subplots(nrows = 1, ncols = 1)
ax.bar(x = np.arange(24), height = boutdf.query("pstep_ratio > @threshold").groupby('hour').count()['date'].values/total_day, label = 'phone', color = color['phone'], alpha = .5)
ax.bar(x = np.arange(24), height = boutdf.query("wstep_ratio > @threshold").groupby('hour').count()['date'].values/total_day,label = "watch", color = color['watch'], alpha = .5)
ax.set_xticks(np.arange(24))
ax.set_xticklabels([str(i).zfill(2) for i in range(24)], rotation = 45, ha = 'center')
# ax.set_xticklabels(f"{timeslot[0]}-{timeslot[1]}"for timeslot in coarse_timeslot)
ax.set_xlabel("Timeslot")
ax.set_ylabel("Ratio of Day")
ax.set_ylim([0,1])
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))



print("Total Differences")
print("Both: {:.3f}, Phone: {:.3f}, Watch: {:.3f}".format(both_diff/total_diff, phone_diff/total_diff, watch_diff/total_diff))
phone = np.sum(boutdf['pstep'])
watch = np.sum(boutdf['wstep'])
print("For Timezone, Phone: {:.3f}, Watch: {:.3f}".format( phone/total_diff, watch/total_diff))
boutdf = getBoutInfo(df, ['uid','date','coarse'])
boutdf = boutdf.query("not (wstep_ratio > @threshold or pstep_ratio > @threshold)")
tmp = df.set_index(['uid','date','coarse'])
mask = tmp.index.isin(boutdf.index)
df = tmp.loc[mask]
df = df.reset_index()


def sumInt(arr):
    return int(np.sum(arr))

tmp = df.groupby(['uid','state']).agg(
    btype = ('btype','first'), nbout = ('btype','count'), 
    step = ('step', 'sum'), det = ('duration',sumInt),
    first = ('first','first'), last = ('last','last'))

tmp['dut'] = (tmp[['first','last']].diff(axis = 1)['last'].dt.total_seconds()//60) + 1
tmp['dut' ] =tmp['dut'].astype(int)
tmp['wd'] = tmp['first'].dt.weekday
tmp['dt'] = tmp['first'].dt.date
tmp['first_hour'] = tmp['first'].dt.hour
tmp['last_hour'] = tmp['last'].dt.hour
tmp['first'] = tmp['first'].dt.time
tmp['last'] = tmp['last'].dt.time

tmp = tmp.query("step > 100 and btype != 'b'")
tmp = tmp.reset_index()
tmp = tmp.set_index(['uid','dt','state'])
cols = ['btype','nbout', 'step','dut','det','wd','first','last', 'first_hour','last_hour']

print(tmp[cols[:-2]])