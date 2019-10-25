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
        'openweather': 'https://api.openweathermap.org/data/2.5/weather?units=metric',
        }


def safe_num(obj: dict, key: str):
    return obj[key] if key in obj else 0

def safe_str(obj: dict, key: str) -> str:
    return obj[key] if key in obj else ''


# https://openweathermap.org/weather-data
class OpenWeatherMap:
    def __init__(self, api_response):
        # percentage cloudiness
        self.cloudiness = safe_num(api_response['clouds'], 'all')
        # Data receiving time (unix, UTC)
        self.data_received_at = safe_num(api_response, 'dt')
        # percentage humidity
        self.humidity = api_response['main']['humidity']
        # pressure, Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data)
        self.pressure = api_response['main']['pressure']
        # temperature in celsius
        self.temperature = api_response['main']['temp']
        self.temperature_max = api_response['main']['temp_max']
        self.temperature_min = api_response['main']['temp_min']

try:
    url = f'{roots["openweather"]}&lat=35&lon=139&appid={keys["openweather"]}'
    res = requests.get(url)
    owmap = OpenWeatherMap(res.json())

    print('cloudiness:\t\t', owmap.cloudiness)
    print('data_received_at:\t', owmap.data_received_at)
    print('humidity:\t\t', owmap.humidity)
    print('pressure:\t\t', owmap.pressure)
    print('temperature:\t\t', owmap.temperature)
    print('temperature_max:\t', owmap.temperature_max)
    print('temperature_min:\t', owmap.temperature_min)

except Exception as e:
    print('there was an error')
    print(e)
