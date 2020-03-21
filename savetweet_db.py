from datetime import date, timedelta, datetime
from functions import downloadTweets, filter2DataFrame
from storeTweets import TweetsStorage
import pandas as pd 
from os import path, mkdir 
from twitterUsers import TwitterInfo


# all dates are in UTC
# 'endDate' not included
endDate = datetime.today()
startDate = endDate - timedelta(days=1)
endDate_str = endDate.strftime("%Y-%m-%d")
startDate_str = startDate.strftime("%Y-%m-%d")

# dictionaries with hlt agencies and gov twitter accounts
hlt_users = TwitterInfo.hlt_users
gov_users = TwitterInfo.gov_users

# download tweets
hlt_tweetsObjs = downloadTweets(hlt_users, 'health', 
                                startDate, endDate)
gov_tweetsObjs = downloadTweets(gov_users, 'gov',
                                startDate, endDate)

# store raw tweets in db
storObj = TweetsStorage()
ltweetObj = []
ltweetObj.append(hlt_tweetsObjs)
ltweetObj.append(gov_tweetsObjs)
for tObjs in ltweetObj:
    for tObj in tObjs: 
        storObj.saveRawTweetsToSql(tObj)

# filter tweets health
hlt_keys_ANY = TwitterInfo.hlt_keys_ANY
hlt_keys_ALL = TwitterInfo.hlt_keys_ALL
hlt_match_covid = TwitterInfo.hlt_match_covid
df_hlt = filter2DataFrame(hlt_tweetsObjs, hlt_keys_ANY,
                          hlt_keys_ALL, hlt_match_covid)

# filter tweets gov
gov_keys_ANY = TwitterInfo.gov_keys_ANY
gov_keys_ALL = TwitterInfo.gov_keys_ALL
gov_match_covid = TwitterInfo.gov_match_covid
df_gov = filter2DataFrame(gov_tweetsObjs, gov_keys_ANY,
                          gov_keys_ALL, gov_match_covid)

# output to csv to be checked manually 
# add column 'measures' for quarantine news etc
df = pd.concat((df_hlt, df_gov), 0)
df['measures'] = ""
df = df[['time', 'text', "measures", 'tweet_source', 'country']]
df.head()
if not path.isdir('./csv'):
    mkdir('./csv')
fname = path.join('csv', 'tweets_original.csv')
df.to_csv(fname, sep=';', index=False,
          encoding='utf-8')