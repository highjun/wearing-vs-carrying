from util import *
df = load_bout()
cur = os.path.splitext(os.path.basename(__file__))[0]
users = set(df["users"])

nrows = 1
ncols = 1
fig, ax = plt.subplots(nrows = nrows, ncols= ncols, figsize= (6.4*ncols, 4.8*nrows))

p_df = df.query("bout_type=='p'")
p_hist,_ = np.histogram(p_df["step"], bins = np.arange(0, 1010, 10))
w_df = df.query("bout_type=='w'")
w_hist,_ = np.histogram(w_df["step"], bins = np.arange(0, 1010, 10))
b_df = df.query("bout_type=='b'")
b_hist,_ = np.histogram(b_df["step"], bins = np.arange(0, 1010, 10))

p_hist = p_hist/np.sum(p_hist)
w_hist = w_hist/ np.sum(w_hist)
b_hist = b_hist/np.sum(b_hist)

plt.plot(np.arange(5,1000,10), p_hist,  label="phone", color = color["phone"])
plt.plot(np.arange(5,1000,10), w_hist,  label="watch", color = color["watch"])
plt.plot(np.arange(5,1000,10), b_hist,  label="both", color = color["both"])

plt.legend()
ax.set_ylim([-0.2,1.2])
ax.set_ylabel("Probability")
ax.set_xlabel('''Step''')

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))
