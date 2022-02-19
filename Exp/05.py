from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()

bratio = getBoutInfo(df, ['uid'])
n_user = len(set(df['uid']))
bratio = bratio.sort_values(by = 'bratio', ascending= False)


nrows, ncols = 2, 1
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize =(15, 4.8 * nrows))

def numSet(arr):
    return len(set(arr))
n_date = df.groupby(['uid']).agg(ndate = ('date',numSet))
# Normalize Quantative Factor by their number of date
columns = ['bstep','pstep','wstep','bcount','pcount','wcount', 'totalstep','totalcount']
bratio[columns] = bratio[columns]/n_date.to_numpy()

total = bratio['totalstep']
bottom = np.zeros(n_user)
for btype in ['both','phone','watch']:
    ax[0].bar(x = np.arange(n_user)+.5, height = bratio[btype[0]+'ratio'],bottom = bottom/total, label = btype, color = color[btype])
    ax[1].bar(x = np.arange(n_user)+.5, height = bratio[btype[0]+'step'],bottom = bottom, label = btype, color = color[btype])
    bottom += bratio[btype[0]+'step'].to_numpy()
    
for i in range(2):
    ax[i].set_xticks(np.arange(n_user)+.5)
    ax[i].set_xticklabels(["P" + str(user).zfill(2) for user in bratio.index], rotation =45, ha='center', fontsize= 7)
    ax[i].set_xlabel('Participants')
    ax[i].set_ylabel('Ratio' if i == 0 else '# of step')
    ax[i].legend()

threshold = .95
n_trust = [0,0]
for idx, btype in enumerate(['phone','watch']):
    n_trust[idx] = np.sum((bratio[btype[0]+'ratio'].to_numpy() + bratio['b'+'ratio'].to_numpy() ) > .95)
    print(f"{btype} is coverable for {btype}: {n_trust[idx]}({round(n_trust[idx]/n_user*100,1)}%)")
n_coverable = np.sum(((bratio['p'+'ratio'].to_numpy() + bratio['b'+'ratio'].to_numpy() ) > .95) | ((bratio['w'+'ratio'].to_numpy() + bratio['b'+'ratio'].to_numpy() ) > .95))
print(f"total {n_coverable}({round(n_coverable/n_user*100,1)}%)")

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, f"{cur}.png"))