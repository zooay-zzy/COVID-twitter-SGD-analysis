# COVID-twitter-SGD-analysis

This repository contains a pipeline of analyzing the concerns and health status of SGD individuals through social media data. The related paper has been published on the [Health Data Science](https://spj.science.org/journal/hds).

### data

The social media data is collected from [Tracking Social Media Discourse About the COVID-19 Pandemic: Development of a Public Coronavirus Twitter Data Set](https://github.com/echen102/COVID-19-TweetIDs).  To filter the tweets and select SGD users, you can run `SGD_selection.py`.

### usage

We analyzed the distribution and dynamics of COVID-related topics, attitudes towards vaccines and the prevalence of symptoms.

* **Topics**: We implemented a Latent Dirichlet Allocation (LDA) topic model.  First, preprocess the raw text by running `python preprocess.py`. Then, execute `python lda_model.py` to run the topic model. To visualize the word frequency distribution of a specific topic, use `Scattertext.py`.
* **Vaccine**: For Named Entity Recognition (NER) and Targeted Sentiment Analysis (TSA) codes, please refer to this repository [YLab-Open/METS-CoV: METS-CoV: a dataset containing Medical Entities and Targeted Sentiments on CoVid-19-related tweets](https://github.com/YLab-Open/METS-CoV). After performing NER and TSA, run `selection.py` to select vaccine targets. To combine different informal expressions of a vaccine brand, execute `brand_count.py`.
* **Symptom**: You can run `symptom.py` to overview the distribution and implement statistical analysis.  Additional codes related to symptom recognition will be uploaded and linked once our other paper is published.
* **Mental health**: To filter mental health symptoms, run `mental_selection.py`. For an overview of the daily distribution of mental health-related tweets, use `daily_count.py`.

 

