from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]
df = load_bout()
survey  =load_survey()
users = set(survey.query("invalid != 1")["id"])

df = df.query(f"users in {list(users)}")

nrows = 4
ncols = 2
fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = (6.4*ncols, 4.8*nrows))

    
type2int = {"n":1, "p":1,"w":2,"b":2}
data = []

track_user = list(survey.query("track == 1")["id"])
track_not_user = list(survey.query("old == 0 and track == 0")["id"])

track_y = df.query(f"users in {track_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
track_y = np.array(track_y.unstack('bout_type', fill_value = 0))
track_n = df.query(f"users in {track_not_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
track_n = np.array(track_n.unstack('bout_type', fill_value = 0))
ax[0][0].boxplot([(track_y[:,0]+track_y[:,1])/np.sum(track_y, axis = 1),(track_n[:,0]+track_n[:,1])/np.sum(track_n, axis = 1)], labels=["track", "not"])
ax[0][1].boxplot([(track_y[:,0]+track_y[:,2])/np.sum(track_y, axis = 1),(track_n[:,0]+track_n[:,2])/np.sum(track_n, axis = 1)], labels=["track", "not"])
ax[0][0].set_ylabel("Ratio")
ax[0][0].set_xlabel("Phone")
ax[0][1].set_xlabel("Watch")

notf_user = list(survey.query("notf == 1")["id"])
notf_not_user = list(survey.query("old == 0 and notf == 0")["id"])

notf_y = df.query(f"users in {notf_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
notf_y = np.array(notf_y.unstack('bout_type', fill_value = 0))
notf_n = df.query(f"users in {notf_not_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
notf_n = np.array(notf_n.unstack('bout_type', fill_value = 0))
ax[1][0].boxplot([(notf_y[:,0]+notf_y[:,1])/np.sum(notf_y, axis = 1),(notf_n[:,0]+notf_n[:,1])/np.sum(notf_n, axis = 1)], labels=["notf", "not"])
ax[1][1].boxplot([(notf_y[:,0]+notf_y[:,2])/np.sum(notf_y, axis = 1),(notf_n[:,0]+notf_n[:,2])/np.sum(notf_n, axis = 1)], labels=["notf", "not"])
ax[1][0].set_ylabel("Ratio")
ax[1][0].set_xlabel("Phone")
ax[1][1].set_xlabel("Watch")

survey["day"]= [type2int[idx] for idx in  survey["cw_day"]]
survey["night"]= [type2int[idx] for idx in  survey["cw_night"]]
always_user = list(survey.query("day ==2 and night == 2")["id"])
day_user = list(survey.query("day == 2 and night == 1")["id"])
no_user = list(survey.query("day == 1 and night == 1")["id"])

always_ = df.query(f"users in {always_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
always_ = np.array(always_.unstack('bout_type', fill_value = 0))
day_ = df.query(f"users in {day_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
day_ = np.array(day_.unstack('bout_type', fill_value = 0))
no_ = df.query(f"users in {no_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
no_ = np.array(no_.unstack('bout_type', fill_value = 0))
ax[2][0].boxplot([(always_[:,0]+always_[:,1])/np.sum(always_, axis = 1),(day_[:,0]+day_[:,1])/np.sum(day_, axis = 1),(no_[:,0]+no_[:,1])/np.sum(no_, axis = 1)], labels=["always", "day","no"])
ax[2][1].boxplot([(always_[:,0]+always_[:,2])/np.sum(always_, axis = 1),(day_[:,0]+day_[:,2])/np.sum(day_, axis = 1),(no_[:,0]+no_[:,2])/np.sum(no_, axis = 1)], labels=["always", "day","no"])
ax[2][0].set_ylabel("Ratio")
ax[2][0].set_xlabel("Phone")
ax[2][1].set_xlabel("Watch")


type2int = {"n":0, "p":1,"w":0,"b":1}
survey["day"]= [type2int[idx] for idx in  survey["cw_day"]]
survey["night"]= [type2int[idx] for idx in  survey["cw_night"]]
always_user = list(survey.query("old == 0 and day ==1 and night == 1")["id"])
day_user = list(survey.query("old == 0 and day==1 and night == 0")["id"])
night_user = list(survey.query("old == 0 and day==0 and night == 1")["id"])
no_user = list(survey.query("old == 0 and day==0 and night == 0")["id"])

always_ = df.query(f"users in {always_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
always_ = np.array(always_.unstack('bout_type', fill_value = 0))
day_ = df.query(f"users in {day_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
day_ = np.array(day_.unstack('bout_type', fill_value = 0))
night_ = df.query(f"users in {night_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
night_ = np.array(night_.unstack('bout_type', fill_value = 0))
no_ = df.query(f"users in {no_user}").groupby(["users","bout_type"]).agg(step =("step","sum"))
no_ = np.array(no_.unstack('bout_type', fill_value = 0))
ax[3][0].boxplot([(always_[:,0]+always_[:,1])/np.sum(always_, axis = 1),(day_[:,0]+day_[:,1])/np.sum(day_, axis = 1),(night_[:,0]+night_[:,1])/np.sum(night_, axis = 1),(no_[:,0]+no_[:,1])/np.sum(no_, axis = 1)], labels=["always", "day","night","no"])
ax[3][1].boxplot([(always_[:,0]+always_[:,2])/np.sum(always_, axis = 1),(day_[:,0]+day_[:,2])/np.sum(day_, axis = 1),(night_[:,0]+night_[:,2])/np.sum(night_, axis = 1),(no_[:,0]+no_[:,2])/np.sum(no_, axis = 1)], labels=["always", "day","night","no"])
ax[3][0].set_ylabel("Ratio")
ax[3][0].set_xlabel("Phone")
ax[3][1].set_xlabel("Watch")


plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(),"Figures", f"{cur}.png"))  
