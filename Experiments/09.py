from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
df = df.query("weekday < 5")
users = getSortedUser(df)
n_user = len(users)

w = getRoutineRatio(users, df)
for idx, w_ in enumerate(w):
    w[idx] = w_.sort_index(level = 0, key=lambda x:[users.index(user) for user in x.to_numpy()])
    w[idx] = w[idx].reindex(users)
nrows, ncols = 2, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*4*ncols, 4.8/2*nrows))

routine_ = ['sleep','before work', 'work', 'after work']
for j, col in enumerate(['tab:blue','tab:orange','tab:green','tab:red']):
    for k in range(2):
        ax[k].bar(x= np.arange(n_user)*4.5+.5+j, height = 1-w[j]['w' if k == 0 else 'p'].to_numpy(na_value = -1), label = routine_[j], color = col)
        ax[k].set_ylim([0,1])
        ax[k].set_xlim([-1,4.5*n_user + 1])
ax[0].set_xlabel('Phone')
ax[1].set_xlabel('Watch')

ax[0].set_xticks(np.arange(n_user)*4.5+ 2)
ax[0].set_xticklabels(['']*n_user)
ax[1].set_xticks(np.arange(n_user)*4.5+ 2)
ax[1].set_xticklabels(['']*n_user)
fig.supxlabel("Covering Ratio for each interval for all Users")
# fig.supylabel('Covering Ratio')
ax[0].legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))  


# data= []
# for user in users:
#     sleep, wake, work, home = list(survey.query(f"id == '{user}'")[["sleep", "wake", "work", "home"]].values)[0]
#     user_df = df.query(f"users =='{user}'")
#     tmp = []
#     if sleep < wake:
#         tmp.append(user_df.query(f"hour < {wake} and hour > {sleep}"))
#     else:
#         tmp.append(user_df.query(f"hour < {wake} or hour > {sleep}"))
#     tmp.append(user_df.query(f"hour < {work} and hour > {wake}"))
#     tmp.append(user_df.query(f"hour < {home} and hour > {work}"))
#     if sleep > home:
#         tmp.append(user_df.query(f"hour < {sleep} and hour > {home}"))
#     else:
#         tmp.append(user_df.query(f"hour < {sleep} or hour > {home}"))
#     for t in tmp:
#         if t.shape[0] == 0:
#             data.append([])
#             data.append([])
#         else:
#             t = getBoutRatio(t)
#             data.append(1- t['p'].to_numpy())
#             data.append(1- t['w'].to_numpy())

#n_user x 4x 2
# data = np.array(data, dtype=object).reshape((len(set(df["users"])), 4, 2))
# nrows = 2
# ncols = 1
# fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*2*ncols, 4.8/2*nrows))
# for j, col in enumerate(['tab:blue','tab:orange','tab:green','tab:red']):
#     for k in range(2):
#         ax[k].boxplot(data[:,j,k],medianprops =dict(color= col),
#                         showcaps= False, showbox = False, showfliers = False)
# d1 = np.abs(data[:,3,0]- data[:,2,0]) > .1
# d2 = np.abs(data[:,2,0]- data[:,1,0]) > .1
# d3 = np.abs(data[:,3,0]- data[:,1,0]) > .1

# print(np.sum(d1))
# print(np.sum(d2))
# print(np.sum(d3))
# print(np.sum(d1 | d2))

# # ax[1].legend()
# fig.supylabel("Covering Ratio for each interval")
# # ax[0].set_xlabel("Watch")
# # ax[0].set_xticks(np.arange(len(set(df["users"])))+1)
# # ax[0].set_xticklabels(['']*len(set(df["users"])))
# # ax[1].set_xlabel("Phone")
# # ax[1].set_xticks(np.arange(len(set(df["users"])))+1)
# # ax[1].set_xticklabels(['']*len(set(df["users"])))
# # fig.supxlabel("Users")

# from matplotlib.lines import Line2D
# custom_lines = [Line2D([0], [0], color='tab:blue', lw=4),
#                 Line2D([0], [0], color='tab:orange', lw=4),
#                 Line2D([0], [0], color='tab:green', lw=4,),
#                 Line2D([0], [0], color='tab:red', lw=4)]
# ax[0].legend(custom_lines, ['sleep','before work', 'working','after work'], bbox_to_anchor = (1,0.5))

# plt.tight_layout()
# plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))  
