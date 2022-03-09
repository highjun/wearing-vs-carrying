from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()
survey = pd.read_csv(os.path.join(data_dir, "survey.csv"), index_col = False, header = 0) 

fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (4.8*2,3.2*2))
for i, usage in enumerate(['DAT','Notf','Exercise','Sleep']):
    notusers = survey[survey[f'Q3.{i+1}'] == 0.0]['UID'].values
    users = survey[survey[f'Q3.{i+1}'] == 1.0]['UID'].values
    print(usage, len(notusers), len(users))
    df[usage] = [0 if uid in users else (1 if uid in notusers else 2) for uid in df['uid'].values]
    comparingGroup(df.query(f"{usage} < 2"), usage, 'date', axes.flatten()[i])
    axes.flatten()[i].set_xlabel(f"Left({usage}) and Right(Not)")
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))
