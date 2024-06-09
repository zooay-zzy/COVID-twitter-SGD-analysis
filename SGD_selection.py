import pandas as pd
import os

read_path = '/data1/data_clean/'
write_path1 = '/data1/sgd_tweets/sgd_clean/'
write_path2 = '/data1/sgd_tweets/non_sgd_clean/'


# COVID selection
COVID = 'Coronavirus|Koronavirus|Corona|CDC|Wuhancoronavirus|Wuhanlockdown|Ncov|Wuhan|N95|Kungflu|Epidemic|outbreak|Sinophobia|covid-19|corona virus|covid|covid19|sars-cov-2|COVIDー19|pandemic|coronapocalypse|canceleverything|COVD|Coronials|SocialDistancingNow|Social Distancing|SocialDistancing|panicbuy|panic buy|panic buying|panicbuying|14DayQuarantine|DuringMy14DayQuarantine|panic shop|panic shopping|panicshop|InMyQuarantineSurvivalKit|panic-buy|panic-shop|coronakindness|quarantinelife|chinese virus|chinesevirus|stayhomechallenge|stay home challenge|sflockdown|DontBeASpreader|lock down|lockdown|sheltering in place|shelteringinplace|stay safe stay home|staysafestayhome|trumppandemic|trump pandemic|flattenthecurve|flattenthecurve|china virus|chinavirus|quarentinelife|PPEshortage|saferathome|stay at home|stayathome|stay home|stayhome|GetMePPE|covidiot|epitwitter|pandemie|wear a mask|wearamask|kung flu|covididiot|COVID__19'
# SGD selection
pre = '(?<!not)(?<!no)(?<!anti)(?<!hate)(?<!against)(?!pro)(?!advocate)'
key = '(lgbt|lesbian|[^a-z]+gay[^a-z]+|bisexual|transgender|[^a-z]+queer[^a-z]+|intersex|asexual|gender minority|sex* minority)'
pos = '(?!not)(?!no)(?!anti)(?!ally)(?!supporter)(?!advocater)(?!friendly)'
SGD = pre + key + pos
data_count = []

for root, dirs, files in os.walk(read_path):
    for name in files:
        if name not in pre_list:
            file_path = os.path.join(read_path, name)
            print('------------%s-----------'%name)
            data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
            # data cleaning
            data = data[~data['full_text'].str.contains('http', na=False)]  # delete tweets containing URLs
            data = data[data['full_text'].str.contains(COVID, na=False, case=False)]  # select COVID-related tweets
            print('Total num: %d'%len(data))

            # SGD selection
            data['sgd'] = data['user'].str.contains(SGD, na=False, case=False)
            sgd_num = len(data[data['sgd']]) # count SGD tweets
            print('SGD num: %d'%sgd_num)
            data_count.append([name,sgd_num]) 
            data[data['sgd']].to_csv(write_path1 + name, index=False)
            data[~data['sgd']].to_csv(write_path2 + name, index=False)
            
count = pd.DataFrame(data_count,columns=['month','count'])
count.to_csv('sgd_count.csv',index=False)
