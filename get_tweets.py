# Import the libraries
import tweepy
import pandas as pd
import numpy as np
import re
import datetime


keywords = 'shoppe'
region = 'C'
max_items = 500


# Functions
def tweet_con(credentials_file):
    """Connect and authenticate Twitter API"""
    
    log = pd.read_csv(credentials_file)

    consumerKey = log['key'][0]
    consumerSecret = log['key'][1]
    bearerToken = log['key'][2]
    accessToken = log['key'][3]
    accessTokenSecret = log['key'][4]

    # Create the authentication object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret)

    # Create the API object while passing in tne auth information
    api = tweepy.API(authenticate, wait_on_rate_limit = True)

    return api


def cleanTxt(text):
    """Filter undesirable characters"""
    text = re.sub(r'@[_A-Za-z0-9*".]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r':', '', text)

    return text


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


geocoded_dct = {
    "N": "-5.569,-58.858,900km",
    "NE": "-7.96,-38.65,800km",
    "C": "-15.893,-55.595,600km",
    "SE": "-22.368,-41.771,600km",
    "S": "-29.053,-52.764,600km"
}

# Connect to Twitter API
api = tweet_con('Login.txt')


# Getting tweets
tweets = tweepy.Cursor(api.search_tweets,
                       q=keywords,
                       geocode=geocoded_dct[region],
                       lang='pt',
                       count=100,
                       tweet_mode='extended',
                       ).items(max_items)

columns = ['date', 'location', 'username', 'text']
data = []
for tweet in tweets:
    text = cleanTxt(tweet.full_text)
    text = remove_emojis(text)
    data.append([tweet.created_at, tweet.user.location, tweet.user.screen_name, text])
    
df = pd.DataFrame(data, columns=columns)
df.to_csv(f'tweets_filt_{keywords}_{region}.txt', sep='\t', encoding='utf-8', index=False)

print(df)

