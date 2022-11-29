# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 12:05:15 2022

@author: justp
"""
import streamlit as st
import preprocessor
import hmmhmm
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt

plt.rc('font', family='Segoe UI Emoji')

st.sidebar.title("Whatsapp Chat Analyzer")

file= st.sidebar.file_uploader('Choose a file')
if file is not None:
    bytes_data= file.getvalue()
    data= bytes_data.decode('utf-8')    
    df= preprocessor.preprocess(data)
    
    #st.dataframe(df)
    
    
    user_list= df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user=st.sidebar.selectbox("Show Analysis for: ", user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        num_messages,words,num_media,num_links= hmmhmm.fetch_stats(selected_user,df)
        
        st.title('Top  Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
            
        with col2:
            st.header("Total Words")
            st.title(words)
            
        with col3:
            st.header("Media Shared")
            st.title(num_media)
            
        with col4:
            st.header("Links Shared")
            st.title(num_links)
            
            
        #timeline
        timeline=hmmhmm.monthly_timeline(selected_user, df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color='green')
        ax.set_xticks(ax.get_xticks()[::2])
        plt.xticks(rotation='vertical')
        x=timeline['time']
        y=timeline['message']
        for index in range(0,len(x)):
            ax.text(x[index], y[index], y[index], size=6)
        st.pyplot(fig)
        
        
        #activity map
        st.title('Activity Map')
        col1,col2= st.columns(2)
        
        with col1:
            st.header('Most Active Day')
            active_day= hmmhmm.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(active_day.index, active_day.values)
            x=active_day.index
            y=active_day.values
            plt.xticks(rotation='vertical')
            for index in range(0,len(x)):
                ax.text(x[index], y[index], y[index], size=12)
            st.pyplot(fig)
        with col2:
            st.header('Most Active Month')
            active_month= hmmhmm.month_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(active_month.index, active_month.values,color='orange')
            plt.xticks(rotation='vertical')
            x=active_month.index
            y=active_month.values
            for index in range(0,len(x)):
                ax.text(x[index], y[index], y[index], size=12)
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        user_heatmap = hmmhmm.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

            
            
        #interactive user
        if selected_user == 'Overall':
            st.title('Most Interactive Users')
            x,perc_df= hmmhmm.most_interactive_user(df)
            fig,ax= plt.subplots()
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(perc_df)
            
                
        df_wc= hmmhmm.create_wordcloud(selected_user, df)
        fig, ax= plt.subplots()
        plt.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)
            
        #most common words
        most_common_df=hmmhmm.most_common_words(selected_user, df)
        fig,ax = plt.subplots()
        
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)
        
        #emoji analysis
        emoji_df = hmmhmm.emoji_analysis(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

    
    