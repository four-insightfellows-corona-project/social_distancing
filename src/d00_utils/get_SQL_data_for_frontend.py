#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:04:51 2020

@author: eric

Obtains most recently updated weather & popular times data from Ed's 
SQL database, processes the data as we did before fitting model, 
and deposits in ../d01_data for fast access by front end.

COMMAND LINE USAGE: 
./get_sql_data_for_frontend.py

"""

## Import necessary modules & functions
import sys
import os
import numpy as np
import datetime as dt

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.binning import binMinute
from d00_utils.db_funcs import db_to_df

def main():
    
    ## Import our most recently updated raw data from SQL
    raw_weather = db_to_df(sql="SELECT * FROM weather",ini_section='non-social-parks-db')
    raw_poptimes = db_to_df(sql="SELECT * FROM popular_times",ini_section='non-social-parks-db')
    
    # To save raw data
    # raw_weather.to_pickle("../d01_data/raw_weather.pkl")
    # raw_poptimes.to_pickle("../d01_data/raw_poptimes.pkl")
    
    ## Process the data in the ways we did before fitting the model
    # Define a useful utility: 
    def convert_time_and_bin(dframe, time_col):
        # Convert time to datetime and bin the time into a time_bin 
        dframe['datetime'] = dframe[time_col].apply(lambda x: dt.datetime.fromtimestamp(x))
        dframe = dframe.set_index('datetime')
        dframe = dframe.tz_localize('US/Eastern')
        dframe = dframe.reset_index()
        
        # bin the time
        dframe['time_bin'] = dframe['datetime'].apply(lambda x: x.replace(minute = 0, second = 0) + dt.timedelta(minutes=binMinute(x.minute)))
        
        return dframe
    
    # Apply to raw_weather & raw_poptimes; convert time to datetime & create time_bin column
    raw_weather = convert_time_and_bin(raw_weather, 'reference_time')
    raw_poptimes = convert_time_and_bin(raw_poptimes, 'local_time')
    
    # Join our raw dataframes on time_bin
    df = raw_weather.join(raw_poptimes[['current_pop','time_bin']].set_index('time_bin'),on = 'time_bin')    
    
    # create good, maybe, bad weather columns
    good = ['clear sky','few clouds']
    maybe = ['scattered clouds','mist','light rain','broken clouds']
    bad = ['heavy intensity rain','moderate rain','overcast clouds','thunderstorm with rain','thunderstorm with light rain']
    df['status_good'] = np.zeros(len(df))
    df['status_maybe'] = np.zeros(len(df))
    df['status_bad'] = np.zeros(len(df))
    df.loc[df.detailed_status.isin(good),'status_good'] =1
    df.loc[df.detailed_status.isin(maybe),'status_maybe'] =1
    df.loc[df.detailed_status.isin(bad),'status_bad'] =1
    
    # add time features
    df['dayofweek'] = df.time_bin.dt.dayofweek
    df['hour'] = df.time_bin.dt.hour
        
    # select final features. Note: the order is important.
    df = df[['time_bin','current_pop', 'wind_speed', 'temp', 'status_good', 
             'status_maybe', 'status_bad', 'dayofweek', 'hour']]
    
    # Drop NAs so we can apply our classifier
    # Note: this is entirely ok to do because we are not training 
    # our model on this data. The model has been trained already.
    df = df.dropna(axis=0)
    
    # Aggregate within time bins, erring toward values that lead to a cautious recommendation ("unsafe")
    df = df.groupby('time_bin').agg({'current_pop':'mean', 'wind_speed':'mean', 'temp':'mean',
                                 'status_good':'max', 'status_maybe':'min', 'status_bad':'min',
                                 'dayofweek':'mean', 'hour':'mean'})
    # Reset index
    df = df.reset_index()
    
    # Save result 
    df.to_pickle("../d01_data/03_SQL_data_for_frontend_ee.pkl")

if __name__ == "__main__":
    main()