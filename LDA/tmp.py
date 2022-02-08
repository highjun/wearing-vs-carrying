from util import *

df = load_bout()
# Active Level of Hourly Step Count
df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
hourly = df.groupby(["uid","date","30min"]).agg(step = ('step','sum'))
hourly = hourly.unstack(level = 2, fill_value = 0)
serial = hourly.to_numpy().reshape(-1)

for step in [0, 10, 50, 150]:
    print(np.sum(serial <= step)/serial.shape[0])
# 0이 58%, 10까지가 3%, 50까지가 11%, 150까지가 10%, 그이상이 18%
