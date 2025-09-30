# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:16:23 2022

@author: ivanoaks
"""

from main import *
from analysis import *

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import os
if not os.path.exists("images"):
    os.mkdir("images")
# pip install -U kaleido

#-------------------------------
'''
df = get_tweets()

df['clean_tweets'] = df.tweets.apply(cleaning)
df['tokenized'] = df.clean_tweets.apply(nltk.word_tokenize)
#df['pos'] = df.tokenized.apply(token_stop_pos)
df['sentiment'] = df.clean_tweets.apply(sentiment_analyse)

df_describe = analyze(df)

dfs_by_tts = split_by_tt(df, amount_tts,amount_tws)

df_sent = []
for i in dfs_by_tts:
    df_sent.append(pos_neg(i))
'''

#-------------------------------

def summarize(df):
    df = pd.DataFrame(df)
    amount_neg = 0
    amount_neu = 0
    amount_pos = 0
    
    for i in range(0,df.shape[0]):
        if df.iloc[i][0] > df.iloc[i][2]:
            amount_neg+=1
        elif df.iloc[i][0] < df.iloc[i][2]:
            amount_pos+=1
        else:
            amount_neu+=1
    
    return [amount_neg,amount_neu,amount_pos]


def two_plots(tt, df_pie, df):
    fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.65, 0.35],
    #row_heights=1,
    specs=[[{"type": "histogram"}, {"type": "pie"}]],
    )

    # Tracing plots

    # Pie
    fig.add_trace(
        go.Pie(values=df_pie,
        labels=['Negatividad', 'Neutralidad', 'Positividad'],
        marker=dict(colors=['#FA4A4A','#DBF2FD','#1DF071']),
        ), 
        
        row=1, col=2
    )

    fig.update_layout(
    template="plotly_dark",
    margin=dict(r=80, t=100, b=100, l=60),
    width=1200,
    height=675,
    title={
        'text': "Tendencia {}".format(tt.upper()),
        'xanchor': 'center',
        'yanchor': 'top',
        'y':0.98,
        'x':0.5,
        'font_color':'#9F87FF' ,
        'font_family':'Courier New',},
    )

    # Histogram

    fig.add_trace(

        go.Histogram(x=df["compound"],marker_color='#9A85F0', histnorm='percent',
                    opacity=0.75, showlegend=False, nbinsx=int(len(df["compound"])/3),
        ),
        row=1, col=1,  
    )

    # kde
    '''
    fig.add_traces(go.Scatter(x=df["compound"],histnorm='percent' ,mode = 'lines', 
                  line = dict(color='rgba(0,255,0, 0.6)',width = 1),
                  name = 'normal',showlegend=False),
                  row=1, col=1)
    '''
    fig.update_xaxes(range=[-1,1], row=1, col=1)
    fig.update_yaxes(ticksuffix="%", row=1, col=1)
    fig.write_image(f"images/{tt}.png")



#sum = summarize(df_sent[0])
#two_plots('prueba',sum, df_sent[0])

#print(df_sent[0])

#define data



