from datetime import date, timedelta, datetime, timezone
import pandas as pd
import pickle
import os 
import sqlite3

def seqDates(startDate, endDate):
    """ Generate seq of dates with right endpoint not incl """
    daysDiff = (endDate - startDate).days
    dates = [startDate + timedelta(days=i) for i in range(daysDiff)]
    return dates

def format_dates_HHMM(dates, HH, MM, utc_offset_h):
    """ Add HH and MM to dates and format tz to UTC """
    if utc_offset_h >= 0:
        offset = f"+{utc_offset_h:02}00"
    else:
        offset = f"-{-utc_offset_h:02}00"
    dates_str = [d.strftime('%Y-%m-%d') for d in dates]
    dates = [f"{d} {HH:02}:{MM:02}{offset}" for d in dates_str]
    dates = [datetime.strptime(t, "%Y-%m-%d %H:%M%z") for t in dates]
    dates = [t.astimezone(timezone.utc) for t in dates]
    return dates

def makeDFfromDates(dates, country, text='', twsource='health'):
    """ Create a DF from a list of dates in utc tz """
    df = pd.DataFrame({'time' : dates,
                       'text' : text,
                       'measures' : None,
                       'tweet_source' : twsource,
                       'country' : country})
    return df





def saveAllTweets(hlt_tweetsObjs, gov_tweetsObjs):
    tweetsObjs = []
    tweetsObjs.append(hlt_tweetsObjs)
    tweetsObjs.append(gov_tweetsObjs)
    for t in tweetsObjs:
        t.savepklTweets()





    # def savepklTweets(self, fname=None):
    #     if fname is None:
    #         if not os.path.exists('./pkl'):
    #             os.mkdir('./pkl')
    #         fname = f"{self.country}_{self.type}.pkl"   
    #         fname = os.path.join('pkl', fname)
    #     with open(fname, 'wb') as f:
    #         pickle.dump(self.tweets, f)
    
# def loadpklTweets(countries, twtype):
#     twObjs = []
#     for c in countries:
#         fname = f"{c}_{twtype}.pkl"  
#         fname = os.path.join('pkl', fname) 
#         with open(fname, 'rb') as f:
#             tweets = pickle.load(f)
#         twObjs.append(TweetsOfficial(c, tweets, twtype))
#     return twObjs



    
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

# def match_tweets_hashtags(tweets, hashtags):
#     """ Match tweets by hashtags 

#         Matches are not case-sensitive and occur if
#         at least one tweet hashtag is in hashtags

#         Parameters
#         ----------
#         tweets : a list of objs of class Tweet
#         hashtags : a list of hashtags [#htag1, #htag2, ...]

#         Returns
#         -------
#         tweets_ok : a list of objs of class Tweet with matched hashtag
#     """
#     tweets_ok = []
#     hashtags = [h.lower() for h in hashtags]
#     for t in tweets:
#         t_hashtags = t.hashtags.split(" ")
#         t_hashtags = set([h.lower() for h in t_hashtags])
#         if len(t_hashtags.intersection(hashtags)) > 0:
#             tweets_ok.append(t)
#     return tweets_ok



