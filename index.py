import os
import requests
from dotenv import load_dotenv
from enum import Enum
from pprint import pprint
load_dotenv()

keys = {
        'openweather': os.getenv('API_KEY_OPEN_WEATHER_MAP'),
        }


roots = {
        'openweather': 'https://api.openweathermap.org/data/2.5/weather',
        }


# https://openweathermap.org/weather-data
class OpenWeatherMap:
    def __init__(self, api_response):
        # percentage cloudiness
        self.cloudiness = api_response['clouds']['all']
        # Data receiving time (unix, UTC)
        self.data_received_at = api_response['dt']
        # percentage humidity
        self.humidity = api_response['main']['humidity']

try:
    url = f'{roots["openweather"]}?lat=35&lon=139&appid={keys["openweather"]}'
    res = requests.get(url)
    owmap = OpenWeatherMap(res.json())
    print(owmap.cloudiness, owmap.data_received_at)
except Exception as e:
    print('there was an error')
    print(e)
