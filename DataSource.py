'''
Python script to make a request to the Twitter Sandbox API based on 
search terms that correlate well with atmospheric particulate matter 
(PM2.5). 

This script was created as part of THE PRACTICAL APPLICATION 
OF A CONCEPTUAL FRAMEWORK USING SOCIAL MEDIA TO UNDERSTAND 
COMMUNITY-LEVEL RESPONSE TO WILDFIRE SMOKE IN THE WESTERN US, M.S.
thesis by Marissa Grubbs, Washington State University, May 2019.

Author: Marissa Grubbs, Washington State University, May 2019.

Contact: Von P. Walden, Washington State University, v.walden@wsu.edu
'''

#%% Necessary Python imports

import requests
import json

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.rrule import rrule, DAILY

import xarray as xr
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords

from wordcloud import WordCloud, STOPWORDS

#%% Setup authentication for Twitter.
base_url = 'https://api.twitter.com/'
bearer_token="xxxx"
endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/sandboxdev.json"
headers = {"Authorization":"Bearer xxxx", "Content-Type": "application/json"}

#%%
# Contraints to request in sandbox:
#    ....query is limit to 128 characters
#    ....profile_locality:Spokane and -is:retweet are not allowable operators
# So print the length of queries to check this.
print(len("(smoke OR wildfire OR haze OR (acres burned)) point_radius:[-117.426 47.658 25mi])"))
print(len("(smoke OR smoky OR unhealthy OR AQI OR smokey OR air quality OR PM2.5 OR lungs) point_radius:[-117.426 47.658 25mi])"))


#%%
# Acquire tweets base on user locality
data = '{"query":"(smoke OR smoky OR unhealthy OR AQI OR smokey OR air quality OR PM2.5 OR lungs) point_radius:[-117.426 47.658 25mi]", "fromDate": "201806010000", "toDate": "201809302359","maxResults":100}'

# Make the request to Twitter
response = requests.post(endpoint,data=data,headers=headers).json()

print(response)
