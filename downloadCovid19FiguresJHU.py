import pandas as pd
from twitterUsers import TwitterInfo
from os import path, mkdir

# import datasets from url
# source: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
url_confi = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_death = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
df_confi = pd.read_csv(url_confi, header=0, sep=',')
df_death = pd.read_csv(url_death, header=0, sep=',')
df_confi['type'] = "confirmed"
df_death['type'] = "death"
df = pd.concat((df_confi, df_death),0)

# clean up columns
# drop lat/longi
# reshape wide -> long
df.drop(columns = ['Lat', 'Long'], inplace=True)
idx_cols = ['Province/State', 'Country/Region', 
            'type']            
df = df.melt(id_vars = idx_cols, value_name = 'cases', 
             var_name = 'date')
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')       
df.columns = ['state', 'country', 'type', 'date', 'cases']

# extract hong-kong to compute only mainland china
idx_cnhk = df['state'] == 'Hong Kong'
df_cnhk = df[idx_cnhk]
df_cnhk['country'] = 'Hong Kong'
df_cnhk.drop(columns='state', inplace=True)
df = df[~idx_cnhk]

# aggregate cases by country 
# and add back hong kong
df_agg = df.groupby(['country', 'type', 'date']).sum()
df_agg.reset_index(level=['country', 'type', 'date'], 
                  inplace=True)
df_agg = pd.concat((df_agg, df_cnhk))                  

# create world count
df_cases_world = df_agg.groupby(['type', 'date']).sum()
df_cases_world.reset_index(level=['type', 'date'], 
                           inplace=True)
df_cases_world['country'] = 'world'
df_agg = pd.concat((df_agg, df_cases_world))  

# codify countries with 2d iso alpha code  
countries = TwitterInfo.country_list                  
countries_ext = ['Australia', 'Canada', 'Switzerland',
                 'China', 'Hong Kong', 'Germany',
                 'Spain', 'France', 'India', 'Italy',
                 'Japan', 'Korea, South', 'New Zealand',
                 'Sweden', 'United Kingdom', 'US']
dict_countries = dict(zip(countries, countries_ext))    
df_agg['country_code'] = None
for k, v in dict_countries.items():
    df_agg.loc[df_agg['country'] == v, 'country_code'] = k

# add 'world' 2 digit code
countries += ['WW']
df_agg.loc[df_agg['country'] == 'world', 'country_code'] = 'WW'

# check match successful
cc_matched = [c for c in pd.unique(df_agg['country_code']) if c is not None]
no_match = set(countries).difference(cc_matched)
if len(no_match) > 0:
    raise KeyError(f"Could not find country: {no_match}")

# retain only relevant countries
df_out = df_agg[df_agg['country_code'].isin(countries)]
df_out.drop(columns='country', inplace=True)
df_out.columns = ['type', 'date', 'cases_cum', 'country']

# output csv
if not path.isdir('./csv_out'):
    mkdir('csv_out')
df_out.to_csv('./csv_out/covid19_allcases.csv',sep=";",
              index=None)