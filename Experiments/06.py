from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users =list(set(df['users']))

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

data = getWearingDayRatio(users, df)[0]['wearing'].to_numpy()
ax.boxplot(data, positions = [0])
ax.scatter(np.ones_like(data), data, s= 4, color = "tab:olive")
ax.set_xlim([-1,2])
ax.set_xticks([])

df.insert(1,'wearing',[1 if p<0.95 else 0 for p in df['date_wearing_ratio']])
nonwearing_date = df.query("wearing == 0").groupby(["users","date"]).agg(weekday =("weekday","first"))
weekend_ratio = nonwearing_date.query("weekday >= 5").shape[0]/nonwearing_date.shape[0]

ax.set_ylabel('Ratio of Wearing day')
fig.supxlabel(f'''weekend account for {round(weekend_ratio*100,2)}%''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))

