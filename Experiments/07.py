from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()

step_min = 0
step_max = 1000
bin_size = 50
n_bin = (step_max-step_min)//bin_size

data = [[],[]]
total = np.sum(df["step"])
total_diff = np.sum(df.query("bout_type=='p'")["step"])+ np.sum(df.query("bout_type=='w'")["step"])
for idx in range(n_bin):
    x_min = idx*bin_size
    x_max = (idx+1)*bin_size
    bin_df = df.query(f"step>={idx*bin_size} and step< {(idx+1)*bin_size}")
    data[0].append((np.sum(bin_df.query("bout_type=='p'")["step"])+ np.sum(bin_df.query("bout_type=='w'")["step"]))/total_diff)
    data[1].append(np.sum(bin_df["step"])/total)

nrows= 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

ax[0].bar(x = np.arange(n_bin), height = data[0], color = "tab:olive")
ax[0].set_xticks(np.arange(-.5, n_bin))
ax[0].set_xticklabels(np.arange(step_min, step_max+bin_size, bin_size), ha="right",rotation = 45, rotation_mode="anchor")
ax[0].set_ylim([0,1])
ax[0].set_xlabel("Percentage per Difference")

ax[1].bar(x = np.arange(n_bin), height = data[1], color = "tab:olive")
ax[1].set_xticks(np.arange(-.5, n_bin))
ax[1].set_xticklabels(np.arange(step_min, step_max + bin_size, bin_size), ha="right",rotation = 45, rotation_mode="anchor")
ax[1].set_ylim([0,1])
ax[1].set_xlabel("Percentage per Total")


plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
