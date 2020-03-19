import GetOldTweets3 as got
import re
from datetime import date, timedelta
import pandas as pd

class TweetsOfficial:
    """ A class to store tweets """ 
    def __init__(self, country, health, gov):
        self.country = country
        self.health = health
        self.gov = gov
    
    def filterTweets(self, keywords):
        """ Filter tweets for keywords """
        hashtags = ["coronavirus", "covid19", 
                    "covid-19", "covid",
                    "COVIDー19"]

        # 1. filter for covid in text   
        # 2. filter for additional keywords     
        attrs = ['health', 'gov']
        lmatch = []
        for a in attrs:
            tweets = getattr(self, a)
            tweets_f1 = match_tweet_text(tweets, hashtags)
            tweets_f2 = match_tweet_text(tweets_f1, keywords)
            lmatch.append(tweets_f2)

        Tweet = TweetsOfficial(self.country,
                               health = lmatch[0],
                               gov = lmatch[1])
        return Tweet

    def createDataFrame(self):
        """ Create dataframe of tweets """
        dfs = []
        attrs = ['health', 'gov']
        for a in attrs:
            tweets = getattr(self, a)
            df = pd.DataFrame()
            df['time'] = [t.date for t in tweets]
            df['text'] = [t.text for t in tweets]
            df['tweet_source'] = a
            df['country'] = self.country
            dfs.append(df)
        df_tweet = pd.concat(dfs, 0)
        return df_tweet


class QueryTweets:
    """ A class to query tweets """
    def __init__(self, countryCode, userHealth, 
                 userGov):
        self.country = countryCode
        self.health = userHealth
        self.gov = userGov

    def getTweets(self, 
                  startDate = "2020-01-31", 
                  endDate = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')):
        tweets = []
        for u in [self.health, self.gov]:
            tweetCriteria = got.manager.TweetCriteria().setUsername(u)\
                                                       .setSince(startDate)\
                                                       .setUntil(endDate)
            if u is not None:
                tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            else:
                tweet = None
            tweets.append(tweet)

        Tweet = TweetsOfficial(self.country, 
                               health=tweets[0],
                               gov=tweets[1])
        return Tweet

def match_tweets_hashtags(tweets, hashtags):
    """ Match tweets by hashtags 

        Matches are not case-sensitive and occur if
        at least one tweet hashtag is in hashtags

        Parameters
        ----------
        tweets : a list of objs of class Tweet
        hashtags : a list of hashtags [#htag1, #htag2, ...]

        Returns
        -------
        tweets_ok : a list of objs of class Tweet with matched hashtag
    """
    tweets_ok = []
    hashtags = [h.lower() for h in hashtags]
    for t in tweets:
        t_hashtags = t.hashtags.split(" ")
        t_hashtags = set([h.lower() for h in t_hashtags])
        if len(t_hashtags.intersection(hashtags)) > 0:
            tweets_ok.append(t)
    return tweets_ok


def is_match(string, patterns):
    """ Find if any pattern in patterns is in string.
        Matches are not case-sensitive.

        Parameters
        ----------
        string : str
        patterns : list, patterns to be matched

        Returns
        -------
        bool
    """
    # warning! re.match matches only at BEGINNING of string -> use re.search
    matches = [re.search(p, string, re.IGNORECASE) for p in patterns]
    is_match = [m is not None for m in matches]
    return any(is_match)

def match_tweet_text(tweets, patterns):
    """ Match tweets by text 

        Matches are not case-sensitive and occur if
        any patter in patterns is found in tweet text

        Parameters
        ----------
        tweets : a list of objs of class Tweet
        patterns : a list of re patterns

        Returns
        -------
        a list of matched objs of class Tweet 
    """
    matches = [is_match(t.text, patterns) for t in tweets]
    return [t for t, m in zip(tweets, matches) if m]
