from numpy import zeros_like
from util import *
from sklearn.decomposition import LatentDirichletAllocation
from scipy.sparse import csr_matrix
import matplotlib as mpl
import pickle
import os
import shutil

df = loadDF()

simulate = True
K = 8 #n_topic
n_exp = 10
if simulate:
    if os.path.exists(f"LDA_/lda{n_exp}.py"):
        print("Same number of experiments exists")
        exit()
    else:
        shutil.copyfile(f"lda.py", f"LDA_/lda{n_exp}.py")
log = open(f"LDA_/result_{n_exp}.out","w")


df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
coverage = getBoutInfo(df, ['uid', 'date', 'weekday','30min'])

columns = []
for metric in ['step_ratio', 'step','count_ratio', 'count']:
    for btype in ['b','p','w']:
        columns.append(btype+metric)
columns.append('totalstep')
columns.append('totalcount')

# For figure
# def RGB2tuple(code):
#     return (int("0x"+code[1:3],16)/255, int("0x"+code[3:5],16)/255, int("0x"+code[5:7],16)/255, 1)
color_match= [(0,'#ffffff'), (.2,'#aaaaaa'),(.4, color['both']), (.6, color['phone']), (.8, color['watch']), (1, '#e8a7a7')]
descriptions = ["inactive", "small step", "both-dominant", "phone-dominant", "watch-dominant", "else"]
cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', color_match, len(color_match))
patches = []
import matplotlib.patches as mpatches
for i in range(6):
    patches.append(mpatches.Patch(color = color_match[i][1], label = descriptions[i]))

def get_color(row):
    # White
    if row[columns.index('totalcount')] ==0:
        return 0
    # 연한 회색
    if row[columns.index('totalcount')] <= 1 and row[columns.index('totalstep')] <10:
        return 1
    # Both
    elif row[columns.index('bstep_ratio')] >.95:
        return 2
    # Phone
    elif row[columns.index('pstep_ratio')] >.95:
        return 3
    # Watch
    elif row[columns.index('wstep_ratio')] >.95:
        return 4
    # No-Dominant   
    else:
        return 5

# Calcluated Feature for LDA
n_feature = 4
def get_feature(row):
    if row[columns.index('totalcount')] <= 1 and row[columns.index('totalstep')] <10:
        return 0
    elif row[columns.index('bstep_ratio')] >.95:
        return 1
    elif row[columns.index('pstep_ratio')] >.95:
        return 2
    elif row[columns.index('wstep_ratio')] >.95:
        return 3
    else:
        return 0
coverage['color'] = [get_color(row) for row in coverage.values]
coverage['feature_LDA'] = [get_feature(row) for row in coverage.values]
coverage_plot = coverage[['color']].unstack(level = 3, fill_value= 0)
coverage_LDA = coverage[['feature_LDA']].unstack(level = 3, fill_value= 0)
def encode(features:list, time:int):
    code = time
    for idx, elem in enumerate(features):
        code += 8*(n_feature**idx)*elem
    return code
def decode(code:int):
    time = code%8
    code //= 8
    features = []
    while code!=0:
        features.append(code%n_feature)
        code //= n_feature
    return features, time
def get_coarse_level(times:np.ndarray):
    coarse= np.zeros_like(times)
    for cut in [7,9,11,14,17,19,21]:
        coarse[times>=cut] +=1
    return coarse

doc_vec = np.zeros((coverage_LDA.shape[0], 8*n_feature**3))
for doc_idx in range(coverage_LDA.shape[0]):
    day = coverage_LDA.iloc[doc_idx].values
    words = []
    for idx in np.arange(1,47):
        words.append(day[idx-1:idx+2])
    words = list(zip(words, get_coarse_level(np.arange(1,47))))
    for word, time in words:
        doc_vec[doc_idx, encode(word,time)] += 1
        
doc_vec = csr_matrix(doc_vec)
LDA = LatentDirichletAllocation(n_components= K, 
                                max_iter = 1000,
                                learning_method="online",
                                learning_offset=50.0,
                                random_state=0,) #doc_topic_prior= 50 / 30, topic_word_prior= .01)
if simulate:
    fit = LDA.fit(doc_vec)
    print("saving ...", file = log, flush = True)
    pickle.dump(fit, open(f"LDA_/model_{n_exp}.pk", 'wb'))
else:
    print("loading...",file = log, flush = True)
    LDA = pickle.load(open(f"LDA_/model_{n_exp}.pk", 'rb'))

def cal_top_topics(transform):
    topics = transform.sum(axis = 0)
    return topics

def display_topics(transform, n_exp, n_toptopic = 12):
    fig, axes = plt.subplots(nrows  = 3, ncols = 4, figsize = (4*4.8, 3*3.2))
    topics = cal_top_topics(transform)
    toptopics = topics.argsort()[::-1][:n_toptopic]

    for idx,ax in enumerate(axes.flatten()):
        topic = toptopics[idx]
        docs = transform[:,topic].argsort()[:-51:-1]
        colors = np.zeros((50,48))
        for jdx, doc in enumerate(docs):
            if transform[doc,topic] > 1/K:
                colors[jdx] = coverage_plot.iloc[doc].values/5
        ax.set_xlabel(f"Topic: {topic}")
        ax.set_xticks(np.arange(0,48+12, 12))
        ax.set_xticklabels(np.arange(0,24+6, 6))
        ax.pcolor(colors,cmap = cmap)
    fig.legend(handles = patches)
    fig.supxlabel("24 Hour timeline divided into 30min")
    fig.supylabel("Days related with topics")
    plt.savefig(f"LDA_/topic_{n_exp}.png")
    plt.close()

def log_topic_docs(transform):
    topics = cal_top_topics(transform).argsort()[::-1]
    for topic in topics:
        docs = transform[:,topic].argsort()[::-1]
        print("## Topic ", topic, file = log)
        for doc in docs:
            if transform[doc, topic] > 1/K:
                print(coverage_LDA.index[doc],":", "{:.3f}".format(transform[doc,topic]), file = log)
            else:
                break
def display_topic_word_distribution(model, transform):
    top_topics= cal_top_topics(transform).argsort()[:-12:-1]
    distribution = model.components_ / model.components_.sum(axis=1)[:,np.newaxis]
    for topic in top_topics:
        print('Topic #', topic, file = log)
        tmp = distribution[topic]
        print(*[str(idx).zfill(3) + " " for idx in tmp.argsort()[::-1][:10]], file = log)
        tmp.sort()
        print(*["{:.2f}".format(prob) for prob in tmp[::-1][:10]], file = log)
        print("", file = log)
        print("-"*30, file = log)

def display_doc_topic_distribution(transform):
    top_topics= cal_top_topics(transform).argsort()[:-12:-1]
    for topic in top_topics:
        docs =transform[:,topic].argsort()[:-50:-1]
        print('Topic #', topic, file = log)
        for doc in docs:
            print(f"Doc: {coverage.index[doc]}, Topic Prob: {round(transform[doc,topic],3)}",file = log)
        print("-"*30, file = log)
    

transform = LDA.transform(doc_vec)
display_topics(transform, n_exp = n_exp)
log_topic_docs(transform)
log.close()