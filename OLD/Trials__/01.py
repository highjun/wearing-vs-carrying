# 사람들은 규칙적인 걸음 수 패턴을 가지나?

from util import *

df = pd.read_csv("Data/integrated.csv", index_col = 0)
df['timestamp'] = pd.to_datetime(df['timestamp'])

users = list(set(df["users"]))

user = users[0]
df = df.query("users==@user and weekday < 5 and device =='phone'")

fig, ax = plt.subplots(figsize= (100, 4))
plt.plot(df['timestamp'], df["step"])
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 6))
# set formatter
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
plt.savefig("tmp.png")
