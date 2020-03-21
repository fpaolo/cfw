import GetOldTweets3 as got
import re
from datetime import date, timedelta, datetime, timezone
from functions import downloadTweets, loadpklTweets
from functions import filter2DataFrame 
import pickle
import pandas as pd 

# =======================================
#      DOWNLOAD and STORE TWEETS
# =======================================
# time interval for tweets 
# since endDate not included in search must lead date by 1 day
startDate = "2020-01-31"
endDate = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

hlt_users = {'IT':"DPCgov", 
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
            #  "CN-HK":None,  # "SCMPNews"
            #  "JA":None,   #"japantimes"
            } 
gov_users = {'IT':"Palazzo_Chigi",
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
            #  "CN":None,
            #  "CN-HK":None,
             "JA":"JPN_PMO"}

# # download tweets
# hlt_tweetsObjs = downloadTweets(hlt_users, 'health')
# gov_tweetsObjs = downloadTweets(gov_users, 'gov')

# # save tweets
# saveAllTweets(hlt_tweetsObjs, gov_tweetsObjs)


# ===================================
#         HEALTH AGENCIES
# ===================================    
# create keywords to match relevant tweets (hopefully)        
hlt_keys_ALL = {'IT':['diretta'], 
                "UK":['update', 'testing'], 
                "DE":['pressebriefing', 'aktuelle'], 
                "ES":['casos', 'actualizados'],
                "FR":['direct', "Point de situation"],
                "US":['briefing'],
                "AU":["update"],
                "NZ":["update"],
                "CA":["update", "broadcast", "live"],
                "CH":["CoronaInfoCH", "bilan actuel"],
                "IN":["CoronaVirusUpdates"],
                "SE":["Uppdaterade", "pressträff"],
                "KR":['breaking'],
                "CN":['Chinese mainland'],
                # "CN-HK":None,
                # "JA":None
                }  
hlt_keys_ANY = hlt_keys_ALL
hlt_match_covid = dict.fromkeys(hlt_users)
for k in hlt_match_covid.keys():
    hlt_match_covid[k] = True

# load tweets
hlt_tweetsObjs = loadpklTweets(hlt_users.keys(), 'health')

# filter tweets
df_hlt = filter2DataFrame(hlt_tweetsObjs, hlt_keys_ANY,
                          hlt_keys_ALL, hlt_match_covid)


# =================================================
#               GOVERNMENT
# ================================================ 
# create keywords to match relevant tweets (hopefully)        
gov_keys_ANY = {'IT':['diretta', 'live', 'broadcast'], 
                "UK":['watch live'], 
                "DE":['konferenz'], 
                "ES":['live', 'directo'],
                "FR":['direct', "Point de situation","adresse"],
                "US":['live', 'press','briefing'],
                "AU":["update"],
                "NZ":["update"],
                "CA":["update", "broadcast", "live"],
                "CH":["stampa"],
                "IN":["CoronaVirusUpdates"],
                "SE":["Uppdaterade", "pressträff"],
                "KR":['breaking'],
                # "CN":None,
                # "CN-HK":None,
                "JA":['update']}  
# gov_keys_ANY = dict.fromkeys(gov_users)
# for k in gov_keys_ANY.keys():
#     gov_keys_ANY[k] = ['update', 'briefing', 'live', 'watch',
#                        'broadcast', 'direct', 'directo',
#                        'pressbriefing']   
gov_keys_ALL = dict.fromkeys(gov_users)
for k in gov_keys_ALL.keys():
    gov_keys_ALL[k] = None
#gov_keys_ALL = gov_keys_ANY
gov_match_covid = dict.fromkeys(gov_users)
for k in gov_match_covid.keys():
    gov_match_covid[k] = True
gov_match_covid['IT'] = False
gov_match_covid['AU'] = False
gov_match_covid['IN'] = False
gov_match_covid['SE'] = False

# load tweets
gov_tweetsObjs = loadpklTweets(gov_users.keys(), 'gov')

# filter tweets
df_gov = filter2DataFrame(gov_tweetsObjs, gov_keys_ANY,
                          gov_keys_ALL, gov_match_covid)



import os 
if not os.path.exists('./pkl'):
    os.mkdir('./pkl')
    print('evvva')

os.path.
os.mkdir('./pkl/mydir')

# final df
df = pd.concat((df_gov, df_hlt))
df.to_csv("df_tweet2.csv", sep=';', index=False,
          encoding='utf-8')

user = "NewIndianXpress"
tweetCriteria = got.manager.TweetCriteria().setUsername(user)\
                                           .setSince("2020-02-01")\
                                           .setUntil("2020-04-30")\
                                           .setQuerySearch("CoronavirusOutbreakindia")
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
IN_tweets = pd.DataFrame()
IN_tweets['time'] = [t.date for t in tweets]
IN_tweets['text'] = [t.text for t in tweets]
IN_tweets['retweets'] = [t.retweets for t in tweets]
IN_tweets.to_csv('TOI_IN.csv', sep=';', index=False,
                 encoding='utf-8')