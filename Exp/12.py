from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = loadDF()

total_diff = np.sum(np.abs(df['pstep'] - df['wstep']))

threshold= 100 
df['SPM'] = [step/duration for step, duration in df[['step','duration']].to_numpy()]
exercise = df.query("SPM > 125 or step > 3000")


exercisep = exercise.query("btype =='p'")
print("Phone Exercise Day difference: {:.3f} users: {}, days:{}, avg step:{}".format(np.sum(exercisep['pstep'])/total_diff, len(set(exercisep['uid'])), exercisep.shape[0], np.mean(exercisep['step'])))
# print(exercisep[['uid','date','weekday','hour', 'pstep','SPM']])


exercisew = exercise.query("btype =='w'")
print("Watch Exercise Day difference: {:.3f} users: {}, days:{}, avg step:{}".format(np.sum(exercisew['wstep'])/total_diff, len(set(exercisew['uid'])), exercisew.shape[0], np.mean(exercisew['step'])))
# print(exercisew[['uid','date','weekday','hour', 'wstep','SPM']])


exerciseb = exercise.query("btype =='b'")
print("Both Exercise Day difference: {:.3f} users: {}, days:{}, avg step:{}".format(np.sum(exerciseb['step'])/total_diff, len(set(exerciseb['uid'])), exerciseb.shape[0], np.mean(exerciseb['step'])))
# print(exerciseb[['uid','date','weekday','hour', 'wstep','SPM']])
