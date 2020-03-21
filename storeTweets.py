
import sqlite3
import pandas as pd
from os import path, mkdir
from datetime import datetime, timezone, timedelta

class TweetsStorage:
    """ A class to store tweets in a sqlite3 db"""
    dbname = 'db_tweet.db'
    dbdir = 'db'
    table_raw = 'raw_tweets'
    table_clean = 'clean_tweets'
    def __init__(self):
        self.db = path.join(self.dbdir, self.dbname)
        if not path.isdir(self.dbdir):
            mkdir(self.dbdir)

    def __createRawTweetTable(self):
        """ Create sqlite3 table to store raw tweets
            
            TO BE EXECUTED ONLY ONCE!!
            Column names are EXACTLY the same as the relevant
            attributes from GetOldTweets3.Tweet + 
            'country', 'twtype' and 'created' (timestamp)
        """
        conn = sqlite3.connect(self.db)    
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE %s
                    (id text,
                    date text, 
                    username text, 
                    text text, 
                    retweets integer,
                    favorites integer,
                    mentions text,
                    hashtags text,
                    geo text,
                    country text,
                    twtype text,
                    created text)''' % self.table_raw)
        conn.commit()
        conn.close()

    def __createCleanTweetTable(self):
        """ Create sqlite3 table to store clean tweets
            
            TO BE EXECUTED ONLY ONCE!!
            Column names are EXACTLY the same as the relevant
            attributes from GetOldTweets3.Tweet + 
            'country', 'twtype' and 'created' (timestamp)
        """
        conn = sqlite3.connect(self.db)    
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE %s
                    (time text,
                    text text, 
                    measures text, 
                    tweet_source text, 
                    country text,
                    timestamp text)''' % self.table_clean)
        conn.commit()
        conn.close()


    def createRawTweetsDf2Sql(self, tweetOff):
        """ Create dataframe to store tweets in sqlite3 db 

            Parameters
            ----------
            tweetOff : a TweetOfficial obj
        """
        attribs = ['id',  # str
                   'date',  # utc datetime
                  # 'permalink',  # str
                   'username',   # str
                  # 'to',   # str
                   'text',  # str
                   'retweets',   # int  
                   'favorites',  # int
                   'mentions',  # str
                   'hashtags',  # str
                   'geo']  # str
        df = pd.DataFrame()
        for a in attribs:
            df[a] = [getattr(t, a) for t in tweetOff.tweets]
        df['country'] = tweetOff.country
        df['twtype']  = tweetOff.type
        df['created'] = datetime.now(tz=timezone(offset=timedelta(hours=1)))
        return df

    def saveRawTweetsToSql(self, tweetOff):
        """ Append raw tweets to database"""
        conn = sqlite3.connect(self.db) 
        df = self.createRawTweetsDf2Sql(tweetOff)
        df.to_sql(self.table_raw, conn, 
                  if_exists="append", index=False)
        conn.close()

    def loadRawTweetsFromSql(self):
        """ Query raw tweets from database """
        conn = sqlite3.connect(self.db) 
        sqlQuery = "SELECT * FROM %s" % self.table_raw
        df = pd.read_sql(sqlQuery, conn,
                         parse_dates = {'date':'%Y-%m-%d %H:%M:%S%z',
                                        'created':'%Y-%m-%d %H:%M:%S.%f%z'})
        conn.close()
        return df

    def saveCleanTweetsToSql(self, df):
        """ Append clean tweets to db 
        
            Parameters
            ----------
            df : pd.DataFrame with structure
                    time : datetime (no microseconds)
                    text : str  
                    measures : str, 
                    tweet_source : str 
                    country : str
                    timestamp : datetime (with microseconds)
        """
        conn = sqlite3.connect(self.db) 
        df.to_sql(self.table_clean, conn, 
                  if_exists="append", index=False)
        conn.close()

    def loadCleanTweetsFromSql(self):
        """ Query clean tweets from database """
        conn = sqlite3.connect(self.db) 
        sqlQuery = "SELECT * FROM %s" % self.table_clean
        df = pd.read_sql(sqlQuery, conn,
                         parse_dates = {'time':'%Y-%m-%d %H:%M:%S%z',
                                        'timestamp':'%Y-%m-%d %H:%M:%S.%f%z'})
        conn.close()
        return df
    

