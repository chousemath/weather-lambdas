import os
import requests
from dotenv import load_dotenv
from enum import Enum
from pprint import pprint
from typing import List
load_dotenv()

keys = {
        'openweather': os.getenv('API_KEY_OPEN_WEATHER_MAP'),
        'weatherbit': os.getenv('API_KEY_WEATHER_BIT'),
        }


roots = {
        'openweather': f'https://api.openweathermap.org/data/2.5/weather?units=metric&appid={keys["openweather"]}',
        'weatherbit': f'https://api.weatherbit.io/v2.0/current?units=M&lang=en&key={keys["weatherbit"]}'
        }

def safe_arr(obj: dict, key: str) -> List:
    return obj[key] if key in obj else []

def safe_dic(obj: dict, key: str) -> dict:
    return obj[key] if key in obj else {}

def safe_num(obj: dict, key: str):
    return obj[key] if key in obj else 0

def safe_str(obj: dict, key: str) -> str:
    return obj[key] if key in obj else ''

def extract_desc(weather_desc) -> dict:
    return {
            'title': weather_desc['main'].lower(),
            'body': weather_desc['description'],
            }

# https://openweathermap.org/weather-data
class WeatherReport:
    def __init__(self, api_response):
        # percentage cloudiness
        self.cloudiness = safe_num(safe_dic(api_response, 'clouds'), 'all')
        # Data receiving time (unix, UTC)
        self.data_received_at = safe_num(api_response, 'dt')
        self.visibility = safe_num(api_response, 'visibility')
        # percentage humidity
        self.humidity = safe_num(safe_dic(api_response, 'main'), 'humidity')
        # pressure, Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data)
        self.pressure = safe_num(safe_dic(api_response, 'main'), 'pressure')
        self.pressure_sea = safe_num(safe_dic(api_response, 'main'), 'sea_level')
        self.pressure_ground = safe_num(safe_dic(api_response, 'main'), 'grnd_level')
        # temperature in celsius
        self.temperature = safe_num(safe_dic(api_response, 'main'), 'temp')
        self.temperature_max = safe_num(safe_dic(api_response, 'main'), 'temp_max')
        self.temperature_min = safe_num(safe_dic(api_response, 'main'), 'temp_min')
        self.rain_vol_1h = safe_num(safe_dic(api_response, 'rain'), '1h')
        self.rain_vol_3h = safe_num(safe_dic(api_response, 'rain'), '3h')
        self.snow_vol_1h = safe_num(safe_dic(api_response, 'snow'), '1h')
        self.snow_vol_3h = safe_num(safe_dic(api_response, 'snow'), '3h')
        self.sunrise = safe_num(safe_dic(api_response, 'sys'), 'sunrise')
        self.sunset = safe_num(safe_dic(api_response, 'sys'), 'sunset')
        self.country = safe_num(safe_dic(api_response, 'sys'), 'country')
        # wind speed in meter/sec
        self.wind_speed = safe_num(safe_dic(api_response, 'wind'), 'speed')
        # wind direction in degrees
        self.wind_direction = safe_num(safe_dic(api_response, 'wind'), 'deg')
        # wind gust in meter/sec
        self.wind_gust = safe_num(safe_dic(api_response, 'wind'), 'gust')
        # https://openweathermap.org/weather-conditions
        self.descriptions = [extract_desc(x) for x in safe_arr(api_response, 'weather')]


try:
    url = f'{roots["openweather"]}&lat=35&lon=139'
    res = requests.get(url)
    owmap = WeatherReport(res.json())

    print('cloudiness:\t\t', owmap.cloudiness)
    print('data_received_at:\t', owmap.data_received_at)
    print('humidity:\t\t', owmap.humidity)
    print('pressure:\t\t', owmap.pressure)
    print('temperature:\t\t', owmap.temperature)
    print('temperature_max:\t', owmap.temperature_max)
    print('temperature_min:\t', owmap.temperature_min)
    print('rain_vol_1h:\t\t', owmap.rain_vol_1h)
    print('rain_vol_3h:\t\t', owmap.rain_vol_3h)
    print('snow_vol_1h:\t\t', owmap.snow_vol_1h)
    print('snow_vol_3h:\t\t', owmap.snow_vol_3h)
    print('descriptions:\t\t', owmap.descriptions)
    print('sunset:\t\t\t', owmap.sunset)
    print('sunrise:\t\t', owmap.sunrise)
    print('country:\t\t', owmap.country)
    print('wind_speed:\t\t', owmap.wind_speed)
    print('wind_direction:\t\t', owmap.wind_direction)
    print('wind_gust:\t\t', owmap.wind_gust)
    pprint(res.json())

except Exception as e:
    print('there was an error')
    print(e)
