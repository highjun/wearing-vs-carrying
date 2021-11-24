from Experiment.util import *

df = load_bout()
scale = 10000

plt.subplots(ncols = 1, nrows = 1, figsize = (6,3))
phone = np.array(df.query(f"bout_type=='p'")["phone"])
watch = np.array(df.query(f"bout_type=='w'")["watch"])
both = (np.array(df.query(f"bout_type=='b'")["phone"])+ np.array(df.query(f"bout_type=='b'")["watch"]))/2

data = [[],[]]
for idx in range(20):
    phone = np.sum(df.query(f"bout_type == 'p' and phone <{50*(idx+1)} and phone >= {50*idx}")['phone'])
    watch = np.sum(df.query(f"bout_type == 'w' and watch <{50*(idx+1)} and watch >= {50*idx}")['watch'])
    data[0].append(phone)
    data[1].append(watch)
data = np.array(data)/scale
data_cum = data.cumsum(axis = 0)
plt.bar(x= list(np.arange(0.5,20.5)), height = data[1,:], width = .8, bottom = data_cum[0],label='watch', color = color['watch'])
plt.bar(x= list(np.arange(0.5,20.5)), height = data[0,:], width = .8, label='phone', color = color['phone'])
plt.xticks(np.arange(0,21),np.arange(0*50,21*50,50), fontsize =7)
plt.xlabel('Step')
plt.ylabel('Total sum(x10000)')
plt.tight_layout()

plt.savefig(os.path.join(os.getcwd(),'Fig','bout_step_step_hist.png'))