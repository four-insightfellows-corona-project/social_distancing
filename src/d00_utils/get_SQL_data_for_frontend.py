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
    df = db_to_df(sql="SELECT * FROM weather",ini_section='non-social-parks-db')
    poptimes = db_to_df(sql="SELECT * FROM popular_times",ini_section='non-social-parks-db')
    
    
    ## Process the data in the ways we did before fitting the model
    df['current_popularity'] = poptimes['current_pop']
    
    # Convert time to datetime and bin the time into a time_bin 
    df['datetime'] = df.reference_time.apply(lambda x: dt.datetime.fromtimestamp(x))
    df = df.set_index('datetime',drop=False)
    df = df.tz_localize('US/Eastern')
    
    # bin the time
    df['time_bin'] = df['datetime'].apply(lambda x: x.replace(minute = 0, second = 0) + dt.timedelta(minutes=binMinute(x.minute)))
    
    # create good, maybe, bad
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
    df = df[['datetime','time_bin','current_popularity', 'wind_speed', 'temp', 'status_good', 
                            'status_maybe', 'status_bad', 'dayofweek', 'hour']]
    
    df.to_pickle("../d01_data/03_from_SQL_for_frontend_ee.pkl")

if __name__ == "__main__":
    main()