import asyncio
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
        'darksky': os.getenv('API_KEY_DARK_SKY'),
        }


roots = {
        'openweather': f'https://api.openweathermap.org/data/2.5/weather?units=metric&appid={keys["openweather"]}',
        'weatherbit': f'https://api.weatherbit.io/v2.0/current?units=M&lang=en&key={keys["weatherbit"]}',
        'darksky': f'https://api.darksky.net/forecast/{keys["darksky"]}',
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
class OpenWeatherMap:
    def __init__(self, api_response):
        # percentage cloudiness
        self.cloudiness = safe_num(safe_dic(api_response, 'clouds'), 'all')
        # Data receiving time (unix, UTC)
        self.data_received_at = safe_num(api_response, 'dt')
        self.visibility = safe_num(api_response, 'visibility')
        # user's location
        self.city = safe_str(safe_dic(api_response, 'city'), 'name')
        self.country = safe_str(safe_dic(api_response, 'city'), 'country')
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


class WeatherBit:
    def __init__(self, data):
        self.sunrise = safe_str(data, 'sunrise') # Sunrise time (HH:MM).
        self.sunset = safe_str(data, 'sunset') # Sunset time (HH:MM).
        self.data_received_at = safe_num(data, 'ts') # Last observation time (Unix timestamp).
        self.city = safe_str(data, 'city_name')
        self.country = safe_str(data, 'country_code')
        self.state = safe_str(data, 'state_code') # State abbreviation/code.
        self.pressure = safe_num(data, 'pres') # Pressure (mb).
        self.pressure_sea = safe_num(data, 'slp') # Sea level pressure (mb).
        self.wind_speed = safe_num(data, 'wind_spd') # Wind speed (Default m/s).
        self.wind_direction = safe_num(data, 'wind_dir') # Wind direction (degrees).
        self.temperature = safe_num(data, 'temp') # Temperature (default Celcius).
        self.temperature_apparent = safe_num(data, 'app_temp') # Apparent/"Feels Like" temperature (default Celcius).
        self.humidity = safe_num(data, 'rh') # Relative humidity (%).
        self.dew_point = safe_num(data, 'despt') # Dew point (default Celcius).
        self.cloudiness = safe_num(data, 'clouds') # Cloud coverage (%).
        self.part_of_day = safe_str(data, 'pod') # Part of the day (d = day / n = night).
        self.descriptions = []
        if 'weather' in data and 'code' in data['weather']:
            self.descriptions.append({'title': data['weather']['code'], 'body': data['weather']['description']})
        self.visibility = safe_num(data, 'vis') # Visibility (default KM).
        self.precipitation = safe_num(data, 'precip') # Liquid equivalent precipitation rate (default mm/hr).
        self.snow = safe_num(data, 'snow') # Snowfall (default mm/hr).
        self.uv = safe_num(data, 'uv') # UV Index (0-11+).
        self.air_quality = safe_num(data, 'aqi') # Air Quality Index [US - EPA standard 0 - +500]
        self.dhi = safe_num(data, 'dhi') # Diffuse horizontal solar irradiance (W/m^2) [Clear Sky]
        self.dni = safe_num(data, 'dni') # Direct normal solar irradiance (W/m^2) [Clear Sky]
        self.ghi = safe_num(data, 'ghi') # Global horizontal solar irradiance (W/m^2) [Clear Sky]
        self.solar_radiation = safe_num(data, 'solar_rad') # Estimated Solar Radiation (W/m^2).
        self.solar_elevation = safe_num(data, 'elev_angle') # Solar elevation angle (degrees).
        self.solar_hour = safe_num(data, 'h_angle') # Solar hour angle (degrees).


async def get_weatherbit():
    res = requests.get(f'{roots["weatherbit"]}&lat=35&lon=139')
    result['wb'] = WeatherBit(res.json()['data'][0])


async def get_openweather():
    res = requests.get(f'{roots["openweather"]}&lat=35&lon=139')
    result['ow'] = OpenWeatherMap(res.json())


async def get_darksky():
    res = requests.get(f'{roots["darksky"]}/35,139')
    pprint(res.json()['currently'])


async def get_weather():
    loop.create_task(get_weatherbit())
    loop.create_task(get_openweather())
    loop.create_task(get_darksky())

try:
    result = {}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_weather())
    loop.close()
    pprint(result)
except Exception as e:
    print('there was an error')
    print(e)
