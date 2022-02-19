from util import *

df = load_bout()
total_diff = np.subtract(df['pstep'],df['wstep']).abs().sum()
print("Total Diff: ", total_diff)

df['30min'] = df['first'].dt.hour + (df['first'].dt.minute//30)/2
df['coarse'] = [getCoarseLevel(t)[1] for t in df['30min'].to_numpy()]
tmp = df.query('step > 100')
for tdx in sorted(set(tmp['coarse'])):
    print(tdx, ":", tmp.query(f'coarse == @tdx').shape[0]/tmp.shape[0])
hourly = df.groupby(["uid","date","30min", "btype"]).agg(step = ('step','sum'))
hourly = hourly.unstack(level = 3, fill_value = 0)
hourly.columns = ['b','p','w']
phone = hourly['p'].to_numpy().sum()
watch = hourly['w'].to_numpy().sum()
print(phone/total_diff, watch/total_diff)

hourly['level'] = [getActiveLevel(*steps)[1] for steps in hourly.to_numpy()]
for btype in ['p','w']:
    tmp = hourly[[btype]].unstack(level = 2, fill_value = 0)
    diff_coarse = np.zeros(8)
    for day in tmp.to_numpy():
        # for idx in range(1,47):
        for idx in range(48):
            coarse = getCoarseLevel(idx/2)[1]
            diff_coarse[coarse] += day[idx]
    diff_coarse /= total_diff
    print(diff_coarse)
hourly = hourly[['level']].unstack(level = 2, fill_value = 0)
print("Hourly Shape: ", hourly.shape)
bag_of_words = [{},{},{},{},{},{},{},{}]

for day in hourly.to_numpy():
    # for idx in range(1,47):
    for idx in range(48):
        # word =  str([day[idx-1], day[idx], day[idx+1]])
        word = str(day[idx])
        coarse = getCoarseLevel(idx/2)[1]
        if word in bag_of_words[coarse].keys():
            bag_of_words[coarse][word] += 1
        else:
            bag_of_words[coarse][word] = 1
bag_of_words = [dict(sorted(bag_of_words[i].items(), key=lambda item: item[1], reverse = True)) for i in range(8)]
for i in range(8):
    print("topic", i, "-"*30)
    total = np.sum(list(bag_of_words[i].values()))
    print(*[ (key, "{:3f}".format(val/total)) for key, val in bag_of_words[i].items()], sep = "\n")


