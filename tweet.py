import GetOldTweets3 as got
import re
from datetime import date, timedelta
from functions import match_tweets_hashtags, match_tweet_text
import pickle
import pandas as pd 

# =======================================
#      DOWNLOAD and STORE TWEETS
# =======================================
# time interval for tweets 
# since endDate not included in search must lead date by 1 day
startDate = "2020-01-31"
endDate = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

# main health agencies for selected countries
users_dict = {'IT':"DPCgov", 
              "UK":"DHSCgovuk", 
              "DE":"rki_de", 
              "ES":"SaludPublicaEs",
              # "ES_v2":"sanidadgob",
              "FR":"MinSoliSante",
              "US":"CDCgov", 
              "AU":"healthgovau",
              "NZ":"minhealthnz",
              "CA":"GovCanHealth",
              "CH":"BAG_OFSP_UFSP",
              "IN":"MoHFW_INDIA",
              "SE":"Folkhalsomynd",
              "KR":"TheKoreaHerald",
              "CN":"PDChina",
              # "CN-HK":"SCMPNews",  # bad source
              # "JA":"japantimes",   # bad source
              }  
# mycountries =  ['ES']
# users_dict = dict([(key, users_dict[key]) for key in mycountries])

tweets_dicts = dict.fromkeys(users_dict.keys())
for k, v in users_dict.items():
    tweetCriteria = got.manager.TweetCriteria().setUsername(v)\
                                               .setSince(startDate)\
                                               .setUntil(endDate)
    tweets_dicts[k] = got.manager.TweetManager.getTweets(tweetCriteria)

# save tweets to disk 
for k, v in tweets_dicts.items():
    fname = f"tweets_{k}.pkl"   
    with open(fname, 'wb') as f:
        pickle.dump(v, f)

# =======================================
#      PARSE TWEETS for COVID-19
# =======================================
# load tweets from disk
for k in tweets_dicts.keys():
    fname = f"tweets_{k}.pkl"   
    with open(fname, 'rb') as f:
        tweets_dicts[k] = pickle.load(f)

# 1. filter for hashtags without '#' since look at tweet TEXT
#  all matches are case-INsensitive 
hashtags = ["coronavirus", "covid19", "covid-19", "covid",
            "COVIDー19"]
tweets_dict_f = dict.fromkeys(users_dict.keys())
for k, v in tweets_dicts.items():
    tweets_dict_f[k] = match_tweet_text(v, hashtags) 

# 2. filter tweet TEXT for press-briefing 
#  all matches are case-INsensitive
pressrel_dict = {'IT':['diretta', 'aggiornamento', 'aggiornamenti',
                       'conferenza', 'news', 'press-release',
                       'update'], 
                 "UK":['update', 'testing'], 
                 "DE":['pressebriefing', 'aktuelle'], 
                 "ES":['casos', 'actualizados'],
                 "ES_v2":['información', 'actualizada'],
                 "FR":['direct', "Point de situation"],
                 "US":['briefing'],
                 "AU":["update"],
                 "NZ":["update"],
                 "CA":["update", "broadcast", "live"],
                 "CH":["CoronaInfoCH", "bilan actuel"],
                 "IN":["CoronaVirusUpdates"],
                 "SE":["Uppdaterade", "pressträff"],
                 "KR":['breaking', 'coronavirusupdates'],
                 "CN":['Chinese mainland']}  
for k, v in tweets_dict_f.items():
    tweets_dict_f[k] = match_tweet_text(v, pressrel_dict[k])       


# =======================================
#         CREATE TWEETS DATASET
# =======================================
# collapse in data.frame
dfs = []
for k, v, in tweets_dict_f.items():
    df = pd.DataFrame()
    df['time'] = [t.date for t in v]
    df['text'] = [t.text for t in v]
    df['country'] = k
    dfs.append(df)
df_tweet = pd.concat(dfs, 0)
df_tweet.to_csv("df_tweet.csv", sep=';', index=False,
                encoding='utf-8')


