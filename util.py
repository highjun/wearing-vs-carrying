import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

color = {'phone':'tab:blue', 'watch':'tab:orange', 'both':'tab:green'}
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def load_bout():
    df = pd.read_csv(os.path.join(os.getcwd(),"Data",'bout.csv'), index_col=0, header = 0)
    df['first'] = pd.to_datetime(df['first'])
    df['last'] = pd.to_datetime(df['last'])
    df['hour'] = df['first'].dt.hour + df['first'].dt.minute/60
    df['date'] = df['first'].dt.date
    df['weekday'] = df['first'].dt.weekday
    df['duration'] = [(row['last']-row['first']).seconds/60+1 for _, row in df.iterrows()]
    df['step'] = [(row['phone']+row['watch'])/(2 if row['bout_type']=='b' else 1)  for _, row in df.iterrows()]
    return df

