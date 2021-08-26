import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster

phone_color = "#ff7f0e"
watch_color = "#1f77b4"

df = pd.read_excel("../Preprocess/all_user.xlsx", index_col = 0)