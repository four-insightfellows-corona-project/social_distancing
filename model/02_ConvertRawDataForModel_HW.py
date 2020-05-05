#!/usr/bin/env python
# coding: utf-8

# **The features used for the model**:  current_popularity, wind_speed,temp, status_good, status_maybe, status_bad, dayofweek, hour. 
# 
# **steps**:
# 1. Load the latest populartimes data & weather data into a data frame.
# 2. Convert time from UTC to EST & bin the time into a time_bin (can't directly use the time information as this sometimes affect the 'hour' feature)
# 3. Create the "status_good, status_maybe, status_bad" features
# 4. Add the time features
# 5. Select the relevant features

# In[ ]:


## Step1: Load the latest data into a data frame. 
# Note that the code below works on populartimes data that Huayi has scrapped, 
# and need to be editted to reflect how Ed is scraping the weather & the populartimes data. 

import boto3
import pandas as pd
from datetime import datetime, timedelta
import json
from io import StringIO
import numpy as np

def binMinute(minute):
    '''
    Calculate which of the 15min bins the current minute falls in.
    The bins are 05, 20, 35, 50. 
    Current minutes less than 05 belongs to bin 50 of the hour before. 
    '''    
    m2q= (minute-5)/15
    if m2q < 0:
        newminute = -10 
    elif m2q < 1:
        newminute = 5
    elif m2q < 2:
        newminute = 20
    elif m2q < 3:
        newminute = 35
    elif m2q < 4:
        newminute = 50
    return(newminute)       


if __name__ == '__main__':  
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('XXXX') # the bucket containing the raw data. 
    idx = 0
    for item in bucket.objects.filter(Prefix = "Data/"): # Predix is the path to the file.
        content = item.get()['Body'].read().decode('utf-8')
        if len(content):
            json_content = json.loads(content)['current_popularity']
            ### + a line to load the weather data
            timestamp = datetime.strptime(item.key[5:-5], '%m%d%Y_%H%M')
            data = pd.DataFrame({'current_popularity': json_content, 'datetime': timestamp}, index = [idx])
            idx +=1


# In[ ]:


## Step2: Convert time from UTC to EST & bin the time into a time_bin 

# change time zone
data['datetime'] = data['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern').dt.tz_localize(None)
# bin the time
data['time_bin'] = data['datetime'].apply(lambda x: x.replace(minute = 0) + timedelta(minutes=binMinute(x.minute)))


# In[ ]:


## Step3: good, maybe, bad
good = ['clear sky','few clouds']
maybe = ['scattered clouds','mist','light rain','broken clouds']
bad = ['heavy intensity rain','moderate rain','overcast clouds','thunderstorm with rain','thunderstorm with light rain']
data['status_good'] = np.zeros(1)
data['status_maybe'] = np.zeros(1)
data['status_bad'] = np.zeros(1)
data.loc[data.detailed_status.isin(good),'status_good'] =1
data.loc[data.detailed_status.isin(maybe),'status_maybe'] =1
data.loc[data.detailed_status.isin(bad),'status_bad'] =1


# In[ ]:


# Step4: add time features
data['dayofweek'] = data.time_bin.dt.dayofweek
data['hour'] = data.time_bin.dt.hour


# In[ ]:


# Step5: select final features. Note: the order is important.
model_input = data[['current_popularity', 'wind_speed', 'temp', 'status_good', 
                    'status_maybe', 'status_bad', 'dayofweek', 'hour']].values

