from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()
survey = pd.read_csv(os.path.join(data_dir, "survey.csv"), index_col = False, header = 0) 

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (4.8,3.2))
usage = 'Enter'
users = survey[survey[f'Q4'] == 'Enter']['UID'].values
ver2users = survey[survey[f'VER'] == 2]['UID'].values
print(usage, len(users))
df[usage] = [0 if uid in users else (1 if uid in ver2users else 2) for uid in df['uid'].values]
comparingGroup(df.query(f"{usage} < 2"), usage, 'date', ax)
ax.set_xlabel(f"Left({usage}) and Right(Not)")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))
