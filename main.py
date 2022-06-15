# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 23:43:10 2022

@author: ivanr
"""


import tweepy
import pandas as pd
import schedule
import time
#import json
import sys
import os

from analysis import *
from plots import *

#----------------------------
# Authotentication Twitter API

consumer_key = '#'
consumer_secret = '#'

access_token = '#'
access_token_secret = '#'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#--------------------
#Program

#Set amounts
amount_tts=3
amount_tws=500

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


def new_tweet(text, filename):
    media = api.media_upload(filename)
    api.update_status(text, media_ids = [media.media_id_string])


def volume_info(tt):
    trending_data = api.get_place_trends(23424747) #(23424747) # Argetina WoeID
    tts=list()

    for trend in trending_data[0]['trends'][:amount_tts]:
        iterator_tws=amount_tws
        if trend['promoted_content'] == None:
            while iterator_tws > 0:
                tts.append(trend['name'])
                iterator_tws -= 1

    for trend in trending_data[0]['trends'][:amount_tts]:
        if trend['name'] == tt:
            return trend['tweet_volume']

#remove = lambda os.remove(x) for x in

def main():
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

    files = {}


    try:

        for tt_sent in df_sent:

            #Summarizing data for Pie Chart
            sum = summarize(tt_sent)
            two_plots(tt_sent['tt'][0],sum, tt_sent)
            files[tt_sent['tt'][0]]=f"images/{tt_sent['tt'][0]}_{date.today()}.png"

        for tt,file in files.items():

            volume = volume_info(tt)


            with open('tts.txt', 'r+') as txt:
                text = txt.read()

                # Run the script just in case this TT was not analyzed yet

                if tt not in text:
                    txt.write(f'\n{tt}')

                    #Writing text depending on if variable volume exists

                    if volume != None:
                        text = f'Análisis sentimental para el TT: {tt}\nTotal de {volume_info(tt)} tweets publicados'
                    else:
                        text = f'Análisis sentimental para el TT: {tt}'

                    #Publishing results
                    try:
                        new_tweet(text, file)
                        print(tt,' DONE')
                    except:
                        print('Ha ocurrido un error en el análisis. Error: ', sys.exc_info()[0])
                    time.sleep(30)
                else:
                    txt.write(f'\nDUPLICATED {tt}')
                    print(f'DUPLICATED {tt}')
                    try:
                        if volume != None:
                            api.update_status(f'{tt.upper()} se mantiene como Trending Topic con un volumen actual de {volume_info(tt)} tweets.')
                        else:
                            api.update_status(f'{tt.upper()} se mantiene como Trending Topic.')

                    except:
                        print('Already tweeted')

        # Remove all tts from txt file at 13 pm
        if time.localtime().tm_hour == 13:
            with open('tts.txt', 'w') as txt:
                txt.write(' ')


    except FileNotFoundError:
        print("The 'docs' directory does not exist")

if __name__ == '__main__':
    main()

