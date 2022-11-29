# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:09:36 2022

@author: justp
"""
from urlextract import URLExtract
from wordcloud import WordCloud,STOPWORDS
import pandas as pd
from collections import Counter
import emoji
import re
import matplotlib.pyplot as plt
import string
import io
import os
from os import path
plt.rc('font', family='Segoe UI Emoji')

extract = URLExtract()


def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    # no of msgs    
    num_msgs= df.shape[0]
    
    #total no of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
        
    #no of media
    num_media= df[df['message'] == '<Media omitted>\n'].shape[0]
    
    #no of Links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
        
    return  num_msgs, len(words), num_media, len(links)


def most_interactive_user(df):
        z=df['user'].value_counts().head()
        percentage_df= round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'Name','user':'Percentage'})
        return z,percentage_df
    
def create_wordcloud(selected_user,df):
    
    #read stopwords
    f= open('stop_hinglish.txt','r')
    stop_words= f.read()
    stop_words = STOPWORDS.update(stop_words.split('\n'))
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # remove mdeia and group notification  
    temp =df[df['user']!= 'group notification']
    temp=temp[temp['message'] != '<Media omitted>\n']
    
    #get all emojis
    emojis=[]
    for message in df['message']:
        emojis.extend(emoji.emoji_list(message))
    
    
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    font_path = path.join(d,'seguiemj.ttf')
    
    
    normal_word = r"(?:\w[\w']+)"
    ascii_art = r"(?:[{punctuation}][{punctuation}]+)".format(punctuation=string.punctuation)
    emoji_reg = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
    regexp = r"{normal_word}|{ascii_art}|{emoji_reg}".format(normal_word=normal_word, ascii_art=ascii_art, emoji_reg=emoji_reg)

    
    
    wc= WordCloud(width=500,height=500,min_font_size=10,background_color='white',stopwords=stop_words,font_path=font_path,regexp=regexp)
    temp['message']=temp['message'].apply(remove_emoji)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    
    return df_wc
 
def most_common_words(selected_user,df):
    
    f= open('stop_hinglish.txt','r')
    stop_words= f.read()
    
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
        
    temp =df[df['user']!= 'group notification']
    temp=temp[temp['message'] != '<Media omitted>\n']
    
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    final_df=pd.DataFrame(Counter(words).most_common(20))
    return final_df

    
    
    #remove emoji and links
def remove_emoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    text=re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)

    text = emoji_pattern.sub(r'', text)
    return text
    
    
#emoji analysis
def emoji_analysis(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
        
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        
    emoji_df= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
        
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[] 
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+ str(timeline['year'][i]))
    timeline['time']=time
        
    return timeline

def week_activity_map(selected_user,df):
    
    if selected_user != 'Overall':
        df= df[df['user']==selected_user]
         
    return df['day_name'].value_counts()
    
def month_activity_map(selected_user,df):
    
    if selected_user != 'Overall':
        df= df[df['user']==selected_user]
         
    return df['month'].value_counts()
    
    
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
    