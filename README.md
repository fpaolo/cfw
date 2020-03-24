# Workflow
Since some manual intervention/checking is necessary the workflow is for *each day* to run the following steps

1. run `downloadTweets.py` 
2. go to `./csv` folder and open the excel `tweets_checked.xlsx`
3. update the excel file and manually add/delete rows with relevant covid-19 news information 
4. export the cleaned tweets to the file `./csv/tweets_checked.csv` 
5. run python code `backupCleanedTweets.py`


## downloadTweets.py
The code automatically 

+ downloads all tweets from *yesterday* (utc or utc+1 time)
+ stores the downloaded, raw tweets in the database of raw tweets
+ does a first filtering of tweets based on pre-specified keywords
+ for US and CN-HK adds covid-19 status report publication times based on website information
+ outputs a `tweets_original.csv` (all dates are in utc)


## cleaning tweets 
Steps 2-3 are done in excel.

+ in the `tweets_checked.xlsx` go to tab `Data > Refresh` to update the tab `tweets_original`
+ copy the tab with formatting to the tab `tweets_checked`
+ edit the tab `tweets_checked` with missing covid-19 info
+ check https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/newpage_00032.html for JA health press releases
+ export the tab `tweets_checked` to csv

**Warning** My excel version translates utc-dates to dates in my locale (utc+1). All rows that you add to csv must therefore have a time in your local tz


## backupCleanedTweets
The code

+ imports the cleaned csv *reading all dates as utc+1* (my locale). Dates are then converted to utc
+ updates the database and exports a csv