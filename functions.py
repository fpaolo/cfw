import GetOldTweets3 as got
import re
from datetime import date, timedelta
import pandas as pd
import pickle



def saveAllTweets(hlt_tweetsObjs, gov_tweetsObjs):
    tweetsObjs = []
    tweetsObjs.append(hlt_tweetsObjs)
    tweetsObjs.append(gov_tweetsObjs)
    for t in tweetsObjs:
        t.savepklTweets()

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


def downloadTweets(dict_users, 
                   twtype,
                   startDate='2020-01-01',
                   endDate='2020-03-20'):
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

    def savepklTweets(self, fname=None):
        if fname is None:
            fname = f"{self.country}_{self.type}.pkl"   
        with open(fname, 'wb') as f:
            pickle.dump(self.tweets, f)
    
def loadpklTweets(countries, twtype):
    twObjs = []
    for c in countries:
        fname = f"{c}_{twtype}.pkl"   
        with open(fname, 'rb') as f:
            tweets = pickle.load(f)
        twObjs.append(TweetsOfficial(c, tweets, twtype))
    return twObjs


# class QueryTweets:
#     """ A class to query tweets """
#     def __init__(self, countryCode, 
#                  user, 
#                  userGov):
#         self.country = countryCode
#         self.health = userHealth
#         self.gov = userGov

#     def getTweets(self, 
#                   startDate = "2020-01-31", 
#                   endDate = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')):
#         tweets = []
#         for u in [self.health, self.gov]:
#             tweetCriteria = got.manager.TweetCriteria().setUsername(u)\
#                                                        .setSince(startDate)\
#                                                        .setUntil(endDate)
#             if u is not None:
#                 tweet = got.manager.TweetManager.getTweets(tweetCriteria)
#             else:
#                 tweet = None
#             tweets.append(tweet)

#         Tweet_hlt = TweetsOfficial(self.country, 
#                                    tweets[0],
#                                    twtype='health')
#         Tweet_gov = TweetsOfficial(self.country, 
#                                    tweets[1],
#                                    twtype='gov')                                   
#         return [Tweet_hlt, Tweet_gov]

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
