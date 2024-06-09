import os
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from ast import literal_eval
from pprint import pprint
import gensim
from gensim.corpora import Dictionary
import pickle
import gensim
import pyLDAvis
import pyLDAvis.gensim_models
import numpy as np
from numpy.polynomial.polynomial import polyfit
import gensim
from gensim import models
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.phrases import Phrases, Phraser
from gensim.corpora import Dictionary
from gensim.models import LdaModel, LdaMulticore, LsiModel, CoherenceModel
import sys

read_path = '/data1/sgd_tweets/lda/input.csv'
output_path = '/data1/sgd_tweets/lda/out.txt'
corpus_path = '/data1/sgd_tweets/lda/corpus/corpus.pkl'

# redirect
current = sys.stdout
fout = open(output_path,'a')
sys.stdout = fout

# Topic modeling
df = pd.read_csv(read_path, keep_default_na=False,low_memory=False, lineterminator="\n")

# convert strings of lists to lists
df.tokens = df.tokens.apply(literal_eval)

data_lemmatized = df.tokens.values.tolist()
dictionary = Dictionary(data_lemmatized)
# changing these numbers can increase/decrease the run time if needed, but too exclusive will lead to worse results
no_below = 20
dictionary.filter_extremes(no_below=no_below, no_above=0.5)
corpus = [dictionary.doc2bow(tokens) for tokens in data_lemmatized]

with open(corpus_path, 'wb') as f: 
    pickle.dump([data_lemmatized,dictionary,corpus], f)


def topic_modeling(num_topics=5):
    np.random.seed(666)
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    chunksize = 10000
    iterations = 100
    passes = 5

    print('topics: {}'.format(num_topics))
    print('interations: {}'.format(iterations))
    print('passes: {}'.format(passes))

    ##Create new model with desired parameters
    # https://radimrehurek.com/gensim/models/ldamulticore.html
    model = LdaModel(
        corpus=corpus,  # leave commented out for batch training, uncomment to train on full corpus at once
        id2word=id2word,
        chunksize=chunksize,
        iterations=iterations,
        passes=passes,
        num_topics=num_topics,
        random_state=0
    )
    model.save('/data1/sgd_tweets/lda/model/topic%i.model'%num_topics)    
    # Compute Perplexity
    print('Perplexity: ', model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=model, texts=data_lemmatized, corpus=corpus,  dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('Coherence: ', coherence_lda)
    # Visualize the topics
    vis = pyLDAvis.gensim_models.prepare(model, corpus, dictionary)
    pyLDAvis.save_html(vis, '/data1/sgd_tweets/lda/vis/topic%d.html'%num_topics)

for num_topics in range(8,30):
    topic_modeling(num_topics=num_topics)
    
# redirect
fout.close()
sys.stdout = current
