from datetime import date, timedelta, datetime, timezone
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
                                startDate_str, endDate_str)
gov_tweetsObjs = downloadTweets(gov_users, 'gov',
                                startDate_str, endDate_str)

# store raw tweets in db
storObj = TweetsStorage()
ltweetObj = hlt_tweetsObjs + gov_tweetsObjs
for tObjs in ltweetObj:
    storObj.saveRawTweetsToSql(tObjs)

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
df = pd.concat((df_hlt, df_gov), 0)

# output to csv to be checked manually 
# add column 'measures' for quarantine news etc
df['measures'] = ""
df = df[['time', 'text', "measures", 'tweet_source', 'country']]
if not path.isdir('./csv'):
    mkdir('./csv')
fname = path.join('csv', 'tweets_original.csv')
df.to_csv(fname, sep=';', index=False,
          encoding='utf-8')


# df_db = storObj.loadRawTweetsFromSql()

# c = ['AU']
# def slice_dict(d, l):
#     return dict([(k, d[k])  for k in l ])
# dusers = slice_dict(TwitterInfo.hlt_users, c)    
# dkey_any = slice_dict(TwitterInfo.hlt_keys_ANY, c)
# dkey_all = slice_dict( TwitterInfo.hlt_keys_ALL, c)
# dcovid = slice_dict(TwitterInfo.hlt_match_covid, c)
# CH_obj = downloadTweets(dusers,
#                         'health', "2020-03-18", "2020-03-21")
# df = filter2DataFrame(CH_obj, dkey_any,
#                       dkey_all, 
#                       dcovid)
# df.to_csv('AU.csv', sep=';', index=False, encoding='utf-8')

# re.search()
# # [t.text for t in CH_obj[0].tweets]

# u = "PIB_India"
# CH_obj = downloadTweets({"IN":u},
#                         'health', "2020-02-01", "2020-03-22")
# df = filter2DataFrame(CH_obj, {'IN':["cases", "number"]},
#                       {'IN':None}, 
#                       {'IN':True})
# df.to_csv('IN.csv', sep=';', index=False, encoding='utf-8')


# u = "CPHO_Canada"
# ["tested", "people", "canada"]
# covid : False