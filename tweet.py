import GetOldTweets3 as got
import re
from datetime import date, timedelta
from functions import TweetsOfficial, QueryTweets
import pickle
import pandas as pd 
import translate
# =======================================
#      DOWNLOAD and STORE TWEETS
# =======================================
# time interval for tweets 
# since endDate not included in search must lead date by 1 day
startDate = "2020-01-31"
endDate = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

tweet_dict = {'IT':{'health':"DPCgov", 
                    "gov":"Palazzo_Chigi"},
              "UK":{'health':"DHSCgovuk",
                     "gov":"10DowningStreet"},
              "DE":{'health':"rki_de", 
                    "gov":"RegSprecher"},
              "ES":{'health':"SaludPublicaEs",
                    "gov": "desdelamoncloa"},        
              "FR":{'health':"MinSoliSante",
                    "gov":"Elysee"},
              "US":{'health':"CDCgov",
                    "gov":"whitehouse"},
              "AU":{'health':"healthgovau",
                    "gov":"ScottMorrisonMP"},
              "NZ":{'health':"minhealthnz",
                    "gov":"govtnz"},
              "CA":{'health':"GovCanHealth",
                    "gov":"CanadianPM"},
              "CH":{'health':"BAG_OFSP_UFSP",
                    "gov":"BR_Sprecher"},
              "IN":{'health':"MoHFW_INDIA",
                    "gov":"narendramodi"},
              "SE":{'health':"Folkhalsomynd",
                    "gov":"swedense"},
              "KR":{'health':"TheKoreaHerald",
                    "gov":"TheBlueHouseENG"},
              "CN":{'health':"PDChina",
                    "gov":None},
              "CN-HK":{"health":None,
                       "gov":None},
              "JA":{'health':None,
                    "gov":"JPN_PMO"}}
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
                 "CH":["CoronaInfoCH", "bilan actuel", "point de presse", "live"],
                 "IN":["CoronaVirusUpdates"],
                 "SE":["Uppdaterade", "pressträff"],
                 "KR":['breaking', 'coronavirusupdates'],
                 "CN":['Chinese mainland']}  

country = 'FR'
country_dict = tweet_dict[country]
IT_tweets = QueryTweets(country, 
                        country_dict['health'], 
                        country_dict['gov'])
tweets = IT_tweets.getTweets("2020-03-08", "2020-03-15")
tweetf = tweets.filterTweets(pressrel_dict[country])
df_tweet = tweetf.createDataFrame()
df_tweet.to_csv("ita_tweet.csv", sep=';', index=False,
                encoding='utf-8')

[t.text for t in tweets.gov[3:8]]

from functions import match_tweet_text
matches = match_tweet_text(tweets.gov[3:8],pressrel_dict['IT'] )

is_match(tweets.gov[4].text, pressrel_dict['IT'])



# main health agencies for selected countries
health_dict = {'IT':"DPCgov", 
               "UK":"DHSCgovuk", 
               "DE":"rki_de", 
               "ES":"SaludPublicaEs",
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
gov_dict = {'IT':"Palazzo_Chigi",
            'UK':"10DowningStreet",
            "DE":"RegSprecher",
            "ES":"desdelamoncloa",
            'FR':"Elysee",
            "US":"whitehouse",
            "AU":"ScottMorrisonMP",
            "NZ":"govtnz",
            "CA":"CanadianPM",
            "CH":"BR_Sprecher",
            "IN":"narendramodi",
            "SE":"swedense",
            "KR":"TheBlueHouseENG",   # TheBlueHouseKR
            "CN":None,
            "JA":"JPN_PMO"}

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
                 "CH":["CoronaInfoCH", "bilan actuel", "point de presse", "live"],
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


