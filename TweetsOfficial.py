import GetOldTweets3 as got
import pandas as pd
import re

class TweetsOfficial:
    """ A class to store and filter tweets """ 
    def __init__(self, country, tweets, twtype):
        self.country = country
        self.type = twtype
        self.tweets = tweets
    
    def filterTweets(self, key_ANY, 
                     key_ALL=None, 
                     match_covid=True):
        """ Filter tweets for keywords """
        # 1. filter for covid in text   
        hashtags = ["coronavirus", "covid19", 
                    "covid-19", "covid",
                    "COVIDー19"]                 
        if match_covid and isinstance(self.tweets, list):
            tweets = match_tweet_text(self.tweets, hashtags)
        else: 
            tweets = self.tweets

        # 2. filter for additional keywords     
        if key_ANY is not None:
            tweets = match_tweet_text(tweets, key_ANY, 'ANY')
        if key_ALL is not None:
            tweets = match_tweet_text(tweets, key_ALL, 'ALL')

        Tweet = TweetsOfficial(self.country,
                               tweets = tweets,
                               twtype = self.type)
        return Tweet

    def createDataFrame(self):
        """ Create dataframe of tweets """
        df = pd.DataFrame()
        df['time'] = [t.date for t in self.tweets]
        df['text'] = [t.text for t in self.tweets]
        df['tweet_source'] = self.type
        df['country'] = self.country
        return df


def downloadTweets(dict_users, 
                   twtype,
                   startDate,
                   endDate):
    tweetsObjs = []
    for k, u in dict_users.items():
        tweetCriteria = got.manager.TweetCriteria().setUsername(u)\
                                                   .setSince(startDate)\
                                                   .setUntil(endDate)
        if u is not None:
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        else:
            tweets = None
        tweetObj = TweetsOfficial(k, tweets, twtype)
        tweetsObjs.append(tweetObj)
    return tweetsObjs


def filter2DataFrame(tweetObjs, dkeys_ANY, dkeys_ALL, 
                     dmatch_covid):
    # filter tweets
    tweetsObjs_f = []
    for t in tweetObjs:
        key_any = dkeys_ANY[t.country]
        key_all = dkeys_ALL[t.country]
        match_cov = dmatch_covid[t.country]
        tf = t.filterTweets(key_any, key_all, match_cov)
        tweetsObjs_f.append(tf)

    # create dataframee
    dfs = []
    for t in tweetsObjs_f:
        if isinstance(t.tweets, list):
            dfs.append(t.createDataFrame())
    
    return pd.concat(dfs, 0)


def is_match(string, patterns, mtype='ANY'):
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
    if mtype == 'ANY':
        is_match = any(is_match)
    else:
        is_match = all(is_match)
    return is_match


def match_tweet_text(tweets, patterns, mtype='ANY'):
    """ Match tweets by text 

        Matches are not case-sensitive and occur if
        any patter in patterns is found in tweet text

        Parameters
        ----------
        tweets : a list of objs of class Tweet
        patterns : a list of re patterns
        mtype : str, either 'ANY' or 'ALL' 

        Returns
        -------
        a list of matched objs of class Tweet 
    """
    matches = [is_match(t.text, patterns, mtype) for t in tweets]
    return [t for t, m in zip(tweets, matches) if m]