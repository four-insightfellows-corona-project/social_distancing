#!/usr/bin/env python3

'''
Captures the 5 day / 3 hour forcasts from OpenWeatherMap API.

Note: In order for this to work you need to install the
develop branch of pyowm, this can be done using:

    pip install git+https://github.com/csparpa/pyowm.git@develop

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

src_dir = os.path.join(os.getcwd(), '..', '..')
root_dir = os.path.join(os.getcwd(), '..', '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from conf.auth import OWM_api_key

owm = pyowm.OWM(OWM_api_key)

park_loc = pd.DataFrame({
    'name': ['Prospect Park', 'Wooster Square'],
    'lat': [40.662551, 41.304745],
    'long': [-73.969256, -72.917757]})

OWM_forcast_cols = ['park_name', 'reception_time', 'reference_time',
                    'sunset_time', 'sunrise_time', 'clouds', 'rain', 'snow',
                    'wind_speed', 'wind_deg', 'humidity', 'press', 'press_sea',
                    'temp', 'temp_feels', 'temp_max', 'temp_min', 'status',
                    'detailed_status']


def forcast_to_df(park_name, park_forcast, t_sunrise, t_sunset, tz_correct):
    ''' Takes a forcast object and sunrise/sunset time,
        Returns datafram of relevant info
    '''
    # Neet to adjust sunrise/set times, should only go
    # into columns of the same day (or just use last day in window?)

    forcast_df = pd.DataFrame(columns=OWM_forcast_cols)

    for x in park_forcast.weathers:
        if (t_sunrise == 0) or (t_sunset == 0):
            x_sunrise = np.nan
            x_sunset = np.nan
        else:
            x_sunrise = t_sunrise + tz_correct
            x_sunset = t_sunset + tz_correct

        x_rain = 0
        if x.rain:
            x_rain = x.rain['3h']

        x_snow = 0
        if x.snow:
            x_snow = x.snow['3h']

        to_add_dict = {
            'park_name': [park_name],
            'reception_time': [park_forcast.reception_time('unix') + tz_correct],
            'reference_time': [x.reference_time() + tz_correct],
            'sunrise_time': [x_sunrise],
            'sunset_time': [x_sunset],
            'clouds': [x.clouds],
            'rain': [x_rain],
            'snow': [x_snow],
            'wind_speed': [x.wind(unit='meters_sec')['speed']],
            'wind_deg': [x.wind(unit='meters_sec')['deg']],
            'humidity': [x.humidity],
            'press': [x.pressure['press']],
            'press_sea': [x.pressure['sea_level']],
            'temp': [x.temperature(unit='fahrenheit')['temp']],
            'temp_feels': [x.temperature(unit='fahrenheit')['feels_like']],
            'temp_max': [x.temperature(unit='fahrenheit')['temp_max']],
            'temp_min': [x.temperature(unit='fahrenheit')['temp_min']],
            'status': [x.status],
            'detailed_status': [x.detailed_status]}

        to_add = pd.DataFrame(to_add_dict)
        forcast_df = forcast_df.append(to_add, ignore_index=True)
    return forcast_df


def main():
    '''
    '''
    park_name = 'Prospect Park'
    park_lat = park_loc.loc[park_loc.name == park_name, 'lat'].iloc[0]
    park_long = park_loc.loc[park_loc.name == park_name, 'long'].iloc[0]

    api_url = 'http://api.openweathermap.org/data/2.5/forecast'
    payload = {
        'lat': park_lat,
        'lon': park_long,
        'appid': OWM_api_key}

    owm_req = requests.get(api_url, params=payload)

    owm_json = json.loads(owm_req.text)

    sunrise_time = owm_json['city']['sunrise']
    sunset_time = owm_json['city']['sunset']
    tz_correct = owm_json['city']['timezone']

    park_forecast = Forecast.from_dict(json.loads(owm_req.text))

    weather_df = forcast_to_df(
        park_name, park_forecast,
        sunrise_time, sunset_time, tz_correct)

    # log_path = data_file_path('weather_data', 'weather_log.csv')
    log_path = os.path.join(root_dir, 'data', 'weather_log.csv')

    if os.path.exists(log_path):
        weather_log = pd.read_csv(log_path, index_col=0)
    else:
        weather_log = pd.read_csv(
            os.path.join(root_dir, 'data', 'example_weather_df.csv'), index_col=0)

    weather_log = weather_log.append(weather_df, ignore_index=True)

    weather_log.to_csv(log_path)


if __name__ == "__main__":
    main()
