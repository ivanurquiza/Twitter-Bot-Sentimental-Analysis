# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:16:23 2022

@author: ivanr
"""
#import csv
import string
import re
import emoji

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from googletrans import Translator


#nltk.download('vader_lexicon')
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('averaged_perceptron_tagger')
import pandas as pd

from main import *
#--------------------------------------------------

#df = get_tweets()

#Data Cleaning

stopwordsList = stopwords.words("Spanish") + list(string.punctuation) + ['“','”','¡','¿',"''",'``','...','→','⬥','…']

def cleaning(text):
    
    #stopwordsList = stopwords.words("Spanish") + list(string.punctuation) + ['“','”','¡','¿',"''",'``','...','→','⬥','…']    
    
    def clean_emoji(text):
        allchars = [str for str in text]
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
        
        return clean_text
    
    def clean_regex(text):
        tweet = re.sub(r'@[a-zA-Z0-9-_.]+', '', text)
        tweet = re.sub(r'#[a-zA-Z0-9-_.]+', '', tweet)
        tweet = re.sub(r'//[a-zA-Z0-9-_.]+', '', tweet)
        tweet = re.sub(r'https://[a-zA-Z0-9-_./]+', '', tweet)
        tweet = re.sub(r'https:[a-zA-Z0-9-_./]+', '', tweet)
        tweet = re.sub(r'www.[a-zA-Z0-9-_./]+', '', tweet)
        tweet = re.sub(r'[a-zA-Z0-9-./]+[…]', '', tweet)
        tweet = re.sub(r'[ ]+[…]', '', tweet)
        tweet = re.sub('\n|\r', '', tweet)
        tweet = re.sub(r'[á|ä|â|à]', 'a', tweet)
        tweet = re.sub(r'[é|ê|è]', 'e', tweet)
        tweet = re.sub(r'[í|î|ì]', 'i', tweet)
        tweet = re.sub(r'[ó|ô|ò]', 'o', tweet)
        tweet = re.sub(r'[ú|û|ù|ü]', 'u', tweet)
        tweet = re.sub(r'RT ', '', tweet)
        tweet = re.sub(r'[:|,]', '', tweet)
        return tweet
    
    tweet_clean = clean_regex(clean_emoji(text)).lower()
    
    
    translator = Translator()
    trans = translator.translate(tweet_clean, dest='en')

    return trans.text

# POS and tokenization
def tokenize(text):
    tags = nltk.word_tokenize(text)
    newlist=list()
    for word, tag in tags:
        if word not in stopwordsList:
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist


# Dictionary created for converting POS data in letters understood by SnowballStemmer
pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN}


def token_stop_pos(text):
    tags = nltk.pos_tag(text)
    newlist=list()
    for word, tag in tags:
        if word not in stopwordsList:
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist


def sentiment_analyse(text):
    score = SentimentIntensityAnalyzer()
    return score.polarity_scores(text)


def analyze(df):
    data = pd.DataFrame({'tts':df.tts,
                            'neg':df.sentiment.apply(lambda x: x['neg']),
                            'neu':df.sentiment.apply(lambda x: x['neu']),
                            'pos':df.sentiment.apply(lambda x: x['pos']),
                            'compound':df.sentiment.apply(lambda x: x['compound'])})
    df_analysis = data.groupby(by='tts', axis=0).agg(['mean','median', 'sum', 'count'])
    return df_analysis

def split_by_tt(df, amount_tts, amount_tws):
    '''
    Split the main DataFrame by Trending Topic.
    The output is a list that contains one value for each TT.
    '''
    '''
    dataframes = []
    for i in df: 
        dataframes.append(df.iloc[:amount_tws])
        amount_tts-=1
        if amount_tts==0: break
    '''
    dataframes = []
    iter=amount_tts*amount_tws
    for i in df: 
        dataframes.append(df.iloc[:amount_tws])
        df.drop(df.index[range(amount_tws)], inplace=True)
        iter -= amount_tws
        if iter<=0: break
    

    return dataframes


def pos_neg(df):
    '''
    Takes only the sentiment field and gets a DataFrame with neg, neu and pos rates.
    '''
    tt, neg, neu, pos, comp = [],[],[],[],[]

    for dic in df.sentiment:
        tt.append(dic['tts'])
        neg.append(dic['neg'])
        neu.append(dic['neu'])
        pos.append(dic['pos'])
        comp.append(dic['compound'])

    df_analysis = pd.DataFrame([tt,neg,neu,pos,comp]).T
    df_analysis.columns = ['tt','neg', 'neu', 'pos','compound']
    return df_analysis

'''
df['clean_tweets'] = df.tweets.apply(cleaning)
df['tokenized'] = df.clean_tweets.apply(nltk.word_tokenize)
#df['pos'] = df.tokenized.apply(token_stop_pos)

df['sentiment'] = df.clean_tweets.apply(sentiment_analyse)

df_analysis = analyze(df['sentiment'])
'''