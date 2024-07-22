import streamlit as st
import preprocessor, helper
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)

    # display dataframe
    # st.dataframe(df)


    # fetch unique users
    user_list = np.unique(df['user'])
    # user_list = np.char.strip(user_list,"group_notification")
    user_list = np.insert(user_list,0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    # user_list1 = pd.Series(df['user']).drop_duplicates().tolist()
    # st.sidebar.selectbox("Show analysis wrt",user_list1)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="#27f52b")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['get_date'],daily_timeline['message'],color="#3059f0")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(busy_day.index,busy_day.values,color="#8bed21")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index,busy_month.values,color="#f79831")
            st.pyplot(fig)

        # activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xlabel('Time Period')
        plt.ylabel('Day')
        st.pyplot(fig)

        
        # find the busiest user in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            user_count,percent_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.barh(user_count.index,user_count.values,color='#ac30d9')
                # plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(percent_df)


        # wordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordCloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user,df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)

        # st.dataframe(most_common_df)


        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(),labels= emoji_df['Emoji'].head(),autopct="%0.2f")
            st.pyplot(fig)


        