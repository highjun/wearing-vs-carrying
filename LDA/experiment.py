from util import *
from sklearn.decomposition import LatentDirichletAllocation
from scipy.sparse import csr_matrix
import pickle
import os

simulate = False
K = 30 #n_topic
n_exp = 1
if os.path.exists(f"lda_model_{n_exp}.pk") and simulate:
    print("Same number of experiment exists")
    exit()

df = load_bout()
# Active Level of Hourly Step Count
df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
hourly = df.groupby(["uid","date","30min"]).agg(step = ('step','sum'), pstep = ('pstep','sum'), wstep = ('wstep','sum'))
levels = np.percentile(hourly.query('step!=0')['step'], [0,33,66])
print("Levels: ", levels)
def get_active_level(step):
    if step == levels[0]:
        return 0
    elif step < levels[1]:
        return 1
    elif step < levels[2]:
        return 2
    else:
        return 3

def get_coarse_level(time):
    if time < 7: 
        return 0
    elif time < 9:
        return 1
    elif time < 11:
        return 2
    elif time < 14:
        return 3
    elif time < 17:
        return 4
    elif time < 19:
        return 5
    elif time < 21:
        return 6
    else:
        return 7

def decomp_word(word):
    ar = np.zeros(4)
    ar[0] = word//(4*4*8)
    word %= 4*4*8
    ar[1] = word//(4*8)
    word %= 4*8
    ar[2] = word//8
    word %= 8
    ar[3] = word
    return ar

hourly['level'] = [get_active_level(val) for val in hourly['step'].to_numpy()]
hourly = hourly[['level']].unstack(level = 2, fill_value = 0)
doc_vec = np.zeros((hourly.shape[0], 4*4*4*8))
for doc_idx in range(hourly.shape[0]):
    day = hourly.iloc[doc_idx]
    for idx in np.arange(1, 47):
        coarse = get_coarse_level(idx/2)
        word = [*day[idx-1:idx+2], coarse]
        word_idx = word[0]*4*4*8 + word[1]*4*8 + word[2]*8 + word[3]
        doc_vec[doc_idx, word_idx] += 1

doc_vec = csr_matrix(doc_vec)
LDA = LatentDirichletAllocation(n_components= K, 
                                max_iter = 1000,
                                learning_method="online",
                                learning_offset=50.0,
                                random_state=0,) #doc_topic_prior= 50 / 30, topic_word_prior= .01)
if simulate:
    fit = LDA.fit(doc_vec)
    print("saving ...")
    pickle.dump(fit, open(f"LDA/model_{n_exp}.pk", 'wb'))
else:
    print("loading...")
    LDA = pickle.load(open(f"LDA/model_{n_exp}.pk", 'rb'))

def cal_top_topics(transform):
    topics = np.zeros(K)
    for idx in range(doc_vec.shape[0]):
        day = transform[idx]
        top3 = day.argsort()[::-1][:3]
    for topic in top3:
        topics[topic] += 1
    return topics

def display_topics(transform, n_exp, n_toptopic = 12):
    fig, axes = plt.subplots(nrows  = 3, ncols = 4, figsize = (4*4.8, 3*3.2))
    topics = cal_top_topics(transform)
    toptopics = topics.argsort()[::-1][:n_toptopic]

    for idx,ax in enumerate(axes.flatten()):
        topic = toptopics[idx]
        docs = transform[:,topic].argsort()[:-50:-1]
        colors = np.zeros((50,48))
        for jdx, doc in enumerate(docs):
            colors[jdx] = hourly.iloc[doc]['level']
        ax.set_xlabel(f"Topic: {topic}")
        ax.set_xticks(np.arange(0,48+12, 12))
        ax.set_xticklabels(np.arange(0,24+6, 6))
        ax.pcolor(colors, cmap = "Reds")
    plt.savefig(f"topic_{n_exp}.png")
    plt.close()

transform = LDA.transform(doc_vec)
display_topics(transform, n_exp)


# distribution = LDA.components_ / LDA.components_.sum(axis=1)[:,np.newaxis]
# for topic in toptopics:
#     print('Topic #', topic)
#     tmp = distribution[topic]
#     print(*[str(decomp_word(word))+": " + "{:.2f}".format(tmp[word]) for word in tmp.argsort()[::-1][:5]])
#     print("-"*30+"\n")

# print("Word Topic Distribution")
# display_word_topic_distribution(LDA)
# print("Topic Word Distribution")
# display_topic_word_distribution(LDA)
# print("Transform")
# print(LDA.score(doc_vec))
# print(LDA.perplexity(doc_vec))
# print("-"*30)
# transform = LDA.transform(doc_vec)
# for idx in range(doc_vec.shape[0]):
#     print(f"Index: ", hourly.index[idx])
#     day = transform[idx]
#     top3 = day.argsort()[::-1][:3]
#     print("Top3 topics: ", top3)
#     for topic in top3:
#         print(topic,":",day[topic])
#     # print("Prob", day)
#     # print("Dominated Topics: ", np.argwhere(day > .5).reshape(-1).tolist())
#     print("--------------------")
# print("Most Occured Topics")
# topics = np.zeros(K)
# for idx in range(doc_vec.shape[0]):
#     day = transform[idx]
#     top3 = day.argsort()[::-1][:3]
#     for topic in top3:
#         topics[topic] += 1
# print(*[str(idx).zfill(2)+ " "*2 for idx in topics.argsort()[::-1][:15]])
# topics.sort()
# print(*[str(int(topic)).zfill(4) for topic in topics[::-1][:15]])
# then reload it with
# def display_word_topic_distribution(model):
#     distribution = model.components_ / model.components_.sum(axis=0)[np.newaxis,:]
#     for word in range(4*4*4*8):
#         print('Word #', list(decomp_word(word)))
#         tmp = distribution[:,word]
#         print(*[str(idx).zfill(2) + "  " for idx in tmp.argsort()[::-1][:10]])
#         tmp.sort()
#         print(*["{:.2f}".format(prob) for prob in tmp[::-1][:10]])
#         print("")
#         print("-"*30)
# def display_topic_word_distribution(model):
#     distribution = model.components_ / model.components_.sum(axis=1)[:,np.newaxis]
#     for compidx in range(K):
#         print('Topic #', compidx)
#         tmp = distribution[compidx]
#         print(*[str(idx).zfill(3) + " " for idx in tmp.argsort()[::-1][:10]])
#         tmp.sort()
#         print(*["{:.2f}".format(prob) for prob in tmp[::-1][:10]])
#         print("")
#         print("-"*30)