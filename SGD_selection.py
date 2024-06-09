import pandas as pd
import os

read_path = '/data1/data_clean/'
write_path1 = '/data1/sgd_tweets/sgd_clean/'
write_path2 = '/data1/sgd_tweets/non_sgd_clean/'

# traverse
pre = '(?<!not)(?<!no)(?<!anti)(?<!hate)(?<!against)(?!pro)(?!advocate)'
key = '(lgbt|lesbian|[^a-z]+gay[^a-z]+|bisexual|transgender|[^a-z]+queer[^a-z]+|intersex|asexual|gender minority|sex* minority)'
pos = '(?!not)(?!no)(?!anti)(?!ally)(?!supporter)(?!advocater)(?!friendly)'
pattern = pre + key + pos
data_count = []
for root, dirs, files in os.walk(read_path):
    for name in files:
        if name not in pre_list:
            file_path = os.path.join(read_path, name)
            print('------------%s-----------'%name)
            data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
            print('Total num: %d'%len(data))
            data['sgd'] = data['user'].str.contains(pattern, na=False, case=False)
            sgd_num = len(data[data['sgd']]) # count SGD tweets
            print('sgd num: %d'%sgd_num)
            data_count.append([name,sgd_num]) 
            data[data['sgd']].to_csv(write_path1 + name, index=False)
            data[~data['sgd']].to_csv(write_path2 + name, index=False)
count = pd.DataFrame(data_count,columns=['month','count'])
count.to_csv('sgd_count.csv',index=False)
