from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # 1. fetching total no of messages
    num_messages = df.shape[0]

    # 2. fetching total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. fetching number of media message
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    # 4. fetching number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

# fetching the most busy users
def most_busy_users(df):
    user_count = df['user'].value_counts().head()
    percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'user':'Name','count':'Percent'})
    return user_count,percent_df


# getting data for wordCloud
def create_wordCloud(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=700,height=700,min_font_size=10,background_color='white')
    new_df = df[df['message'] != '<Media omitted>\n']
    df_wc = wc.generate(new_df['message'].str.cat(sep=" "))
    return df_wc

# getting most common words used
def most_common_words(selected_user,df):

    file = open('stop_hinglish.txt', 'r')
    stop_words = file.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


# getting emoji data
def emoji_helper(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        # Extract emojis from the message
        extracted_emojis = [c for c in message if emoji.is_emoji(c)]
        emojis.extend(extracted_emojis)

    # Create a DataFrame with the count of each emoji occurrence
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0:'Emoji',1:'Count'})

    return emoji_df

# getting monthy timeline
def monthly_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-"+str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

# getting daily timeline
def daily_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('get_date').count()['message'].reset_index()

    return daily_timeline

# getting activity map
def week_activity_map(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    day_name_counts = df['day_name'].value_counts()

    return day_name_counts

def month_activity_map(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    month_name_counts = df['month'].value_counts()

    return month_name_counts

def activity_heatmap(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values= 'message', aggfunc= 'count').fillna(0)

    return user_heatmap