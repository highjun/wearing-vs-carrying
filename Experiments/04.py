from util import *

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]
users = sorted(set(df['users']))

step_min = 0
step_max = 1000
bin_size = 50
n_bin = (step_max-step_min)//bin_size
data = [[],[],[]]

data[0] = np.histogram(df.query("bout_type == 'p'")["step"], bins = n_bin, range = (step_min, step_max))[0]
data[1] = np.histogram(df.query("bout_type == 'w'")["step"], bins = n_bin, range = (step_min, step_max))[0]
data[2] = np.histogram(df.query("bout_type == 'b'")["step"], bins = n_bin, range = (step_min, step_max))[0]
data = np.array(data)/1000
datacum = data.cumsum(axis = 0)

nrows= 1
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))
ax[0].bar(x= np.arange(0.5, n_bin +.5), height = data[0], label = 'phone', color = color['phone'])
ax[0].bar(x= np.arange(0.5, n_bin +.5), height = data[1], bottom = datacum[0], label = 'watch', color = color['watch'])
ax[0].bar(x= np.arange(0.5, n_bin +.5), height = data[2], bottom = datacum[1], label = 'both', color = color['both'])
ax[0].set_xticks(np.arange(0,n_bin + 1))
ax[0].set_xticklabels(np.arange(step_min, step_max + bin_size, bin_size), fontsize = 7)
ax[0].set_xlabel("Step count")
ax[0].set_ylabel("Frequency(x1000)")

data = data/datacum[2]
datacum = datacum/datacum[2]
ax[1].bar(x= np.arange(0.5, n_bin +.5), height = data[0], label = 'phone', color = color['phone'])
ax[1].bar(x= np.arange(0.5, n_bin +.5), height = data[1], bottom = datacum[0], label = 'watch', color = color['watch'])
ax[1].bar(x= np.arange(0.5, n_bin +.5), height = data[2], bottom = datacum[1], label = 'both', color = color['both'])
ax[1].set_xticks(np.arange(0,n_bin + 1))
ax[1].set_xticklabels(np.arange(step_min, step_max + bin_size, bin_size), fontsize = 7)
ax[1].set_xlabel("Step count")
ax[1].set_ylabel("Ratio")
ax[1].legend()


plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
