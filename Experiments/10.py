from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
survey = load_survey()
users = list(set(df["users"]))

nrows = 4
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

xlabels = [
    ['notf','not'],
    ['track','not'],
    ['10s','20s','30s','40+'],
    ['M','W'],
    ['[0,5000]','[5000,8000]','[8000,)'],
    ['b','p','w','n'],
    ['b','p','w','n'],
    ['b','p','w','n'],
    ['b','p','w','n']
]
supxlabels = [
    'Grouping by Notf',
    'Grouping by Tracking',
    'Grouping by Age',
    'Grouping by Gender',
    'Grouping by Active Level',
    'Grouping by Sleep time carry/wear',
    'Grouping by carry/wear before work',
    'Grouping by carry/wear working',
    'Grouping by carry/wear after work',
]
ylabels = [
    ['Total'],
    ['WearingDay'],
    ['Day', 'Night'],
    ['Weekday','Weekend'],
    ['Sleep', 'Before Work', 'Work', 'After Work']
]
anova_f = []
anova_p = []
for idx,users in enumerate([
    getNotfUser(), getTrackUser(), getAgeUser(), 
    getGenderUser(), getActiveUser(df), getCarryingUser(t = 1),
    getCarryingUser(t = 2),getCarryingUser(t = 3),getCarryingUser(t = 4)]):
    for jdx, metric in enumerate([
        getTotalRatio,
        getWearingDayRatio,
        getDayNightRatio,
        getWeekendRatio,
        getRoutineRatio
    ]): 
        if jdx == 1:
            nrows, ncols = 1, 1
            fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))
            
            users_df = [metric(user,df)[0] for user in users]
            
            F_stat, pVal = stats.f_oneway(*filter(lambda x: len(x) >0, [tmp['wearing'].to_numpy() for tmp in users_df]))
            anova_f.append(F_stat)
            anova_p.append(pVal)
            ax.boxplot([tmp['wearing'].to_numpy() for tmp in users_df], 
            labels = [label + f"({len(users[ldx])})" for ldx, label in enumerate(xlabels[idx])])
            ax.set_ylabel("Wearing Ratio")
            ax.set_ylim([-.1,1.1])
            ax.set_xlabel(f"F:{round(F_stat,2)}, p-val: {round(pVal, 3)}")
            plt.tight_layout()
            plt.savefig(os.path.join(os.getcwd(),"Figures", f"RQ3_{idx}_{jdx}.png"))
            plt.clf()
        else:
            users_df = [metric(user,df) for user in users]
            for kdx in range(len(ylabels[jdx])):
                kusers_df = [tmp[kdx] for tmp in users_df]
                nrows, ncols = 1, 2
                fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))
                # if idx == 7:
                    # print(kusers_df)
                    # print(kusers_df)
                F_stat, pVal = stats.f_oneway(*filter(lambda x: len(x) > 0,[1-tmp['w'].to_numpy() for tmp in kusers_df]))
                anova_f.append(F_stat)
                anova_p.append(pVal)
                ax[0].boxplot([ 1 - tmp['w'].to_numpy() for tmp in kusers_df], 
                labels = [label + f"({len(users[ldx])})" for ldx, label in enumerate(xlabels[idx])])
                ax[0].set_ylim([-.1,1.1])
                ax[0].set_xlabel(f"Phone, F:{round(F_stat,2)}, p-val: {round(pVal, 3)}")

                F_stat, pVal = stats.f_oneway(*filter(lambda x: len(x) > 0,[1-tmp['p'].to_numpy() for tmp in kusers_df]))
                anova_f.append(F_stat)
                anova_p.append(pVal)
                ax[1].boxplot([ 1 - tmp['p'].to_numpy() for tmp in kusers_df], 
                labels = [label + f"({len(users[ldx])})" for ldx, label in enumerate(xlabels[idx])])
                ax[1].set_ylim([-.1,1.1])
                ax[1].set_xlabel(f"Watch, F:{round(F_stat,2)}, p-val: {round(pVal, 3)}")             
                ax[0].set_ylabel("Covering Ratio")
                fig.supylabel(ylabels[jdx][kdx])
                fig.supxlabel(supxlabels[idx])
                plt.tight_layout()
                plt.savefig(os.path.join(os.getcwd(),"Figures", f"RQ3_{idx}_{jdx}_{kdx}.png"))
                plt.close()

pd.DataFrame(np.array(anova_f).reshape(-1, 19)).to_csv("anova_f.csv")
pd.DataFrame(np.array(anova_p).reshape(-1, 19)).to_csv("anova_p.csv")

