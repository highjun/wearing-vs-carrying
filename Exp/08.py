from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(9.6*ncols, 4.8 * nrows))

df = loadDF()
df['day'] = [ 7<= val <19 for val in df['hour'].to_numpy()]
comparingGroup(df, 'day','date', ax)
ax.set_xlabel('Comparing Bout ratio of Day(Left) and Night(Right)')
ax.set_ylabel('Ratio')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))