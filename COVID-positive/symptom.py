import pandas as pd
import numpy as np
from scipy import stats

read_path1 = '/data1/sgd_tweets/positive/syptom/diagnose_sgd.csv'
read_path2 = '/data1/sgd_tweets/positive/syptom/diagnose_non.csv'
write_path = '/data1/sgd_tweets/positive/syptom/merge_symptom.csv'

sgd = pd.read_csv(read_path1,keep_default_na=False,lineterminator='\n')
non = pd.read_csv(read_path1,keep_default_na=False,lineterminator='\n')

# count related users
g1 = sgd.groupby(['symptom','username']).agg(np.size)['id']
symptom_user = [i[0] for i in g1.index]
user_count = pd.DataFrame(symptom_user,columns = ['user'])
sgd_users = user_count['user'].value_counts()
sgd_users = sgd_users.sort_index() 
g3 = non.groupby(['symptom','username']).agg(np.size)['id']
symptom_user = [i[0] for i in g3.index]
user_count = pd.DataFrame(symptom_user,columns = ['user'])
non_users = user_count['user'].value_counts()
non_users = non_users.sort_index()
# count related tweets
g2 = sgd.groupby('symptom').agg(np.size)['id']
g4 = non.groupby('symptom').agg(np.size)['id']

# merge sgd and non-sgd tweets
sgd = pd.DataFrame({'symptom':sgd_users.index,'user':sgd_users.values,'tweet':g2.values})
non = pd.DataFrame({'symptom':non_users.index,'user':non_users.values,'tweet':g4.values})
merge = pd.merge(sgd,non, on=['symptom'], suffixes=('_sgd','_non'))
symptom_type = sgd.drop(columns=['id', 'date', 'tweet', 'username', 'has_date', 'created_at', 'acc_date\r'])
merge = merge.merge(symptom_type, on=['symptom'], how=('left'))
merge = merge.drop_duplicates(subset=['symptom'])

# calculate chi2 P value
p_value = []
for i in range(len(data)):
    k1 = merge['user_sgd'].iloc[i]
    k2 = merge['user_non'].iloc[i]  
    res = stats.chi2_contingency(np.array([[k1, sgd_users-k1], [k2, non_users-k2]]))
    p_value.append(res[1])
merge['pvalue'] = p_value
merge.to_csv(write_path,index=False)
