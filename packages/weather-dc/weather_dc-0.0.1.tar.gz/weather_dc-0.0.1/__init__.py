import pandas as pd
import requests
from bs4 import BeautifulSoup

def weather():
    page = requests.get('https://forecast.weather.gov/MapClick.php?lat=38.8904&lon=-77.032#.YB-IN2gzbaI')
    soup = BeautifulSoup(page.content, 'html.parser')
    week = soup.find(id='seven-day-forecast-body')
    items = week.find_all(class_='tombstone-container')

    print('Washington DC')
    period_names = [item.find(class_='period-name').get_text() for item in items]
    short_desc = [desc.find(class_='short-desc').get_text() for desc in items]
    temp = [temp.find(class_='temp').get_text() for temp in items]

    weather_stuff = pd.DataFrame(
        {
            'period': period_names,
            'short_desc': short_desc,
            'temp': temp,
        })

    print(weather_stuff)

    weather_stuff.to_csv('weather.csv')