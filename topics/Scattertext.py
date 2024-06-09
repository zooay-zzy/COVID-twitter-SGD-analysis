import pandas as pd
import scattertext as st
import spacy
from ast import literal_eval
from pprint import pprint

# read data
read_path = '/data1/sgd_tweets/lda/merge_topic.csv'
write_path = '/data1/lgbt_tweets/scatter_text/version_topic/friend_family.html'
data = pd.read_csv(data_path, low_memory=False, lineterminator="\n")
data = data[data['topic']==1]  # select the topic "friend and family"
#generate corpus
data['tokens'] = data.tokens.apply(lambda x: literal_eval(x))
data['tokens'] = data.tokens.apply(lambda x: list(set(x)))
data['scatter_text'] = data.tokens.apply(lambda x: ' '.join(x))
nlp = spacy.load('en_core_web_sm')
corpus = st.CorpusFromPandas(data,category_col='sgd',text_col='scatter_text',nlp=nlp).build()
# calculate frequency
term_freq_df = corpus.get_term_freq_df()
term_freq_df['general Score'] = corpus.get_scaled_f_scores('non')
term_freq_df['lgbt Score'] = corpus.get_scaled_f_scores('sgd')
html = st.produce_scattertext_explorer(corpus,
                                       category='non',
                                       category_name='non-SGD users',
                                       not_category_name='SGD users',
                                       width_in_pixels=720))
open(write_path, 'wb').write(html.encode('utf-8'))
