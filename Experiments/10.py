from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
survey = load_survey()

xlabels = [
    ['not','notf'],
    ['not','track'],
    ['10s','20s','30s','40+'],
    ['M','W'],
    ['[0,5000]','[5000,8000]','[8000,)'],
    ['b','p','w','n'],
    ['b','p','w','n'],
    ['b','p','w','n'],
    ['b','p','w','n']
]
ylabels = [
    ['Total'],
    # ['WearingDay'],
    ['Day', 'Night'],
    ['Weekday','Weekend'],
    # ['Sleep', 'Before Work', 'Work', 'After Work']
]
group = ["Notfication","Tracking","Age","Gender","ActiveLevel","Sleep","BeforeWork","Working","AfterWork"]
anova_f = []
anova_p = []
metric_name = ["Total","DayNight","Weekday"]
for idx,users in enumerate([
    getNotfUser(), getTrackUser(), getAgeUser(), 
    getGenderUser(), getActiveUser(df), getCarryingUser(t = 1),
    getCarryingUser(t = 2),getCarryingUser(t = 3),getCarryingUser(t = 4)]):
    for jdx, metric in enumerate([
        getTotalRatio,
        # getWearingDayRatio,
        getDayNightRatio,
        getWeekendRatio,
        # getRoutineRatio
    ]): 
        groups_df = [metric(user,df) for user in users]
        for kdx in range(len(ylabels[jdx])):
            kdf = [tmp[kdx] for tmp in groups_df]
            nrows, ncols = 1, 2
            fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))
            for col, btype in enumerate(["phone","watch"]):
                data = [df[btype[0]].to_numpy() + df['b'].to_numpy() for df in kdf]
                if len(list(filter(lambda x: len(x) > 0,data))) >= 2:
                    F_stat, pVal = stats.f_oneway(*filter(lambda x: len(x) > 0,data))
                else:
                    F_stat, pVal = np.NaN, np.NaN
                anova_f.append(F_stat)
                anova_p.append(pVal)
                ax[col].boxplot(data, labels = [label + f"({kdf[ldx].shape[0]})" for ldx, label in enumerate(xlabels[idx])])
                ax[col].set_ylim([-.1,1.1])
                ax[col].set_xlabel(f"Grouping by {group[idx]}\n\nF:{round(F_stat,2)}, p-val: {round(pVal, 3)}")
                ax[col].set_ylabel(f"{btype} covering ratio for {ylabels[jdx][kdx]}")
            plt.tight_layout()
            print(group[idx],ylabels[jdx][kdx])
            plt.savefig(os.path.join(os.getcwd(),"Figures", f"10_{group[idx]}_{ylabels[jdx][kdx]}.png"))
            plt.close()            

# pd.DataFrame(np.array(anova_f).reshape(-1, 19)).to_csv("anova_f.csv")
# pd.DataFrame(np.array(anova_p).reshape(-1, 19)).to_csv("anova_p.csv")

