import pandas as pd
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt
tknzr = TweetTokenizer()
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import gensim
import spacy
from gensim.models.phrases import Phrases, Phraser
from ast import literal_eval

stopwords_path = '/data1/sgd_tweets/lda/stopwords.txt'
read_path = '/data1/sgd_tweets/lda/corpus.csv'
write_path = '/data1/sgd_tweets/lda/input.csv'

with open(stopwords_path,'r') as f:
    stop_words = f.read().splitlines()
df = pd.read_csv(read_path, keep_default_na=False, lineterminator='\n')
print('finish import')
df["full_text"] = df.full_text.str.replace(r"@[^ ]*|#[^ ]*", '').str.lower()
df = df[~df["full_text"].str.contains('http',na=False, case=False)]
print('finish first filter')
# use NLTK's TweetTokenizer to tokenize the full_text
df["tokens"] = df.full_text.apply(lambda x: tknzr.tokenize(x))
df["tokens"] = df.tokens.apply(lambda x: [t for t in x if len(t) > 2 and t.isalpha() and t not in stop_words])
print('finish second filter')
# lemmatize tokens
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
df["tokens"] = df.tokens.apply(lambda x: [lemmatizer.lemmatize(t) for t in x]) # nltk lemmatize
df["tokens"] = df.tokens.apply(lambda x: [t.lemma_ for t in nlp(" ".join(x))]) # spacy lemmatize
df["count"] = df.tokens.apply(lambda x: len(x))
print('finish lemmatization')
# remove stopwords again
df["tokens"] = df.tokens.apply(lambda x: [t for t in x if len(t) > 2 and t not in stop_words])
print('finish third filter')
# add bigrams
corpus = df.tokens.values.tolist()  # add tokens from each tweet to the corpus
phrases = Phraser(Phrases(corpus)) # default min_count=5
for i in range(len(corpus)): # iterates through the corpus and adds bigram tokens to notes when appropriate, unigram components aren't removed
    bigrams = [token for token in phrases[corpus[i]] if "_" in token]
    corpus[i].extend(bigrams)
print('finish bigram')

corpus = df.tokens.values.tolist()
long_string = ",".join([",".join([
        t for t in c
        if t not in ["covid", "pandemic"]
    ]) for c in corpus])

# save tokens to files
df_token = df[["id", "tokens", "full_text","time",'count','user','geo','sgd']]
df_token = df_token[df_token["count"] >= 5]
print(len(df_token))
df_token.to_csv(write_path, index=False)
