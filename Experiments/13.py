from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = sorted(set(df['users']))

fig, ax = plt.subplots(nrows = 1, ncols = 1)
type = ['phone','watch','both']
data = []
watch = 0
phone = 0
for idx,user in enumerate(users):
    user_df = df.query(f"users =='{user}'") 
    wear = user_df.groupby('date').agg(phone=('phone','sum'),watch = ('watch','sum'))
    nonwearing_date = wear.query("watch == 0").index
    data.append(len(nonwearing_date)/len(set(user_df["date"])))
ax.boxplot(data,positions=[0])
ax.scatter(np.ones_like(data), data, s= 4, color = "tab:olive")
ax.set_xlim([-1,2])
ax.set_xticks([])
ax.set_ylabel('Ratio of Non-wearing day')
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

