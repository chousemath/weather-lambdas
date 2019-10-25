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


# https://samples.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid=b6907d289e10d714a6e88b30761fae22
try:
    url = f'{roots["openweather"]}?lat=35&lon=139&appid={keys["openweather"]}'
    res = requests.get(url)
    pprint(res.json())
except Exception as e:
    print('there was an error')
    print(e)
