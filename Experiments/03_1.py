
from util import *

df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]

nrows = 4
ncols = 3
fig, axes = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))
metric = ["duration","distance","calorie","speed"]
for idx in range(4):
    p_df = df.query("bout_type=='p'")
    w_df = df.query("bout_type=='w'")
    b_df = df.query("bout_type=='b'")
    axes[idx][0].scatter(b_df["step"], b_df[metric[idx]], color = color["both"], label="both", s = 1)
    axes[idx][1].scatter(p_df["step"], p_df[metric[idx]], color = color["phone"], label="phone" ,s = 1)   
    axes[idx][2].scatter(w_df["step"], w_df[metric[idx]], color = color["watch"], label="watch",s = 1)
    axes[idx][0].set_ylabel(f'''{metric[idx]}''')

for j in range(3):
    axes[0][j].set_xlim([-500,16050])
    axes[0][j].set_ylim([-10,150])
    axes[1][j].set_xlim([-500,16050])
    axes[1][j].set_ylim([-500,14050])
    axes[2][j].set_xlim([-500,16050])
    axes[2][j].set_ylim([-50,1250])
    axes[3][j].set_xlim([-500,16050])
    axes[3][j].set_ylim([-.5,7.5])
axes[3][0].set_xlabel("both")
axes[3][1].set_xlabel("phone")
axes[3][2].set_xlabel("watch")
fig.supxlabel('''Step''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures",f"{cur}.png"))