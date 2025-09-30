# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 23:43:10 2022

@author: ivanr
"""


import tweepy
import pandas as pd
import schedule
import time
import json


from analysis import *
from plots import *

#----------------------------
# Authotentication Twitter API

consumer_key = 'yC9Od1Q5MU0hZKY7ZCInwgqyu'
consumer_secret = 'nI53S477CuOJskaZ3pkhLVx0Xbd1xn1J9G1Cg5dkTl0nHztUbY'

access_token = '1511167798688595971-uZhoT9aiHbhUV3fhHVbNafKKAAAfmD'
access_token_secret = 'R4npkSkRlasiKtKwhx6KQYQ9Pp9XHlWslJ5As9HORojOw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#--------------------
#Program

#Set amounts
amount_tts=4 
amount_tws=10

def get_tts():
    
    trending_data = api.get_place_trends(23424747) #(23424747) # Argetina WoeID 
    tts=list()
    
    for trend in trending_data[0]['trends'][:amount_tts]:
        iterator_tws=amount_tws
        if trend['promoted_content'] == None:
            while iterator_tws > 0:
                tts.append(trend['name'])
                iterator_tws -= 1
    
    return tts

def get_tweets():
    tts = get_tts()
    tts_unique=list()
    tweets = list()
    
    for tt in tts:
        if tt not in tts_unique:
            tts_unique.append(tt)
    
    for tt in tts_unique:
        for tweet in tweepy.Cursor(api.search_tweets, q=tt,lang='es',tweet_mode='extended').items(amount_tws):
            tweets.append(tweet.full_text)
    
    #Creating DataFrame
    df = pd.DataFrame(data={'tts':tts,'tweets':tweets,})
    return df


def export(df):
    
    #Cleaning data
    pass
    #df.to_csv(r'C:\ivanr\Desktop\sample.csv', index = False, header=True)
    
    

def new_tweet(tw):
    api.update_status(tw)


def main():

    df = get_tweets()

    df['clean_tweets'] = df.tweets.apply(cleaning)
    df['tokenized'] = df.clean_tweets.apply(nltk.word_tokenize)
    #df['pos'] = df.tokenized.apply(token_stop_pos)

    df['sentiment'] = df.clean_tweets.apply(sentiment_analyse)

    df_analysis = analyze(df)
    
    return df_analysis


if __name__ == '__main__':
    data = main()
    df = get_tweets()

    df['clean_tweets'] = df.tweets.apply(cleaning)
    df['tokenized'] = df.clean_tweets.apply(nltk.word_tokenize)
    #df['pos'] = df.tokenized.apply(token_stop_pos)
    df['sentiment'] = df.clean_tweets.apply(sentiment_analyse)
    df_describe = analyze(df)
    dfs_by_tts = split_by_tt(df, amount_tts,amount_tws)
    
    #Getting Sentiment DataFrame for each TT
    
    df_sent = []
    for i in dfs_by_tts:
        df_sent.append(pos_neg(i))
    
    

    # Create and download one plot for each TT in path ".\images"
    '''
    for tt_sent in df_sent:
        
        #Summarizing data for Pie Chart
        sum = summarize(tt_sent)
        two_plots('prueba',sum, tt_sent)
    '''
    print(df_sent)
    


      

