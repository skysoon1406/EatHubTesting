import requests
import time
from dotenv import load_dotenv
import os

def text_search(keyword, location, radius):
    API_KEY = os.getenv("Google_API_KEY")
    query = keyword
    language = "zh-TW"
    type = "food"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&language={language}&type={type}&key={API_KEY}"

    all_data = []

    while True:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "OK":
            break

        all_data.append(data)
        next_page_token = data.get("next_page_token")

        if next_page_token:
            time.sleep(3)
        else:
            break

    return all_data