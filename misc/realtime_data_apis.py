import os
import sys
import datetime
import time
import json
import requests
from dotenv import load_dotenv
load_dotenv()
cached_weather_data = ''
cached_news_data = ''


def get_realtime_data(data_category, query=""):
    if data_category == 'datetime':
        # datetime_json = json.loads(datetime.datetime.now().strftime("{\"date\": \"%Y-%m-%d\", \"time\": \"%H:%M\"}"))
        # return datetime_json
        return datetime.datetime.now()

    elif data_category == 'news':
        def extract_source_and_title(data):
            # Load JSON data from string
            articles_data = data

            # Extract the relevant information
            extracted_data = [
                {"source": article["source"]["name"], "title": article["title"]}
                for article in articles_data["articles"]
            ]

            return extracted_data

        api_url = (f"https://newsapi.org/v2/top-headlines?country=in&pageSize=3&page=1&apiKey={os.getenv('NEWSAPI_APIKEY')}")
        response = requests.get(f"{api_url}")
        if response.status_code == 200:
            return extract_source_and_title(response.json())
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

