import pandas as pd
from datetime import timedelta, datetime, timezone
from storeTweets import TweetsStorage
from os import path, mkdir

df_csv = pd.read_csv('./csv/tweets_checked.csv', sep=';')

# convert all dates to UTC
# WARNING!!! excel dates are from my locale which is utc+1
df_csv['time'] = df_csv['time'] + '+0100'
times = df_csv['time'].to_list()
times = [datetime.strptime(t, "%d/%m/%Y %H:%M%z") for t in times]
times = [t.astimezone(timezone.utc) for t in times]
df_csv['time'] = times

# sort and create timestamp
df_csv.sort_values(['country', 'time'], ascending=False,
                    inplace=True)
tstamp = datetime.now(tz=timezone(offset=timedelta(hours=1)))
df_csv['timestamp'] = tstamp

# upload to db
stObj = TweetsStorage()
stObj.saveCleanTweetsToSql(df_csv)

# downloads the full dataset and outputs a csv
df_all = stObj.loadCleanTweetsFromSql()
if not path.isdir('./csv_out'):
    mkdir('csv_out')
df_all.sort_values(['country', 'time'], ascending=False,
                    inplace=True)
df_all.to_csv(path.join('csv_out', 'covid19_allnews.csv'), 
              sep=';', index=False,
              encoding='utf-8')


# # add CN-HK covid19 status reports according to info
# # '''I checked Hong Kong CHP's website, and the dashboard 
# #    and the pdf version (https://www.chp.gov.hk/files/pdf/local_situation_covid19_en.pdf) 
# #    is updated at 4pm (HK time) every day. 
# #    At 4:30pm of each day, CHP holds a press briefing 
# #    session to explain the latest situation to the public
# #    and media. '''
# df_csv['monthday'] = df_csv['time'].map(lambda x: f"{x.month:02}{x.day:02}")
# cn_mdays = pd.unique(df_csv[df_csv['country'] == 'CN']['monthday'])
# df_csv.drop(columns='monthday', inplace=True)
# def format_dates(dates_MMDD, HH, MM):
#     """ Add HK dates and format tz to UTC """
#     dates = [f"2020{c} {HH}:{MM}+0800" for c in dates_MMDD]
#     dates = [datetime.strptime(t, "%Y%m%d %H:%M%z") for t in dates]
#     dates = [t.astimezone(timezone.utc) for t in dates]
#     return dates
# df_cnhk_hlt = pd.DataFrame({'time' : format_dates(cn_mdays, 16, 00),
#                             'text' : 'dashboard update',
#                             'measures' : None,
#                             'tweet_source' : 'health',
#                             'country' : 'CN-HK'})
# df_cnhk_gov = pd.DataFrame({'time' : format_dates(cn_mdays, 16, 30),
#                             'text' : 'press release',
#                             'measures' : None,
#                             'tweet_source' : 'health',
#                             'country' : 'CN-HK'})
# df_cnhk = pd.concat((df_cnhk_hlt, df_cnhk_gov))                            

# # add cn-hk and sort 
# df_csv = pd.concat((df_csv, df_cnhk))  
# df_csv.sort_values(['country', 'time'], ascending=False,
#                     inplace=True)

# # create timestamp
# tstamp = datetime.now(tz=timezone(offset=timedelta(hours=1)))
# df_csv['timestamp'] = tstamp

# # upload to db
# stObj = TweetsStorage()
# stObj.saveCleanTweetsToSql(df_csv)


# df = stObj.loadCleanTweetsFromSql()
# def extract_country_dates(df, country):
#     """ Extract unique YYYYMMDD dates for country """
#     df_cntr = df[df['country'] == country]
#     fdate = lambda x: f"{x.year:04}{x.month:02}{x.day:02}"
#     df_cntr['monthday'] = df_cntr['time'].map(fdate)
#     mdays = pd.unique(df_cntr['monthday'])
#     return mdays

# def format_date2s(dates_MMDD, HH, MM, utc_offset):
#     """ Add dates and format tz to UTC """
#     dates = [f"{c} {HH}:{MM}+{utc_offset:.02}00" for c in dates_MMDD]
#     dates = [datetime.strptime(t, "%Y%m%d %H:%M%z") for t in dates]
#     dates = [t.astimezone(timezone.utc) for t in dates]
#     return dates


# endDate = datetime.today()
# startDate = endDate - timedelta(days=21)


# # create timestamp
# tstamp = datetime.now(tz=timezone(offset=timedelta(hours=1)))
# df_us['timestamp'] = tstamp


# stObj = TweetsStorage()
# stObj.saveCleanTweetsToSql(df_us)