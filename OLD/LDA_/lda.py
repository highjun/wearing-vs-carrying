from util import *
from sklearn.decomposition import LatentDirichletAllocation
from scipy.sparse import csr_matrix
import matplotlib as mpl
import pickle
import os, shutil
from colorsys import hls_to_rgb as hls2rgb
from itertools import product

df = loadDF()

simulate = True
K = 12 #n_topic
n_exp = 17
if simulate:
    if os.path.exists(f"LDA_/lda{n_exp}.py"):
        print("Same number of experiments exists")
        exit()
    else:
        shutil.copyfile(f"lda.py", f"LDA_/lda{n_exp}.py")
log = open(f"LDA_/result.out","w")


df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
coverage = getBoutInfo(df, ['uid', 'date', 'weekday','30min'])

columns = []
for metric in ['step_ratio', 'step','count_ratio', 'count']:
    for btype in ['b','p','w']:
        columns.append(btype+metric)
columns.append('totalstep')
columns.append('totalcount')

ncolors = 13
color_match = [
    (0, hls2rgb(0,1,0)),
    (1/(ncolors-1), hls2rgb(120/360,80/100,57/100)),
    (2/(ncolors-1), hls2rgb(205/360,90/100,70/100)), 
    (3/(ncolors-1), hls2rgb(28/360,90/100,100/100)), 
    (4/(ncolors-1), hls2rgb(0/360,80/100,0/100)), 

    (5/(ncolors-1), hls2rgb(120/360,60/100,57/100)),
    (6/(ncolors-1), hls2rgb(205/360,70/100,70/100)), 
    (7/(ncolors-1), hls2rgb(28/360,70/100,100/100)), 
    (8/(ncolors-1), hls2rgb(0/360,40/100,0/100)),
    
    (9/(ncolors-1), hls2rgb(120/360,40/100,57/100)),
    (10/(ncolors-1), hls2rgb(205/360,50/100,70/100)), 
    (11/(ncolors-1), hls2rgb(28/360,50/100,100/100)), 
    (12/(ncolors-1), hls2rgb(0/360,0/100,0/100)),
    ]
descriptions = [
    "inactive", 
    *[" ".join([a,b]) for a, b in list(product(["small","middle","large"],["both","phone","watch","not-dominant"]))]]
cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', color_match, len(color_match))
patches = []
import matplotlib.patches as mpatches
for i in range(ncolors):
    patches.append(mpatches.Patch(color = color_match[i][1], label = descriptions[i]))

def get_color(row):
    # White
    if row[columns.index('totalstep')] ==0:
        return 0
    else:
        level = None
        if row[columns.index('totalstep')] < 50:
            level = 0
        elif row[columns.index('totalstep')] < 250:
            level =1
        else:
            level = 2
        if row[columns.index('bstep_ratio')] >.95:
            return level*4+ 1
        # Phone
        elif row[columns.index('pstep_ratio')] >.95:
            return level*4+ 2
        # Watch
        elif row[columns.index('wstep_ratio')] >.95:
            return level*4+ 3
        else:
            return level*4+ 4

# Calcluated Feature for LDA
n_feature = 5
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
        return 4
coverage['color'] = [get_color(row)/12 for row in coverage.values]
coverage['feature_LDA'] = [get_feature(row) for row in coverage.values]
coverage_plot = coverage[['color']].unstack(level = 3, fill_value= 0)
coverage_LDA = coverage[['feature_LDA']].unstack(level = 3, fill_value= 0)
n_timelevel = 4
def get_coarse_level(times:np.ndarray):
    coarse= np.zeros_like(times)
    for cut in [6,12,18]:
        coarse[times>=cut] +=1
    return coarse

def encode(features:list, time:int):
    code = time
    for idx, elem in enumerate(features):
        code += n_timelevel*(n_feature**idx)*elem
    return int(code)
def decode(code:int):
    time = code%n_timelevel
    code //= n_timelevel
    features = []
    while code!=0:
        features.append(code%n_feature)
        code //= n_feature
    return features, time

doc_vec = np.zeros((coverage_LDA.shape[0], n_timelevel*(n_feature**3)))
for doc_idx in range(coverage_LDA.shape[0]):
    day = coverage_LDA.iloc[doc_idx].values
    words = []
    for idx in np.arange(1,47):
        words.append(day[idx-1:idx+2])
    words = list(zip(words, get_coarse_level(np.arange(1,47)/2)))
    for word, time in words:
        doc_vec[doc_idx, encode(word,time)] += 1
        
doc_vec = csr_matrix(doc_vec)
LDA = LatentDirichletAllocation(n_components= K, 
                                max_iter = 1000,
                                learning_method="online",
                                learning_offset=50.0,
                                random_state=0,) #doc_topic_prior= 50 / 30, topic_word_prior= .01)
if simulate:
    print("calculating...")
    fit = LDA.fit(doc_vec)
    print("saving ...")
    pickle.dump(fit, open(f"LDA_/model_{n_exp}.pk", 'wb'))
else:
    print("loading...")
    LDA = pickle.load(open(f"LDA_/model_{n_exp}.pk", 'rb'))

def cal_top_topics(transform):
    topics = transform.sum(axis = 0)
    return topics

def display_topics(transform, n_exp):
    fig, axes = plt.subplots(nrows  = (K+3)//4, ncols = 4, figsize = (4*4.8, 3*3.2))
    topics = cal_top_topics(transform)
    toptopics = topics.argsort()[::-1]

    for idx,ax in enumerate(axes.flatten()):
        topic = toptopics[idx]
        docs = transform[:,topic].argsort()
        plot_docs = []
        for jdx, doc in enumerate(docs):
            if transform[doc,topic] > 1/K:
                plot_docs.append(doc)
        ax.set_xlabel(f"Topic: {topic}")
        ax.set_xticks(np.arange(0,48+12, 12))
        ax.set_xticklabels(np.arange(0,24+6, 6))
        ax.pcolor(coverage_plot.iloc[plot_docs],cmap = cmap)
    fig.legend(handles = patches)
    fig.supxlabel("24 Hour timeline divided into 30min")
    fig.supylabel("Days related with topics")
    plt.savefig(f"LDA_/topic.png")
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
# def display_topic_word_distribution(model, transform):
#     top_topics= cal_top_topics(transform).argsort()[:-12:-1]
#     distribution = model.components_ / model.components_.sum(axis=1)[:,np.newaxis]
#     for topic in top_topics:
#         print('Topic #', topic, file = log)
#         tmp = distribution[topic]
#         print(*[str(idx).zfill(3) + " " for idx in tmp.argsort()[::-1][:10]], file = log)
#         tmp.sort()
#         print(*["{:.2f}".format(prob) for prob in tmp[::-1][:10]], file = log)
#         print("", file = log)
#         print("-"*30, file = log)

# def display_doc_topic_distribution(transform):
#     top_topics= cal_top_topics(transform).argsort()[:-12:-1]
#     for topic in top_topics:
#         docs =transform[:,topic].argsort()[:-50:-1]
#         print('Topic #', topic, file = log)
#         for doc in docs:
#             print(f"Doc: {coverage.index[doc]}, Topic Prob: {round(transform[doc,topic],3)}",file = log)
#         print("-"*30, file = log)
    

transform = LDA.transform(doc_vec)
display_topics(transform, n_exp = n_exp)
log_topic_docs(transform)
log.close()
shutil.copy(f"LDA_/result.out",f"LDA_/result_{n_exp}.out")
shutil.copy(f"LDA_/topic.png",f"LDA_/topic_{n_exp}.png")
