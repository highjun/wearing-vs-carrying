from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

# Active Level에 따라서 Ratio 차이가 분명히 난다.
daily = df.groupby(["uid","date", "btype"]).agg(step = ("step","sum"))
daily = daily.unstack(level = 2, fill_value = 0)
daily.columns = ["b","p","w"]
daily = daily.apply(lambda x: np.concatenate((x/np.sum(x), x, np.sum(x).reshape(1))),axis = 1,  result_type='expand')
daily.columns = ['bratio','pratio','wratio','bstep','pstep','wstep','sum']
# 25% 3242.5 50% 5862.5 75% 9266.0 걸음에서 Active Level을 얻어옴
def cal_level(step):
    if step < 3000:
        return 0
    elif step < 6000:
        return 1
    elif step < 9000:
        return 2
    else:
        return 3
daily["active_level"] = [cal_level(val) for val in daily["sum"]]
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16, 3.6))
for jdx, btype in enumerate(['both','phone','watch']):
    data = [daily.query(f"active_level == @i and pratio < 1 and wratio < 1")[btype[0] + 'ratio'].to_numpy() for i in range(4)]
    axes[jdx].boxplot(data, labels = np.arange(4), showfliers = False)
    F_stat, pVal = stats.f_oneway(*data)
    axes[jdx].set_xlabel(f"F={round(F_stat,2)}, {'p=' + str(round(pVal,3)) if pVal > 0.001 else 'p < .001'}")
    axes[jdx].set_ylabel(f"{btype} bout ratio")
fig.supxlabel(", ".join([f"level {i} of day: " + str(daily.query("active_level == @i").shape[0]) for i in range(4)]))
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

