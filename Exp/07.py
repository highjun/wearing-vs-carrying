from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(9.6*ncols, 4.8 * nrows))

df = loadDF()
df['weekend'] = [ val>= 5 for val in df['weekday'].to_numpy()]
comparingGroup(df, 'weekend','date', ax)
ax.set_xlabel('Comparing Bout ratio of Weekday(Left) and Weekend(Right)')
ax.set_ylabel('Ratio')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))