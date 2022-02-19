from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

tmp = df.groupby(["uid", "date","btype"]).agg(step = ("step","sum"))
tmp = tmp.unstack(level=2, fill_value = 0)
tmp.columns = ['b','p','w']
tmp = tmp.apply(lambda x: np.concatenate((x/np.sum(x), x, np.sum(x).reshape(1))),axis = 1,  result_type='expand')
tmp.columns = ['bratio','pratio','wratio', 'both','phone','watch', 'step']
tmp = tmp.reset_index()

th = .95

total_diff= np.sum(np.abs(df["pstep"].to_numpy() - df["wstep"].to_numpy()))

for btype in ["phone","watch"]:
    single_day = tmp.query(f"{btype[0]}ratio > @th and step > 500")
    single_day['weekday'] = single_day['date'].dt.weekday
    single_user = len(set(single_day['uid']))
    diff = single_day[btype].to_numpy().sum()
    print(f"{btype} day: {single_day.shape[0]}({round(single_day.shape[0]/tmp.shape[0]*100,1)}%) occured from {single_user}({round(single_user/n_user*100,1)}%) users make {round(diff/total_diff*100,1)}% difference")
    print(f"{btype} Day 중 {single_day.query('weekday >= 5').shape[0]}({round(single_day.query('weekday >= 5').shape[0]/single_day.shape[0]*100,1)}%)는 주말에 해당한다.")

tmp.insert(0,'is_wearing',[0 if val > th else 1 for val in tmp['pratio'].to_numpy()])
data = tmp.groupby(['uid','is_wearing']).agg(ratio = ('date','count'))
data = data.unstack(level = 1, fill_value = 0)
data = data.apply(lambda x: x/np.sum(x), axis = 1)['ratio'][0].to_numpy()
ax.boxplot(data, positions = [0])
ax.scatter(np.ones_like(data), data, s= 1, color = "tab:olive")
ax.set_xlim([-1,2])
ax.set_xticks([])

ax.set_ylabel('Ratio of Non-Wearing day')
fig.supxlabel("Box plot and distribution of Non-Wearing day Ratio")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

