import pandas as pd
from datetime import timedelta, datetime, timezone
from storeTweets import TweetsStorage


df_csv = pd.read_csv('tweets_clean.csv', sep=';')

# convert all dates to UTC
# WARNING!!! excel dates are from my local which is utc+1
df_csv['time'] = df_csv['time'] + '+0100'
times = df_csv['time'].to_list()
times = [datetime.strptime(t, "%d/%m/%Y %H:%M%z") for t in times]
times = [t.astimezone(timezone.utc) for t in times]
df_csv['time'] = times

# add CN-HK covid19 status reports according to info
# '''I checked Hong Kong CHP's website, and the dashboard 
#    and the pdf version (https://www.chp.gov.hk/files/pdf/local_situation_covid19_en.pdf) 
#    is updated at 4pm (HK time) every day. 
#    At 4:30pm of each day, CHP holds a press briefing 
#    session to explain the latest situation to the public
#    and media. '''
df_csv['monthday'] = df_csv['time'].map(lambda x: f"{x.month:02}{x.day:02}")
cn_mdays = pd.unique(df_csv[df_csv['country'] == 'CN']['monthday'])
df_csv.drop(columns='monthday', inplace=True)
def format_dates(dates_MMDD, HH, MM):
    """ Add HK dates and format tz to UTC """
    dates = [f"2020{c} {HH}:{MM}+0800" for c in dates_MMDD]
    dates = [datetime.strptime(t, "%Y%m%d %H:%M%z") for t in dates]
    dates = [t.astimezone(timezone.utc) for t in dates]
    return dates
df_cnhk_hlt = pd.DataFrame({'time' : format_dates(cn_mdays, 16, 00),
                            'text' : 'dashboard update',
                            'measures' : None,
                            'tweet_source' : 'health',
                            'country' : 'CN-HK'})
df_cnhk_gov = pd.DataFrame({'time' : format_dates(cn_mdays, 16, 30),
                            'text' : 'press release',
                            'measures' : None,
                            'tweet_source' : 'health',
                            'country' : 'CN-HK'})
df_cnhk = pd.concat((df_cnhk_hlt, df_cnhk_gov))                            

# add cn-hk and sort 
df_csv = pd.concat((df_csv, df_cnhk))  
df_csv.sort_values(['country', 'time'], ascending=False,
                    inplace=True)

# create timestamp
tstamp = datetime.now(tz=timezone(offset=timedelta(hours=1)))
df_csv['timestamp'] = tstamp

# upload to db
stObj = TweetsStorage()
stObj.saveCleanTweetsToSql(df_csv)


df = stObj.loadCleanTweetsFromSql()
def extract_country_dates(df, country):
    """ Extract unique YYYYMMDD dates for country """
    df_cntr = df[df['country'] == country]
    fdate = lambda x: f"{x.year:04}{x.month:02}{x.day:02}"
    df_cntr['monthday'] = df_cntr['time'].map(fdate)
    mdays = pd.unique(df_cntr['monthday'])
    return mdays

def format_date2s(dates_MMDD, HH, MM, utc_offset):
    """ Add dates and format tz to UTC """
    dates = [f"{c} {HH}:{MM}+{utc_offset:.02}00" for c in dates_MMDD]
    dates = [datetime.strptime(t, "%Y%m%d %H:%M%z") for t in dates]
    dates = [t.astimezone(timezone.utc) for t in dates]
    return dates


endDate = datetime.today()
startDate = endDate - timedelta(days=21)
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
dates = seqDates(startDate, endDate)
# dashboard update
dates_cnhk_du = format_dates_HHMM(dates, 16, 0, 8)
df_cnhk_du = makeDFfromDates(dates_cnhk_du, 'CN-HK', 'dashboard update')
# press release
dates_cnhk_pr = format_dates_HHMM(dates, 16, 30, 8)
df_cnhk_pr = makeDFfromDates(dates_cnhk_pr, 'CN-HK', 'press release')
df_cnhk = pd.concat((df_cnhk_du, df_cnhk_pr))


# create timestamp
tstamp = datetime.now(tz=timezone(offset=timedelta(hours=1)))
df_us['timestamp'] = tstamp


stObj = TweetsStorage()
stObj.saveCleanTweetsToSql(df_us)