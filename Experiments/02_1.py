from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]


df = pd.read_csv(os.path.join(os.getcwd(),"Data","integrated.csv"), index_col= 0, header = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])

df = df.set_index(['uid', 'timestamp', 'device'])[['step']]
df = df.unstack(level = 2, fill_value = 0)
df.columns = df.columns.droplevel()
df = df.reset_index().rename({'level_0':'uid','level_1':'timestamp'})
df.sort_values(["uid","timestamp"], inplace= True)

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

ax.scatter(df["phone"],df["watch"], s= 1, color = "tab:olive")
ax.set_xlabel("Phone\n\nMinute Level Step count Scatter Plot")
ax.set_ylabel("Watch")

total_diff = np.sum(np.abs(df["phone"].to_numpy() - df["watch"].to_numpy()))
phone = df.query("watch == 0 ")["phone"].to_numpy().sum()
watch = df.query("phone == 0")["watch"].to_numpy().sum()
print("Total Difference 중의 Phone의 비율과 Watch의 비율: ")
print(f"Phone: {round(phone/total_diff*100,1)}% , Watch: {round(watch/total_diff*100,1)}%, Both: {round((1- (phone+ watch)/total_diff)*100,1)}%")
print("-"*20)

corr = np.corrcoef(df['phone'],df['watch'])[0,1]
print(f"Correlation: {round(corr,3)}")
T, pVal = stats.ttest_rel(df['phone'], df['watch'])
print(f"paired t-test: T={T}, p={pVal}")

both_df = df.query("phone > 0 and watch > 0")
both_corr = np.corrcoef(both_df['phone'],both_df['watch'])[0,1]
print(f"Both Minute Correlation: {round(both_corr,3)}")
T, pVal = stats.ttest_rel(both_df['phone'], both_df['watch'])
print(f"paired t-test: T={T}, p={pVal}")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures",f"{cur}.png"))