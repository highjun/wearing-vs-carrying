from util import *

sum_th = 100
ratio_th = .1

df = pd.read_csv(os.path.join(os.getcwd(),"time_difference.csv"), header = 0)

df['sum'] = df['phone'].to_numpy() + df['watch'].to_numpy()

df['ratio']  = (df['phone'].to_numpy() - df['watch'].to_numpy())/(df['phone'].to_numpy() + df['watch'].to_numpy())

df = df.query(f'ratio < 1 and ratio > -1 and sum > {sum_th} and ( ratio > {ratio_th} or ratio < {-ratio_th})')


df.to_csv("big_ratio.csv")