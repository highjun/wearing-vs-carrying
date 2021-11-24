from numpy import histogram
from Experiment.util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
df['hour'] = df['first'].dt.hour
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = [(row['last']-row['first']).seconds/60+1 for _, row in df.iterrows()]
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]

step_min = 0
step_max = 1000
bin_size = 50
n_bin = (step_max-step_min)//bin_size
data = [[],[],[]]

data[0] = np.histogram(df.query("bout_type=='p'")["step"], bins = n_bin, range = (step_min, step_max))[0]
data[1] = np.histogram(df.query("bout_type=='w'")["step"], bins = n_bin, range = (step_min, step_max))[0]
data[2] = np.histogram(df.query("bout_type=='b'")["step"], bins = n_bin, range = (step_min, step_max))[0]
data = np.array(data)/1000
datacum = data.cumsum(axis = 0)
fig, ax = plt.subplots(nrows = 1, ncols = 1)
ax.bar(x= np.arange(0.5, n_bin +.5), height = data[0], label = 'phone', color = color['phone'])
ax.bar(x= np.arange(0.5, n_bin +.5), height = data[1], bottom = datacum[0], label = 'watch', color = color['watch'])
ax.bar(x= np.arange(0.5, n_bin +.5), height = data[2], bottom = datacum[1], label = 'both', color = color['both'])
ax.set_xticks(np.arange(0,n_bin + 1))
ax.set_xticklabels(np.arange(step_min, step_max + bin_size, bin_size), fontsize = 7)
ax.set_xlabel("Step count")
ax.set_ylabel("Frequency(x1000)")
ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"New", f"{cur}.png"))

