from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = getSortedUser(df)
n_user = len(users)

total_diff= np.sum(np.abs(df["pstep"].to_numpy() - df["wstep"].to_numpy()))
df = filterWearingDate(df, ret_wearing = True)

df['run_ratio'] = [run/step if step> 0 else 0 for run, step in df[['run','step']].to_numpy()]

for btype in ["phone","watch", "both"]:
    exercise = df.query(f"run_ratio> .05 and btype == '{btype[0]}'")
    exercise_user = len(set(exercise['uid']))
    diff = exercise['step'].to_numpy().sum()
    print(f"{btype} {'only ' if btype !='both' else ''}exercise: It occured from {exercise_user}({round(exercise_user/n_user*100,1)}%) users make {round(diff/total_diff*100,1)}% difference")


nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows), sharex = True, sharey = False)


# bins = [0, 150, 500, 1000, 2000, 3000, 4000, 5000, 6000,7000, 8000, 20000]
# for jdx, metric in enumerate(["Freq","Ratio"]):
#     if jdx == 0:
#         bottom = np.zeros(len(bins)-1)
#         sum_ = np.ones_like(bottom)
#     else:
#         sum_ = bottom
#         bottom = np.zeros_like(sum_)
#     for idx, btype in enumerate(["both","phone","watch"]):
#         tmp = df.query(f"btype=='{btype[0]}' and run_ratio > 0.05")
#         hist, _ = np.histogram(tmp['step'], bins = bins)
#         ax[jdx].bar(x = np.arange(len(bottom)), height = hist/sum_, bottom = bottom, label = btype, color = color[btype])
#         bottom += hist/sum_
#     ax[jdx].set_xticks(np.arange(len(bottom)))
#     ax[jdx].set_xticklabels([f"[{bins[i-1]},{bins[i]})" for i in range(1, len(bins))], rotation = 90)
#     ax[jdx].set_ylabel(metric)
# ax[1].legend()

bins = [0, 150, 500, 1000, 2000, 3000, 4000, 5000, 6000,7000, 8000, 16000]
for jdx, metric in enumerate(["Total","Exercise"]):
    bottom = np.zeros(len(bins)-1)
    tmp = df
    if jdx == 1:
        tmp = tmp.query(f"run_ratio > .05")
    sum_, _  =np.histogram(tmp['step'], bins = bins)
    for idx, btype in enumerate(["both","phone","watch"]):
        tmp = df.query(f"btype=='{btype[0]}'")
        if jdx == 1:
            tmp = tmp.query(f"run_ratio > .05")
        hist, _ = np.histogram(tmp['step'], bins = bins)
        ax[jdx].bar(x = np.arange(len(bottom)), height = hist/sum_, bottom = bottom, label = btype, color = color[btype])
        bottom += hist/sum_
    ax[jdx].set_xticks(np.arange(len(bottom)))
    ax[jdx].set_xticklabels([f"[{bins[i-1]},{bins[i]})" for i in range(1, len(bins))], rotation = 90)
    ax[jdx].set_xlabel(metric)
ax[1].legend()

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
