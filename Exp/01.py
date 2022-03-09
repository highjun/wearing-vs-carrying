from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

# Minute Level Correlation Coefficient
df = pd.read_csv(os.path.join(data_dir,'integrate.csv'), index_col = False, header = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index(['uid', 'timestamp', 'device'])[['step']]
df = df.unstack(level = 2, fill_value = 0)
df = df.reset_index()
df.columns = ['uid','timestamp', 'phone','watch']
df.sort_values(["uid","timestamp"], inplace= True)

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

ax.scatter(df["phone"],df["watch"], s= 1, color = "tab:olive")
ax.set_xlabel("Phone\n\nComparing Minute Level Step count of two device")
ax.set_ylabel("Watch")

total_diff = df[['phone','watch']].diff(axis = 1)['watch'].to_numpy()
total_diff = np.sum(np.abs(total_diff))
phone = df.query("watch == 0 ")["phone"].to_numpy().sum()
watch = df.query("phone == 0")["watch"].to_numpy().sum()
print("Total Difference 중의 Phone의 비율과 Watch의 비율: ")
print(f"Phone: {round(phone/total_diff*100,1)}% , Watch: {round(watch/total_diff*100,1)}%, Both: {round((1- (phone+ watch)/total_diff)*100,1)}%")
print("-"*20)

corr = df[['phone','watch']].corr().iloc[0,1]
print("Correlation: {:.3f}".format(corr))
T, pVal = stats.ttest_rel(df['phone'], df['watch'])
print("paired t-test: T={}, p={:.3f}".format(T, pVal))
print("\n---------------")
print("For both detected minute")
both = df.query("phone > 0 and watch > 0")
corr = both[['phone','watch']].corr().iloc[0,1]
print("Correlation: {:.3f}".format(corr))
T, pVal = stats.ttest_rel(both['phone'], both['watch'])
print("paired t-test: T={}, p={:.3f}".format(T, pVal))

plt.tight_layout()
plt.savefig(os.path.join(fig_dir,f"{cur}.png"))