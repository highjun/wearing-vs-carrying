from util import *
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
import pickle

from sklearn.decomposition import LatentDirichletAllocation

df = load_bout()
# Active Level of Hourly Step Count
df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
hourly = df.groupby(["uid","date","30min"]).agg(step = ('step','sum'))
hourly = hourly.unstack(level = 2, fill_value = 0)
serial = hourly.to_numpy().reshape(-1)
# for step in [0, 10, 50,100, 150]:
#     print(np.sum(serial <= step)/serial.shape[0])
# 0이 58%, 10까지가 3%, 50까지가 11%, 100까지가 6%,  150까지가 4%, 그이상이 18%
hourly = df.groupby(["uid","date","30min", "btype"]).agg(step = ('step','sum'))
hourly = hourly.unstack(level = 3, fill_value = 0)
hourly.columns = ['b','p','w']

simulate = False
K = 15 #n_topic
n_exp = 'active'
if os.path.exists(f"LDA/model_{n_exp}.pk") and simulate:
    print("Same number of experiment exists")
    exit()
log = open(f"LDA/result_{n_exp}.out","w")

thd = 100
def get_active_level(b,p,w):
    total = b+p+w
    word = [0,0,0]
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
    return word
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

hourly['word'] = [get_active_level(*steps)[0] for steps in hourly[['b','p','w']].to_numpy()]
hourly = hourly[['word']].unstack(level = 2, fill_value = 0)
hourly = hourly.sort_index()
words = sorted(list(set([str(val)for val in hourly.to_numpy().reshape(-1).tolist()])))
print('time slot words:',words)
bags = []
for doc_idx in range(hourly.shape[0]):
    bags.append([])
    day = hourly.iloc[doc_idx]
    for idx in np.arange(1, 47):
        coarse = get_coarse_level(idx/2)
        word = [*day[idx-1:idx+2], coarse]
        bags[-1].append(str(word))

vectorizer = CountVectorizer(analyzer=lambda x: x)
doc_vec = vectorizer.fit_transform(bags).toarray()
print("n_word: ", doc_vec.shape[1])
doc_vec = csr_matrix(doc_vec)
print("Word Preprocessing Complete...")

LDA = LatentDirichletAllocation(n_components= K, 
                                max_iter = 500,
                                learning_method="online",
                                random_state=0,)
if simulate:
    fit = LDA.fit(doc_vec)
    print("saving ...",)
    pickle.dump(fit, open(f"LDA/model_{n_exp}.pk", 'wb'))
else:
    print("loading...")
    LDA = pickle.load(open(f"LDA/model_{n_exp}.pk", 'rb'))

def cal_top_topics(transform):
    topics = transform.sum(axis = 0).argsort()[::-1]
    return topics

def display_topics(transform, n_exp, nrows = 2, ncols = 4):
    fig, axes = plt.subplots(nrows  = nrows, ncols = ncols, figsize = (ncols*4.8, nrows*3.2))
    topics = cal_top_topics(transform)
    for idx,ax in enumerate(axes.flatten()):
        topic = topics[idx]
        docs = transform[:,topic].argsort()[:-51:-1]
        colors = np.zeros((50,48))
        for jdx, doc in enumerate(docs):
            colors[jdx] = [words.index(str(word)) for word in hourly.iloc[doc]['word'].to_numpy()]
        ax.set_xlabel(f"Topic: {topic}")
        ax.set_xticks(np.arange(0,48+12, 12))
        ax.set_xticklabels(np.arange(0,24+6, 6))
        import matplotlib.colors as mcolors
        clist = [mcolors.hsv_to_rgb(hsv) for hsv in [(0, 0,1), (0,0.5,1), (0,1,1)]]
        cmap = mcolors.LinearSegmentedColormap.from_list('mycmap', clist, N = len(words))
        c = ax.pcolor(colors, cmap = cmap, vmin = 0, vmax = len(words)-1)
        fig.colorbar(c, ax=ax)
    plt.tight_layout()
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
    top_topics= cal_top_topics(transform)
    for topic in top_topics:
        docs =transform[:,topic].argsort()[:-51:-1]
        print('Topic #', topic, file = log)
        for doc in docs:
            print(f"Doc: {hourly.index[doc]}, Topic Prob: {round(transform[doc,topic],3)}",file = log)
            # print(list(hourly.iloc[doc]['word'].to_numpy()), file = log)
        print("-"*30, file = log)

transform = LDA.transform(doc_vec)
display_topics(transform, n_exp)
display_doc_topic_distribution(transform)
print("Transform!")
print(*[str(topic).zfill(2) + " "*3 for topic in range(K)], file = log)
print("dominant pattern %:", np.sum(transform > .5)/transform.shape[0])
for doc in transform:
    print(*["{:.3f}".format(topic) for topic in doc], file = log)

pickle.dump(transform, open(f"LDA/{n_exp}_transform.pk",'wb'))

log.close()
