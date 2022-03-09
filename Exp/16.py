from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()

total_diff = np.sum(np.abs(df['pstep'] - df['wstep']))
phone_diff = np.sum(df.query("btype == 'p'")['pstep'])
watch_diff = np.sum(df.query("btype == 'w'")['wstep'])
both_diff = np.sum(np.abs(df.query("btype=='b'")['pstep'] - df.query("btype=='b'")['wstep']))


boutdf = getBoutInfo(df, ['uid','date'])

state = []
for user in sorted(set(df['uid'])):
    udf = df.query(f"uid == @user")
    udf['btype_idx'] = [['b','p','w'].index(val) for val in udf['btype'].values]
    diff_btype = udf['btype_idx'].diff()
    diff_date = udf['date'].diff().dt.total_seconds()
    diff_time = udf['last'].diff().dt.total_seconds()//60 - udf['duration']

    # diff = np.array([1 if bt != 0 or time > 120 else 0  for bt, time in list(zip(diff_btype, diff_time))])

    diff = np.array([1 if bt != 0 or time != 0 else 0  for bt, time in list(zip(diff_btype, diff_date))])
    state += list(diff.cumsum())
df['state'] = state

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



# tmp = tmp.query("step > 50")
tmp = tmp.reset_index()
tmp = tmp.set_index(['uid','dt','state'])

start, end, bsize = 0, 600, 20
n_level = (end-start)//bsize
def getLevel(step):
    level = (step-start)//bsize
    if level >= n_level:
        return n_level-1
    return level
tmp['level'] = [getLevel(dut) for dut in tmp['dut'].to_numpy()]

phone = tmp.query("btype == 'p'").groupby('level').agg(step=('step','sum'))
phone = phone.reindex(np.arange(n_level),fill_value = 0)['step']
watch = tmp.query("btype == 'w'").groupby('level').agg(step=('step','sum'))
watch = watch.reindex(np.arange(n_level),fill_value = 0)['step']

phone /= total_diff
watch /= total_diff

print(phone, watch)

# phone, _ = np.histogram(phone['dut'], bins = np.arange(0,end+bsize, bsize))
# watch, _ = np.histogram(watch['dut'], bins = np.arange(0,end+bsize, bsize))


fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (4.8, 4.8))

ax.bar(height = phone,x= np.arange((end-start)//bsize)+.5, label = 'phone', color = color['phone'], alpha = .5)
ax.bar(height = watch,x= np.arange((end-start)//bsize)+.5, label = 'watch', color = color['watch'], alpha = .5)


ax.set_xticks(np.arange((end-start)//bsize + 1))
ax.set_xticklabels(np.arange(start, end + bsize, bsize), fontsize = 7, ha='center', rotation= 45)
ax.set_xlabel("Bin for Duration")
ax.legend()
ax.set_ylabel("Step Count")

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))