import os 
import ast
import datetime
import numpy as np
import pandas as pd

read_path = '/data1/sgd_tweets/vaccine/'
Type = []

for file in os.listdir(read_path):
    file_path = os.path.join(read_path, file)
    data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
    sentiment = data.sentiment.apply(lambda x: ast.literal_eval(x))
    for i in range(len(sentiment)):
        for j in sentiment[i]:
            if j['type'] == 'Vaccine-related' and 'sentiment' in j:
                row = data[['id','user','time','geo','full_text']].iloc[i].tolist()
                row.append(j['value'])
                row.append(j['sentiment'])
                Type.append(row)
              
Select = pd.DataFrame(Type, columns=['id','user','time','geo','full_text','value','sentiment','sgd'])
Select = Select.drop_duplicates(['id','value'],keep='first')  # when the same entity is mentioned multiple times in one tweets, retain the first one
print(len(Select))
Select.to_csv('/data1/lgbt_tweets/vaccine/vaccine.csv',index=False)
