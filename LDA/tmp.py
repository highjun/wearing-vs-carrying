from util import *

df = load_bout()
# Active Level of Hourly Step Count
df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
hourly = df.groupby(["uid","date","30min"]).agg(step = ('step','sum'))
hourly = hourly.unstack(level = 2, fill_value = 0)
serial = hourly.to_numpy().reshape(-1)
# for step in [0, 10, 50,100, 150]:
#     print(np.sum(serial <= step)/serial.shape[0])
# 0이 58%, 10까지가 3%, 50까지가 11%, 100까지가 6%,  150까지가 4%, 그이상이 18%


# p,w가 동시에 나타나는 개수?
hourly = df.groupby(["uid","date","30min", "btype"]).agg(step = ('step','sum'))
hourly = hourly.unstack(level = 3, fill_value = 0)
hourly.columns = ['b','p','w']
# for idx in range(8):
#     tmp = hourly
#     if idx & 2 == 0:
#         print('p>0', end =", ")
#         tmp = tmp.query('p>0')
#     if idx & 4 == 0:
#         print('w>0', end =", ")
#         tmp = tmp.query('w>0')
#     if idx & 1 == 0:
#         print('b>0', end =", ")
#         tmp = tmp.query('b>0')
#     print(tmp.shape[0]/serial.shape[0])
# p>0, w>0, b>0, 0.015956822715006452
# p>0, w>0, 0.02466121084125308
# w>0, b>0, 0.07902880441159216
# w>0, 0.18530007039774726
# p>0, b>0, 0.04756247800070398
# p>0, 0.1722838202510853
# b>0, 0.20009093042355977

# b => 0 , 1
# p,w => (0,0), (1,1), (0,1), (0,2), (1,0), (2,0)

simulate = False
K = 10 #n_topic
n_exp = 12
if os.path.exists(f"LDA/model_{n_exp}.pk") and simulate:
    print("Same number of experiment exists")
    exit()
log = open(f"LDA/result_{n_exp}.out","w")

thd = 100
def get_active_level(b,p,w):
    total = b+p+w
    word = [0,0,0]
    # word = [0]
    for idx, step in enumerate([total,p,w]):
        if step == 0:
            pass
        elif step <= thd:
            word[idx] = 1
        else:
            if idx == 0:
                word[idx] = 2
            else:
                word[idx] = 1
    
    return word[0]      
def get_coarse_level(time):
    if time < 7: 
        return [0,7]
    elif time < 9:
        return [7,9]
    elif time < 11:
        return [9,11]
    elif time < 14:
        return [11,14]
    elif time < 17:
        return [14, 17]
    elif time < 19:
        return [17, 19]
    elif time < 21:
        return [19, 21]
    else:
        return [21,24]

hourly['word'] = [get_active_level(b,p,w) for b,p,w in hourly[['b','p','w']].to_numpy()]
hourly = hourly[['word']].unstack(level = 2, fill_value = 0)
words = sorted(list(set([str(val) for val in hourly.to_numpy().reshape(-1).tolist()])))
print('time slot words:',words)
bags = []
for doc_idx in range(hourly.shape[0]):
    bags.append([])
    day = hourly.iloc[doc_idx]
    for idx in np.arange(1, 47):
        coarse = get_coarse_level(idx/2)
        word = [*day[idx-1:idx+2], coarse]
        bags[-1].append(str(word))

from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
vectorizer = CountVectorizer(analyzer=lambda x: x)
doc_vec = vectorizer.fit_transform(bags).toarray()
print("n_word: ", doc_vec.shape[1])
doc_vec = csr_matrix(doc_vec)
print("word Preprocessing Complete")


from sklearn.decomposition import LatentDirichletAllocation
LDA = LatentDirichletAllocation(n_components= K, 
                                max_iter = 150,
                                learning_method="online",
                                random_state=0,)
import pickle
if simulate:
    fit = LDA.fit(doc_vec)
    print("saving ...",)
    pickle.dump(fit, open(f"LDA/model_{n_exp}.pk", 'wb'))
else:
    print("loading...")
    LDA = pickle.load(open(f"LDA/model_{n_exp}.pk", 'rb'))

def cal_top_topics(transform):
    topics = transform.sum(axis = 0)
    return topics

def display_topics(transform, n_exp, nrows = 2, ncols = 4):
    fig, axes = plt.subplots(nrows  = nrows, ncols = ncols, figsize = (ncols*4.8, nrows*3.2))
    topics = cal_top_topics(transform)
    toptopics = topics.argsort()[::-1]

    for idx,ax in enumerate(axes.flatten()):
        topic = toptopics[idx]
        docs = transform[:,topic].argsort()[:-50:-1]
        colors = np.zeros((50,48))
        for jdx, doc in enumerate(docs):
            colors[jdx] = [words.index(str(word)) for word in hourly.iloc[doc]['word'].to_numpy()]
        ax.set_xlabel(f"Topic: {topic}")
        ax.set_xticks(np.arange(0,48+12, 12))
        ax.set_xticklabels(np.arange(0,24+6, 6))
        c = ax.pcolor(colors, cmap = 'tab20', vmin = 0, vmax = len(words)-1)
        fig.colorbar(c, ax=ax)
    plt.savefig(f"LDA/topic_{n_exp}.png")
    plt.close()

def display_topic_word_distribution(model, transform):
    top_topics= cal_top_topics(transform).argsort()[::-1]
    distribution = model.components_ / model.components_.sum(axis=1)[:,np.newaxis]
    for topic in top_topics:
        print('Topic #', topic, file = log)
        tmp = distribution[topic]
        print(*[str(idx).zfill(3) + " " for idx in tmp.argsort()[::-1]], file = log)
        tmp.sort()
        print(*["{:.2f}".format(prob) for prob in tmp[::-1]], file = log)
        print("", file = log)
        print("-"*30, file = log)

def display_doc_topic_distribution(transform):
    top_topics= cal_top_topics(transform).argsort()[::-1]
    for topic in top_topics:
        docs =transform[:,topic].argsort()[:-50:-1]
        print('Topic #', topic, file = log)
        for doc in docs:
            print(f"Doc: {hourly.index[doc]}, Topic Prob: {round(transform[doc,topic],3)}",file = log)
            # print(list(hourly.iloc[doc]['word'].to_numpy()), file = log)
        print("-"*30, file = log)

transform = LDA.transform(doc_vec)
display_topics(transform, n_exp)
display_doc_topic_distribution(transform)

top_topics = cal_top_topics(transform).argsort()[:-9:-1]
top5_acc = transform[:,top_topics].sum(axis = 1)
print(top5_acc.min(), top5_acc.max(), file = log)

log.close()
