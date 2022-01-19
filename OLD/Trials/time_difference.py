from util import *

survey = load_survey()
valid_user = list(set(survey.query("invalid !=1")["id"]))

df = pd.read_csv(os.path.join(os.getcwd(),"Data","integrated.csv"), index_col= 0, header = 0)

df = df.query(f"users in {valid_user}")
df = df.set_index(['users', 'timestamp', 'device'])[['step']]
df = df.unstack(level = 2, fill_value = 0)
df.columns = ["phone","watch"]
df = df.reset_index().rename({'level_0':'users', 'level_1':'timestamp'})
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour *2  + df['timestamp'].dt.minute//30

df = df.groupby(["users","date","hour"]).agg(phone=('phone','sum'), watch=('watch','sum'))

df.to_csv("time_difference.csv")