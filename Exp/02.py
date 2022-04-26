from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

# Bout Level Correlation Coefficient
df = loadDF()

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

ax.scatter(df["pstep"],df["wstep"], s= 1, color = "tab:olive")
ax.set_xlabel("Phone\n\nComparing Bout Level Step count of two device")
ax.set_ylabel("Watch")

total_diff = df[['pstep','wstep']].diff(axis = 1)['wstep'].to_numpy()
total_diff = np.sum(np.abs(total_diff))
phone = df.query("wstep == 0 ")["pstep"].to_numpy().sum()
watch = df.query("pstep == 0")["wstep"].to_numpy().sum()
print("Total Difference Ratio from Phone, Watch, Both Ratio ")
print("Phone: {:2.1f}% , Watch: {:2.1f}%, Both: {:2.1f}%".format(phone/total_diff*100, watch/total_diff*100, 100-(phone+watch)/total_diff*100))
print("-"*20)

corr = df[['pstep','wstep']].corr().iloc[0,1]
print("Correlation: {:.3f}".format(corr))
T, pVal = stats.ttest_rel(df['pstep'], df['wstep'])
print("paired t-test: T={}, p={:.3f}".format(T, pVal))
print("\n---------------")
print("For both detected bout")
both = df.query("btype == 'b'")
corr = both[['pstep','wstep']].corr().iloc[0,1]
print("Correlation: {:.3f}".format(corr))
T, pVal = stats.ttest_rel(both['pstep'], both['wstep'])
print("paired t-test: T={}, p={:.3f}".format(T, pVal))

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),fig_dir,f"{cur}.png"))