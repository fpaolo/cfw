from datetime import date, timedelta, datetime, timezone
from TweetsOfficial import downloadTweets, filter2DataFrame
from storeTweets import TweetsStorage
from twitterUsers import TwitterInfo
from functions import seqDates, format_dates_HHMM, makeDFfromDates
import pandas as pd 
from os import path, mkdir 

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

# cat in a unique df with right structure
df = pd.concat((df_hlt, df_gov), 0)
df['measures'] = ""
df = df[['time', 'text', "measures", 'tweet_source', 'country']]

# manually add US and CN-HK data
# ========== US CDC =========
#  dates from https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fcases-in-us.html
#This page will be updated regularly at noon Mondays 
# through Fridays. Numbers close out at 4 p.m. 
# the day before reporting.
dates = seqDates(startDate, endDate)
dates_us = format_dates_HHMM(dates, 12, 0, -4)
dates_us = [d for d in dates_us if d.isoweekday() not in [6, 7]]
df_us = makeDFfromDates(dates_us, 'US', 'cdc website')


# ====== CN-HK =========
# '''I checked Hong Kong CHP's website, and the dashboard 
#    and the pdf version (https://www.chp.gov.hk/files/pdf/local_situation_covid19_en.pdf) 
#    is updated at 4pm (HK time) every day. 
#    At 4:30pm of each day, CHP holds a press briefing 
#    session to explain the latest situation to the public
#    and media. '''
# dashboard update
dates_cnhk_du = format_dates_HHMM(dates, 16, 0, 8)
df_cnhk_du = makeDFfromDates(dates_cnhk_du, 'CN-HK', 'dashboard update')
# press release
dates_cnhk_pr = format_dates_HHMM(dates, 16, 30, 8)
df_cnhk_pr = makeDFfromDates(dates_cnhk_pr, 'CN-HK', 'press release')
df_cnhk = pd.concat((df_cnhk_du, df_cnhk_pr))

# final dataset
df = pd.concat((df, df_us, df_cnhk), 0)


# output to csv to be checked manually 
# add column 'measures' for quarantine news etc
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