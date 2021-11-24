from Experiment.util import *

df = load_bout()
fig, ax = plt.subplots(nrows = 1, ncols =2, )

#step count distribution
df = df.groupby(['users','device','bout']).agg({'step':['sum','count'], 'timestamp':['first','last']})
df.columns = df.columns.droplevel()
df.rename({'sum':'step','count':'duration'},axis = 1, inplace=True)
df = df.reset_index().rename({'level_0':'users','level_1':'device','level_2':'bout'})
phone_steps = []
# phone_durations = []
watch_steps = []
# watch_durations = []
for idx in set(df['users']):
    phone_steps.append(df.query(f"device=='phone' and users =={idx}")["step"])
    watch_steps.append(df.query(f"device=='watch' and users =={idx}")["step"])
    # phone_durations.append(df.query(f"device=='phone' and users =={idx}")["duration"])
    # watch_durations.append(df.query(f"device=='watch' and users =={idx}")["duration"])

fig, ax = plt.subplots(nrows =1, ncols = 2, figsize = (12,3),constrained_layout = True, sharex= True)

# ax[0][0].plot([np.median(p) for p in phone_steps])
# ax[0][1].plot([np.median(w) for w in watch_steps])
# ax[1][0].plot([np.median(p) for p in phone_durations])
# ax[1][1].plot([np.median(p) for p in phone_durations])
# ax[1][0].set_xticks(range(len(set(df['users']))))
# ax[1][0].set_xticklabels(set(df['users']))
# ax[1][1].set_xticks(range(len(set(df['users']))))
# ax[1][1].set_xticklabels(set(df['users']))
ax[0].boxplot(phone_steps, showfliers = False, showbox= True,showcaps = False, whis = 0)
ax[1].boxplot(watch_steps, showfliers = False, showbox= True,showcaps = False, whis = 0)
ax[0].set_ylim([0,200])
ax[1].set_ylim([0,200])
# ax[1][0].boxplot(phone_durations, showfliers = False, showcaps  =False, whis = 0)
# ax[1][1].boxplot(watch_durations, showfliers = False, showcaps  =False, whis = 0)
# ax[1][0].set_ylim([0,10])
# ax[1][1].set_ylim([0,10])
ax[0].set_xlabel("Phone",fontsize = 16)
ax[1].set_xlabel("Watch", fontsize = 16)
plt.savefig(os.path.join(cwd,'Fig','bout_boxplot.png'))
