#!/usr/bin/env python
# coding: utf-8

# **The features used for the model**:  current_popularity, wind_speed,temp, status_good, status_maybe, status_bad, dayofweek, hour. 
# 
# **steps**:
# 1. Load the latest populartimes data & weather data into a data frame.
# 2. Convert time from unix structure to datetime & bin the time into a time_bin (can't directly use the time information as this sometimes affect the 'hour' feature)
# 3. Create the "status_good, status_maybe, status_bad" features
# 4. Add the time features
# 5. Select the relevant features


import boto3
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
import numpy as np
 

bucket_name = "prospectparkmodel"




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



def load_newest_observation():

    ## Step1: Load the latest data into a data frame. 
    # Note that the code below works on populartimes data that Huayi has scrapped, 
    # and need to be editted to reflect how Ed is scraping the weather & the populartimes data. 

    client = boto3.client('s3') #low-level functional API

    resource = boto3.resource('s3') #high-level object-oriented API
    my_bucket = resource.Bucket(bucket_name) 

    # read in the weather data
    df = pd.DataFrame()
    weather_data = client.get_object(Bucket =bucket_name, Key='data/current_weather.csv')['Body']
    weather_string = weather_data.read().decode('utf-8')
    df = pd.read_csv(StringIO(weather_string))

    # add "current_popularity"
    popularity_data = client.get_object(Bucket =bucket_name, Key='data/current_weather.csv')['Body']
    popularity_string = popularity_data.read().decode('utf-8')
    df['current_popularity'] = pd.read_csv(StringIO(popularity_string))['current_pop']


    ## Step2: Convert time from UTC to EST & bin the time into a time_bin 

    ## convert unix time to datetime
    df['datetime'] = datetime.fromtimestamp(df.reception_time)
    # bin the time
    df['time_bin'] = df['datetime'].apply(lambda x: x.replace(minute = 0, second = 0) + timedelta(minutes=binMinute(x.minute)))


    # In[30]:


    ## Step3: good, maybe, bad
    good = ['clear sky','few clouds']
    maybe = ['scattered clouds','mist','light rain','broken clouds']
    bad = ['heavy intensity rain','moderate rain','overcast clouds','thunderstorm with rain','thunderstorm with light rain']
    df['status_good'] = np.zeros(1)
    df['status_maybe'] = np.zeros(1)
    df['status_bad'] = np.zeros(1)
    df.loc[df.detailed_status.isin(good),'status_good'] =1
    df.loc[df.detailed_status.isin(maybe),'status_maybe'] =1
    df.loc[df.detailed_status.isin(bad),'status_bad'] =1


    # In[31]:


    # Step4: add time features
    df['dayofweek'] = df.time_bin.dt.dayofweek
    df['hour'] = df.time_bin.dt.hour


    # In[32]:


    # Step5: select final features. Note: the order is important.
    model_input = df[['current_popularity', 'wind_speed', 'temp', 'status_good', 
                        'status_maybe', 'status_bad', 'dayofweek', 'hour']].values

    return model_input


if __name__ == '__main__':
    load_newest_observation()

