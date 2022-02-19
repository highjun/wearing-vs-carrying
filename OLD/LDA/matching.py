
from util import *
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
import pickle

transforms = []
log =  open("LDA/matching.out", 'w')
for exp in ['active', 'phone','watch']:
    transforms.append(pickle.load(open(f"LDA/{exp}_transform.pk",'rb')))
print(transforms[0].shape)
# desc =[{0 : 'None', 13: '7-19,2', 12:'11-24,2', 8: '9-24, 1', 10: '7-24,2', 1:'9-24,2', 7: '7-24,1', 3:'All'}
# ,{0 : 'None', 13: '7-9+17-24,1', 8:'11-24,1', 9: 'all, 1', 12: '7-24', 6:'11-24,2', 5: '7-24,2', 14:'11-24,2'}
# ,{0 : 'None', 5: '12-24,1', 12:'7-19,1', 13: '9-19,2', 9: '0-11+19-24, 1', 1:'0-24', 7: '9-24', 10:'19-24,2'}]
# desc =[{0 : 'None', 13: '6-19', 12:'12-24', 8: '12-24', 10: '6-24', 1:'12-24', 7: '6-24', 3:'All'}
# ,{0 : 'None', 13: '7-9+17-24,1', 8:'12-24', 9: 'All', 12: '6-19', 6:'12-24', 5: '6-24', 14:'12-24'}
# ,{0 : 'None', 5: '12-24', 12:'6-19', 13: '6-19', 9: '0-11+19-24', 1:'All', 7: '12-24', 10:'19-21'}]
# topicsword = []
# for docidx in range(transforms[0].shape[0]):
#     toptopics = []
#     for tidx in range(len(transforms)):
#         topic = transforms[tidx][docidx].argmax()
#         prob = transforms[tidx][docidx, topic]
#         # toptopics.append([topic, prob])
#         if topic in desc[tidx].keys():
#             toptopics.append(desc[tidx][topic])
#         else:
#             toptopics.append("Not Selected")
#     topicsword.append(str(toptopics))
#     print(*toptopics, file =log)
# word_dist = []
# for word in set(topicsword):
#     word_dist.append([word,topicsword.count(word)])
# word_dist = sorted(word_dist, key = lambda x: x[1])
# print("-"*50)
# print(*word_dist, file = log, sep="\n")

df = load_bout()
total_diff= np.sum(np.abs(df["pstep"].to_numpy() - df["wstep"].to_numpy()))
users = getSortedUser(df)
n_user = len(users)
daily = df.groupby(['uid','date','btype']).agg(step = ('step','sum'))
daily = daily.unstack(level = 2, fill_value = 0)
daily.columns = ['b','p','w']
daily = daily.sort_index()
daily = daily.reset_index()
phone = transforms[2]
topics = phone.sum(axis = 0).argsort()[::-1]
toptopic = phone.argmax(axis = 1)
# print(*toptopic)
# print("-"*50)
for topic in topics[:8]:
    idxes =  np.arange(phone.shape[0])[toptopic == topic]
    # docs = phone[toptopic == topic]
    tmp = daily.iloc[idxes]
    n_topicuser = len(set(tmp['uid']))
    diff = tmp['w'].to_numpy().sum()
    print(f"Topic {topic}: {tmp.shape[0]} days occured from {n_topicuser}({round(n_topicuser/n_user*100,1)}%) users make {round(diff/total_diff*100,1)}% difference")

log.close()