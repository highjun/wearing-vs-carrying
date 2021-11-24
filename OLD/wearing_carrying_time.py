from numpy import histogram, pi
from Experiment.util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
df['hour'] = df['first'].dt.hour
df['date'] = df['first'].dt.date
df['weekday'] = df['first'].dt.weekday
df['duration'] = [(row['last']-row['first']).seconds/60+1 for _, row in df.iterrows()]
df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
users = list(set(df['users']))
picture = True
carry_th = 5
wear_th = 100
if picture:
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (6,12))
type = ['phone','watch','both']
data = [[],[],[]]
def time(date, dt_):
    dt_date = dt_.date()
    if dt_date > date:
        return 24
    time = dt_.time()
    return time.hour + time.minute/60
for idx,user in enumerate(users):
    if picture:
        user = 20
    tmp = df.query(f"users=={user}")
    day = 0
    total_w = 0
    total_c = 0
    total_b = 0
    for date in sorted(set(tmp["date"])):
        w_time = []
        c_time = []
        wearing = None
        w_th = 0
        carrying = None
        c_th = 0
        tmp_ = tmp[tmp["date"]== date]
        for _, row in tmp_.iterrows():
            if row["bout_type"] == 'p':
                if wearing is not None:
                    w_th += row["step"]
                    if w_th > wear_th:
                        w_time.append(wearing)
                        wearing = None
                        w_th = 0
                if carrying is not None:
                    carrying[1] = time(date,row["last"])
                    c_th = 0
                else:
                    carrying = [time(date,row["first"]), time(date,row["last"])]
                    c_th = 0
            elif row["bout_type"] == 'w':
                if carrying is not None:
                    c_th += row["step"]
                    if c_th > carry_th:
                        c_time.append(carrying)
                        carrying = None
                        c_th = 0
                if wearing is not None:
                    wearing[1] = time(date,row["last"])
                    w_th = 0
                else:
                    wearing = [time(date,row["first"]), time(date,row["last"])]
                    w_th = 0
            else:
                if carrying is not None:
                    carrying[1] = time(date,row["last"])
                    c_th = 0
                else:
                    carrying = [time(date,row["first"]),time(date,row["last"])]
                    c_th = 0
                if wearing is not None:
                    wearing[1] = time(date,row["last"])
                    w_th = 0
                else:
                    wearing = [time(date,row["first"]),time(date,row["last"])]
                    w_th = 0
            print(c_th,w_th, row)
        if carrying is not None:
            c_time.append(carrying)
        if wearing is not None:
            w_time.append(wearing)
        w_time = np.array(w_time)
        c_time = np.array(c_time)
        if picture:
            if len(w_time) > 0:
                ax.hlines(np.ones(len(w_time))+2*day, xmin= w_time[:,0] , xmax = w_time[:,1], colors = [color["watch"]]*len(w_time))
            if len(c_time) > 0:
                ax.hlines(np.zeros(len(c_time))+2*day, xmin= c_time[:,0] , xmax = c_time[:,1], colors = [color["phone"]]*len(c_time))
        
        total_w += np.sum([t[1]-t[0] for t in w_time])
        total_c += np.sum([t[1]-t[0] for t in c_time])
        start = 0
        for w0,w1 in w_time:
            for c0,c1 in c_time:
                if (w0-c0)*(w1-c0)<=0:
                    if (w0-c1)*(w1-c1) <= 0:
                        total_b+= c1-c0
                    else:
                        total_b+= w1-c0
                else:
                    if (w0-c1)*(w1-c1) < 0:
                        total_b += c1-w0
                    else:
                        if (c1-w0)*(c0-w0)<0:
                            total_b += w1-w0
        day += 1
    print(f"{user}: carry= {total_c/day}, wear = {total_w/day} both={total_b/day}")
    data[0].append(total_b)
    data[1].append(total_c-total_b)
    data[2].append(total_w-total_b)
    if picture:
        break
if not picture:
    data = np.array(data)
    datacum = data.cumsum(axis = 0)
    fig, ax = plt.subplots(nrows = 1, ncols = 1)
    ax.barh(np.arange(.5, len(users)+.5),width = data[0], color=color["both"], label="both")
    ax.barh(np.arange(.5, len(users)+.5),width = data[1],left =datacum[0], color=color["phone"], label="phone")
    ax.barh(np.arange(.5, len(users)+.5),width = data[2],left =datacum[1], color=color["watch"], label="watch")
    ax.set_yticks(np.arange(.5,len(users)+.5))
    ax.set_yticklabels(users)
    ax.set_xlabel("Total Time")
    ax.set_ylabel("Participants")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(os.getcwd(),"New", f"time_ratio.png"))

if picture:    
    ax.set_xticks(np.arange(0,25))
    ax.set_ylim([-1,day*2])
    ax.set_xlim([-1,25])
    ax.vlines([0,6,12,18,24], ymin = -1, ymax = day*2, colors =(1,0,0,0.5))
    ax.hlines(np.arange(1.5, day*2, 2), xmin = -1, xmax = 25, colors = (0,0,0,0.2), linestyles='--')
    ax.set_yticks(np.arange(.5, day*2+.5, 2))
    weekday = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    ax.set_yticklabels([str(date.month)+"-"+str(date.day) +"," + weekday[date.weekday()] for date in sorted(set(tmp["date"]))])
    ax.set_ylabel('')
    ax.set_xlabel('''Hour

    Wearing/Carrying time''')
    plt.tight_layout()
    plt.savefig(os.path.join(os.getcwd(),"New", f"{cur}.png"))

