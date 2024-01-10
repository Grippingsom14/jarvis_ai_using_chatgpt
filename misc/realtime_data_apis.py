import os
import datetime
import requests
from dotenv import load_dotenv
load_dotenv()


def get_realtime_data(data_category, query=""):
    if data_category == 'time':
        return datetime.time

    elif data_category == 'date':
        return datetime.date

    elif data_category == 'news':
        api_url = (f"https://newsapi.org/v2/top-headlines?country=in&pageSize=3&page=1&apiKey={os.getenv('NEWSAPI_APIKEY')}")
        response = requests.get(f"{api_url}")
        if response.status_code == 200:
            return response.json()
        else:
            return "weather data is not available right now"

    elif data_category == 'weather':
        api_url = ("https://api.open-meteo.com/v1/forecast?latitude=22.578132&longitude=88.390158&temperature_unit"
                   "=celsius&current_weather=true&daily=sunrise,sunset&current=is_day,rain,showers,"
                   "snowfall&timezone=Asia/Kolkata&forecast_days=1")

        response = requests.get(f"{api_url}")
        if response.status_code == 200:
            return response.json()
        else:
            return "weather data is not available right now"

