import os
import numpy as np
import pandas as pd
import datetime 
import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy.signal import savgol_filter

# count and divide mental health-related tweets
read_path = '/data1/sgd_tweets/mental_new/'
anxiety_count = 0
depression_count = 0
insomnia_count = 0
addiction_count = 0
for root, dirs, files in os.walk(read_path):
    for name in files:
        print(name)
        file_path = os.path.join(read_path, name)
        data = pd.read_csv(file_path,low_memory=False, lineterminator="\n")
        anxiety = data[data['anxiety']]
        depression = data[data['depression']]
        insomnia = data[data['insomnia']]
        addiction = data[data['addiction']]
        g1 = anxiety.groupby(['time']).agg(np.size)['id']
        g2 = depression.groupby(['time']).agg(np.size)['id']
        g3 = insomnia.groupby(['time']).agg(np.size)['id']
        g4 = addiction.groupby(['time']).agg(np.size)['id']
        for i in range(len(g1)):
            anxiety_dict[g1.index[i]] += g1[i]
        for i in range(len(g2)):
            depression_dict[g2.index[i]] += g2[i]
        for i in range(len(g3)):
            insomnia_dict[g3.index[i]] += g3[i]
        for i in range(len(g4)):
            addiction_dict[g4.index[i]] += g4[i]    

# save daily count
anxiety = pd.DataFrame({'time_count': anxiety_dict.keys(), 'col2': anxiety_dict.values()})
depression = pd.DataFrame({'time_count': depression_dict.keys(), 'col2': depression_dict.values()})
insomnia = pd.DataFrame({'time_count': insomnia_dict.keys(), 'col2': insomnia_dict.values()})
addiction = pd.DataFrame({'time_count': addiction_dict.keys(), 'col2': addiction_dict.values()})
anxiety.to_csv('/data1/sgd_tweets/mental_health/anxiety_count.csv',index=False)
depression.to_csv('/data1/sgd_tweets/mental_health/depression_count.csv',index=False)
insomnia.to_csv('/data1/sgd_tweets/mental_health/insomnia_count.csv',index=False)
addiction.to_csv('/data1/sgd_tweets/mental_health/addiction_count.csv',index=False)

