import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("weather_api_key")

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": f"{city},IN", "appid": API_KEY, "units": "metric"}
    headers = {"User-Agent": "Mozilla/5.0"}

    data = requests.get(url, params=params, headers=headers).json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rain = data.get("rain", {}).get("1h", 0)
    soil = rain * 2

    return temp, humidity, rain, soil
