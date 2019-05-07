'''
Python script to process JSON object returned after request to the 
Twitter Sandbox API based on search terms that correlate well with 
atmospheric particulate matter (PM2.5). 

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

#%%
#parsing through returned json to make an organized dataframe with the relevant information
created_at = []  
id_str=[]
text=[]
source=[]
truncated=[]
in_reply_to_status_id_str=[]
in_reply_to_user_id_str=[]
in_reply_to_screen_name=[]
user=[]
username=[]
coordinates=[]
place=[]
extended_tweet=[]           #may be nonexistant before November 2017
full_text=[]                #may be nonexistant before November 2017
quoted_status_id_str=[]
is_quote_status=[]
quoted_original_status=[]
quoted_original_text=[]
quoted_original_truncated=[]
quoted_original_full_text=[]
retweeted_original_status=[]
retweeted_original_text=[]
retweeted_original_full_text=[]
quote_count=[]
reply_count=[]
retweet_count=[]
favorite_count=[]
entities=[]
extended_entities=[]
lang=[]
matching_rules=[]
retweet=[]

count=0
for x in response.get('results'):
    created_at.append((x['created_at']))
    id_str.append((x['id_str']))
    text.append((x['text']))
    source.append((x['source']))
    truncated.append((x['truncated']))
    in_reply_to_status_id_str.append((x['in_reply_to_status_id_str']))
    in_reply_to_user_id_str.append((x['in_reply_to_user_id_str']))
    in_reply_to_screen_name.append((x['in_reply_to_screen_name']))
    user.append((x['user']))
    username.append((x['user']['name']))
    coordinates.append((x['coordinates']))
    place.append((x['place']))
    try:
        extended_tweet.append((x['extended_tweet']))
    except:
        extended_tweet.append("")
    try:
        full_text.append((x['extended_tweet']['full_text']))
    except:
        full_text.append("")
    try:
        quoted_status_id_str.append((x['quoted_status_id_str']))
    except:
        quoted_status_id_str.append("")
    is_quote_status.append((x['is_quote_status']))
    try:
        quoted_original_status.append((x['quoted_status']))
        quoted_original_text.append((x['quoted_status']['text']))
        quoted_original_truncated.append((x['quoted_status']['truncated']))
        try:
            quoted_original_full_text.append((x['quoted_status']['extended_tweet']['full_text']))
        except:
            quoted_original_full_text.append("")
    except:
        quoted_original_status.append("")
        quoted_original_text.append("")
        quoted_original_truncated.append("")
        quoted_original_full_text.append("")
    try:
        retweeted_original_status.append((x['retweeted_status']))
        retweet.append(True)
        retweeted_original_text.append((x['retweeted_status']['text']))
        try:
            retweeted_original_full_text.append((x['retweeted_status']['extended_tweet']['full_text']))
        except:
            retweeted_original_full_text.append("")
    except:
        retweeted_original_status.append("")
        retweeted_original_text.append("")
        retweeted_original_full_text.append("")
        retweet.append(False)
    quote_count.append((x['quote_count']))
    reply_count.append((x['reply_count']))
    retweet_count.append((x['retweet_count']))
    favorite_count.append((x['favorite_count']))
    entities.append((x['entities']))
    try:
        extended_entities.append((x['extended_entities']))
    except:
        extended_entities.append("")
    lang.append((x['lang']))
    matching_rules.append((x['matching_rules']))
    count=count+1
print(count)
    
d = {'created_at': created_at, 'id_str': id_str, 'text':text, 'source':source, 'retweet':retweet, 'truncated':truncated, 'in_reply_to_status_id_str':in_reply_to_status_id_str, 'in_reply_to_user_id_str':in_reply_to_user_id_str,'in_reply_to_screen_name':in_reply_to_screen_name, 'user':user, 'username':username, 'coordinates':coordinates, 'place':place, 'extended_tweet':extended_tweet, 'full_text':full_text, 'quoted_status_id_str':quoted_status_id_str, 'is_quote_status':is_quote_status, 'quoted_original_status':quoted_original_status, 'quoted_original_text':quoted_original_text, 'quoted_original_truncated':quoted_original_truncated,'quoted_original_full_text':quoted_original_full_text, 'retweeted_original_status':retweeted_original_status, 'retweeted_original_text':retweeted_original_text, 'retweeted_original_full_text':retweeted_original_full_text,'quote_count':quote_count, 'reply_count':reply_count, 'retweet_count':retweet_count, 'favorite_count':favorite_count, 'entities':entities, 'extended_entities':extended_entities, 'lang':lang, 'matching_rules':matching_rules}
dsimple = {'created_at': created_at, 'text':text,'truncated':truncated,'full_text':full_text, 'is_quote_status':is_quote_status,'quoted_original_text':quoted_original_text,'quoted_original_truncated':quoted_original_truncated,'quoted_original_full_text':quoted_original_full_text,'quote_count':quote_count,'reply_count':reply_count,'retweet_count':retweet_count,'favorite_count':favorite_count,'username':username}
df=pd.DataFrame(data=d)
dfsimple=pd.DataFrame(data=dsimple)
df=df.set_index('created_at')
dfsimple=dfsimple.set_index('created_at')

#save dataframe to csv
#df.to_csv(filename)
#dfsimple.to_csv(simplefilename)


#%%
print(count)


#%%



#%%
dfsimple


#%%
print(dfsimple['text'])

#%% [markdown]
# # NLTK

#%%
#Take the category of interest and turn the column with the full tweets into a single string of everything. Then use NLTK to process
tweets=[]

for row in dfsimple['text']:
    tweets.append(row)
    
tweetstring=""
for tweet in tweets:
    tweetstring=tweetstring+str(tweet)

#Divide the string into tokens (word, punctuation, emoji etc)
tweetwords=nltk.word_tokenize(tweetstring)

#sets Stopwords, tokens from NLTK and ones I added which don't contribute to the meaning
stop_list=stopwords.words('english')
cap_stop_list=['I', 'Me', 'My', 'Myself', 'We', 'Our', 'Ours', 'Ourselves', 'You', "You're", "You've", "You'll", "You'd", 'Your', 'Yours', 'Yourself', 'Yourselves', 'He', 'Him', 'His', 'Himself', 'She', "She's", 'Her', 'Hers', 'Herself', 'It', "It's", 'Its', 'Itself', 'They', 'Them', 'Their', 'Theirs', 'Themselves', 'What', 'Which', 'Who', 'Whom', 'This', 'That', "That'll", 'These', 'Those', 'Am', 'Is', 'Are', 'Was', 'Were', 'Be', 'Been', 'Being', 'Have', 'Has', 'Had', 'Having', 'Do', 'Does', 'Did', 'Doing', 'A', 'An', 'The', 'And', 'But', 'If', 'Or', 'Because', 'As', 'Until', 'While', 'Of', 'At', 'By', 'For', 'With', 'About', 'Against', 'Between', 'Into', 'Through', 'During', 'Before', 'After', 'Above', 'Below', 'To', 'From', 'Up', 'Down', 'In', 'Out', 'On', 'Off', 'Over', 'Under', 'Again', 'Further', 'Then', 'Once', 'Here', 'There', 'When', 'Where', 'Why', 'How', 'All', 'Any', 'Both', 'Each', 'Few', 'More', 'Most', 'Other', 'Some', 'Such', 'No', 'Nor', 'Not', 'Only', 'Own', 'Same', 'So', 'Than', 'Too', 'Very', 'S', 'T', 'Can', 'Will', 'Just', 'Don', "Don't", 'Should', "Should've", 'Now', 'D', 'L', 'M', 'O', 'Re', 'Ve', 'Y', 'Ain', 'Aren', "Aren't", 'Couldn', "Couldn't", 'Didn', "Didn't", 'Doesn', "Doesn't", 'Hadn', "Hadn't", 'Hasn', "Hasn't", 'Haven', "Haven't", 'Isn', "Isn't", 'Ma', 'Mightn', "Mightn't", 'Mustn', "Mustn't", 'Needn', "Needn't", 'Shan', "Shan't", 'Shouldn', "Shouldn't", 'Wasn', "Wasn't", 'Weren', "Weren't", 'Won', "Won't", 'Wouldn', "Wouldn't","'s","n't","'m","'re","'ve","'ll",'na','u','THE','gon','AND','im','IN','OF',"'d",'YOU','wo','wan','IS','TO','SO','ta','NOT','ur','U','MY','ya','Im','NO','ALL',"'S",'IT','DO','ON']
punctuation_list=['@','.','#','?',',','?','!',':','...','…',"'",'-',';','%',"''",")","(",'’','’’','$','``','“','”','‘','--','|','+','—','..','[',']','amp','1','2','3','4','5','6','7','8','9','0','&','https']

full_stop_list=stop_list+cap_stop_list+punctuation_list
for element in full_stop_list:
    for word in tweetwords:
        if element==word:
            #print(element)
            tweetwords.remove(element)

fdist=nltk.FreqDist(tweetwords)
print(fdist)


#%%
#makes a frequency distribution plot of most used tokens
fdist=nltk.FreqDist(tweetwords)
fdist.plot(30, cumulative=True)

