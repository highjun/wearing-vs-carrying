from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

df = load_bout()
ax.scatter(df["pstep"],df["wstep"], s= 1, color = "tab:olive")
ax.set_xlabel("Phone\n\nBout Level Step count Scatter Plot")
ax.set_ylabel("Watch")

total_diff = np.sum(np.abs(df["pstep"].to_numpy() - df["wstep"].to_numpy()))
phone = df.query("btype== 'p'")["pstep"].to_numpy().sum()
watch = df.query("btype== 'w'")["wstep"].to_numpy().sum()
print("Total Difference 중의 Phone의 비율과 Watch의 비율: ")
print(f"Phone: {round(phone/total_diff*100,1)}% , Watch: {round(watch/total_diff*100,1)}%, Both: {round((1- (phone+ watch)/total_diff)*100,1)}%")
print("-"*20)

corr = np.corrcoef(df['pstep'],df['wstep'])[0,1]
print(f"Correlation: {round(corr,3)}")
T, pVal = stats.ttest_rel(df['pstep'], df['wstep'])
print(f"paired t-test: T={T}, p={pVal}")

both_df = df.query("btype == 'b'")
both_corr = np.corrcoef(both_df['pstep'],both_df['wstep'])[0,1]
print(f"Both Bout Correlation: {round(both_corr,3)}")
T, pVal = stats.ttest_rel(both_df['pstep'], both_df['wstep'])
print(f"paired t-test: T={T}, p={pVal}")

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures",f"{cur}.png"))