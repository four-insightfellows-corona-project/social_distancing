#!/usr/bin/env python3

'''


'''

import os
import sys
import json
import pyowm
import requests
import numpy as np
import pandas as pd
# from pyowm.weatherapi25.parsers import forecastparser
from pyowm.weatherapi25.forecast import Forecast

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.db_funcs import insert_user_feedback, db_to_df
from conf.auth import OWM_api_key


def weather_current():
    ''' Gets current weather data and commits to postgres db
    '''

    weather_columns = [
        'park_name', 'reception_time', 'reference_time', 'sunrise_time', 'sunset_time',
        'clouds', 'rain_1h', 'snow_1h', 'wind_speed', 'humidity',
        'press', 'temp', 'temp_feels', 'temp_max', 'temp_min', 'status', 'detailed_status',
        'wind_deg']

    owm = pyowm.OWM(OWM_api_key)

    park_name = 'Prospect Park'
    park_lat = 40.662551
    park_long = -73.969256
    tz_offset = -14400

    w_m = owm.weather_manager()
    # obs = w_m.weather_at_place('London,GB')
    obs = w_m.weather_at_coords(lat=park_lat, lon=park_long)
    # owm.weather_around_coords(,)

    w = obs.weather

    w_rain = 0
    if w.rain:
        w_rain = w.rain['1h']

    w_snow = 0
    if w.snow:
        w_snow = w.snow['1h']

    wind_deg = 0
    null_wind_deg = True
    if 'deg' in w.wind():
        null_wind_deg = False
        w.wind()['deg']

    weather_values = [
        park_name,
        obs.reception_time() + tz_offset,
        w.reference_time() + tz_offset,
        w.sunrise_time() + tz_offset,
        w.sunset_time() + tz_offset,
        w.clouds,
        w_rain,
        w_snow,
        w.wind()['speed'],
        w.humidity,
        w.pressure['press'],
        w.temperature(unit='fahrenheit')['temp'],
        w.temperature(unit='fahrenheit')['feels_like'],
        w.temperature(unit='fahrenheit')['temp_max'],
        w.temperature(unit='fahrenheit')['temp_min'],
        w.status,
        w.detailed_status,
        wind_deg
    ]

    if null_wind_deg:
        commit_cols = weather_columns[:-1]
        commit_vals = weather_values[:-1]
    else:
        commit_cols = weather_columns
        commit_vals = weather_values

    insert_user_feedback(
        table='weather_test',
        columns=commit_cols,
        values=commit_vals,
        ini_section='non-social-parks-db'
    )

def forcast():
    ''' Get prospect park forcast and
    '''
    owm = pyowm.OWM(OWM_api_key)

    park_name = 'Prospect Park'
    park_lat = 40.662551
    park_long = -73.969256

    api_url = 'http://api.openweathermap.org/data/2.5/forecast'
    payload = {
        'lat': park_lat,
        'lon': park_long,
        'appid': OWM_api_key}

    owm_req = requests.get(api_url, params=payload)

    print(owm_req.text)

    owm_json = json.loads(owm_req.text)

    sunrise_time = owm_json['city']['sunrise']
    sunset_time = owm_json['city']['sunset']
    tz_correct = owm_json['city']['timezone']

if __name__ == '__main__':
    weather_current()
