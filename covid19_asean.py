# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:53:27 2020

@author: prisc
"""
import json
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import datetime

def get_json(api_url):
	response = requests.get(api_url)
	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return none
    
record_date = '2020-08-17'
covid_url = 'https://covid19-api.org/api/status?date='+record_date
df_covid_worldwide = pd.io.json.json_normalize(get_json(covid_url))

#print(df_covid_worldwide.head())

df_covid_worldwide['last_update'] = pd.to_datetime(df_covid_worldwide['last_update'], format='%Y-%m-%d %H:%M:%S')
df_covid_worldwide['last_update'] = df_covid_worldwide['last_update'].apply(lambda x: x.date())

countries_url = 'https://covid19-api.org/api/countries'
df_countries = pd.io.json.json_normalize(get_json(countries_url))
df_countries = df_countries.rename(columns={'alpha2': 'country'})[['name','country']]

#print(df_countries.head())

df_covid_denormalized = pd.merge(df_covid_worldwide, df_countries, on='country')

#print(df_covid_denormalized.head())

df_covid_denormalized['fatality_ratio'] = df_covid_denormalized['deaths']/df_covid_denormalized['cases']





df_top_20_fatality_rate = df_covid_denormalized.sort_values(by='fatality_ratio', ascending=False).head(20)

plt.figure(figsize=(20, 8))
x = df_top_20_fatality_rate['name']
y = df_top_20_fatality_rate['fatality_ratio']
plt.barh(x,y)
plt.gca().invert_yaxis()
plt.xlabel('Fatality Rate')
plt.ylabel('Country Name')
plt.title('Top 20 Highest Fatality Rate Countries')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

    
    

    
    
    
    
    
    

countries = ['ID','MY','SG','TH','VN', 'PH', 'MM', 'BN', 'LA', 'KH']
i = 0
for country in countries:
	covid_timeline_url = 'https://covid19-api.org/api/timeline/'+country
	df_covid_timeline = pd.io.json.json_normalize(get_json(covid_timeline_url))
	df_covid_timeline['last_update'] = pd.to_datetime(df_covid_timeline['last_update'], format='%Y-%m-%d %H:%M:%S')
	df_covid_timeline['last_update'] = df_covid_timeline['last_update'].apply(lambda x: x.date())
	if i==0:
		df_covid_timeline_merged = df_covid_timeline
	else:
		df_covid_timeline_merged = df_covid_timeline.append(df_covid_timeline_merged, ignore_index=True)
	i=i+1
    
print(df_covid_timeline_merged.head())
print('')

df_covid_timeline_denormalized = pd.merge(df_covid_timeline_merged, df_countries, on='country')

df_covid_timeline_denormalized = df_covid_timeline_denormalized[(df_covid_timeline_denormalized['last_update'] >= datetime.date(2020, 3, 1))]
df_covid_timeline_denormalized = df_covid_timeline_denormalized.append(df_covid_denormalized['fatality_ratio'])


#else:
#        asean_cases = asean_last_update.append(asean_cases)

countries = ['ID','MY','SG','TH','VN', 'PH', 'MM', 'BN', 'LA', 'KH']
i = 0
for country in countries:
    asean_last_update = df_covid_timeline_merged[(df_covid_timeline_merged['last_update']==datetime.date(2020,9,13))]
    asean_cases = pd.DataFrame(asean_last_update).reset_index().drop('index', axis=1)
    
    if i==0:
        asean_cases = asean_last_update
    i=i+1
print(asean_cases)
print('')

asean_total_case = asean_cases['cases'].sum()
asean_total_deaths = asean_cases['deaths'].sum()
asean_total_recovered = asean_cases['recovered'].sum()
print ("ASEAN total cases: ", asean_total_case)
print ("ASEAN total deaths: ", asean_total_deaths)
print ("ASEAN total recovered: ", asean_total_recovered)


plt.clf()
countries = ['ID','MY','SG','TH','VN', 'PH', 'MM', 'BN', 'LA', 'KH']
plt.figure(figsize=(8, 5))
for country in countries:
	country_data = df_covid_timeline_denormalized['country']==country
	x = df_covid_timeline_denormalized[country_data]['last_update']
	y = df_covid_timeline_denormalized[country_data]['cases']
	plt.plot(x, y, label = country, linewidth = 2)
    
plt.style.use('dark_background')
plt.legend()
plt.xlabel('Record Date')
plt.xticks(rotation=45)
plt.ylabel('Total Cases')
#plt.title('COVID-19 ASEAN')
plt.show()


plt.clf()
countries = ['ID','MY','SG','TH','VN', 'PH', 'MM', 'BN', 'LA', 'KH']
plt.figure(figsize=(8, 5))
for country in countries:
	country_data = df_covid_denormalized['country']==country
	x = df_covid_denormalized[country_data]['country']
	y = df_covid_denormalized[country_data]['fatality_ratio']
	plt.bar(x, y)
    
plt.style.use('dark_background')
plt.xlabel('Country')
plt.ylabel('Fatality Ratio')
#plt.title('Fatality Rate')
plt.show()