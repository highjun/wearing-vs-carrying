from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

daily = df.groupby(["uid","date", "btype"]).agg(step = ("step","sum"))
daily = daily.unstack(level = 2, fill_value = 0)
daily.columns = ["b","p","w"]
daily = daily.apply(lambda x: np.concatenate((x/np.sum(x), x, np.sum(x).reshape(1))),axis = 1,  result_type='expand')
daily.columns = ['bratio','pratio','wratio','bstep','pstep','wstep','sum']
daily = daily.reset_index() 

daily["is_weekend"] = [1 if val >= 5 else 0 for val in daily['date'].dt.weekday.to_numpy()]
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16, 3.6))
for jdx, btype in enumerate(['both','phone','watch']):
    data = [daily.query(f"is_weekend ==@i")[btype[0] + 'ratio'].to_numpy() for i in range(2)]
    axes[jdx].boxplot(data, labels = ["Weekday","Weekend"], showfliers = False)
    F_stat, pVal = stats.f_oneway(*data)
    axes[jdx].set_xlabel(f"F={round(F_stat,2)}, {'p=' + str(round(pVal,3)) if pVal > 0.001 else 'p < .001'}")
    axes[jdx].set_ylabel(f"{btype} bout ratio")
fig.supxlabel(f"Weekday({daily.query(f'is_weekend == 0').shape[0]}), Weekend({daily.query(f'is_weekend == 1').shape[0]})")
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

