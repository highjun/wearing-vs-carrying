from util import *

survey = load_survey()
valid_user = list(set(survey.query("invalid !=1")["id"]))

df = pd.read_csv(os.path.join(os.getcwd(),"Data","integrated.csv"), index_col= 0, header = 0)

df = df.query(f"users in {valid_user}")
df['timestamp'] = pd.to_datetime(df['timestamp'])

df = df.set_index(['users', 'timestamp', 'device'])[['step']]
df = df.unstack(level = 2, fill_value = 0)
df.columns = df.columns.droplevel()
df = df.reset_index().rename({'level_0':'users','level_1':'timestamp'})
df.sort_values(["users","timestamp"], inplace= True)

nrows = 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

ax[0].scatter(df["phone"], df["watch"], s= 4, color = "tab:olive")
corr = np.corrcoef(df["phone"],df["watch"])
ax[0].set_xlabel(f'''Phone

minute level Coef: {round(corr[0,1],3)}''')
ax[0].set_ylabel('Watch')

df = load_bout()
ax[1].scatter(df["phone"],df["watch"], s= 4, color = "tab:olive")
df = df.query("phone > 0 and watch >0")
corr = np.corrcoef(df["phone"],df["watch"])
ax[1].set_xlabel(f'''Phone

bout level Coef: {round(corr[0,1], 3)}''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures","02.png"))