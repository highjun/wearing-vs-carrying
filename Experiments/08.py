from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
df = df.query("weekday <5")
users = getSortedUser(df)
n_user = len(users)

nrows, ncols = 1, 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(6.4*ncols, 4.8 * nrows))

day, night = getDayNightRatio(users, df)
day = day.sort_index(level = 0, key=lambda x: [users.index(user) for user in x.to_numpy()])
night = night.sort_index(level = 0, key=lambda x: [users.index(user) for user in x.to_numpy()])

for idx in range(ncols):
    ax[idx].scatter(1-day['w' if idx == 0  else 'p'].to_numpy(), 1-night['w' if idx == 0  else 'p'].to_numpy(),s = 4)
    ax[idx].set_xlabel('day' + ('Phone' if idx == 0  else 'Watch'))
    ax[idx].set_ylabel('night')
    ax[idx].set_xlim([0,1])
    ax[idx].set_ylim([0,1])


# for idx,user in enumerate(users):
#     user_df = df.query(f"users =='{user}'")
#     bout_df = user_df.groupby(["date","bout_type"]).agg(step = ("step","sum")) 
#     bout_df = bout_df.reindex(pd.MultiIndex.from_product([list(set(bout_df.index.get_level_values(0))), ['b','p','w']]),fill_value = 0)
#     bout_df = bout_df.unstack(level=1)
#     bout_df.columns = ['b','p','w']
#     wear_ratio = (bout_df['w']+bout_df['b'])/(bout_df['p']+bout_df['b']+ bout_df['w']) 
#     wearing_date = list(bout_df.index[wear_ratio >= 0.05])
#     user_df = user_df.query(f"date in {wearing_date}")
#     user_df = user_df.query(f"weekday < 5")

#     night = user_df.query('hour > 18 or hour < 9')
#     day = user_df.query('hour<=18 and hour >=9')

#     night_w.append(np.sum(night.query("bout_type != 'p'")["step"])/np.sum(night["step"]))
#     night_p.append(np.sum(night.query("bout_type != 'w'")["step"])/np.sum(night["step"]))
#     day_w.append(np.sum(day.query("bout_type != 'p'")["step"])/np.sum(day["step"]))
#     day_p.append(np.sum(day.query("bout_type != 'w'")["step"])/np.sum(day["step"]))

# night_w = np.array(night_w)
# night_p = np.array(night_p)
# day_w = np.array(day_w)
# day_p = np.array(day_p)
# ax[0][0].scatter(day_w, night_w, s=4)
# ax[0][1].scatter(night_p, night_w, s=4)
# ax[1][0].scatter(day_w, day_p, s=4)
# ax[1][1].scatter(night_p, day_p, s=4)
# ax[0][0].set_ylabel("night watch")
# ax[1][0].set_ylabel("day phone")
# ax[1][0].set_xlabel("day watch")
# ax[1][1].set_xlabel("night phone")

# fig.supxlabel(f'''Scatter plot of Ratio

# watch ratio was dropped for {np.sum( day_w - night_w >.1)}, and increased for {np.sum( day_w - night_w <-.1)}
# phone ratio was dropped for {np.sum( day_p - night_p >.1)}, and increased for {np.sum( day_p - night_p <-.1)}
# ''')

# for ax_ in ax.flatten():
#     ax_.set_xlim([0,1])
#     ax_.set_ylim([0,1])

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

