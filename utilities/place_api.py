import requests
import time
from dotenv import load_dotenv
import os

def text_search(keyword, location, radius,count=20):
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_API_KEY')
    query = keyword
    language = 'zh-TW'
    type = 'food'
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&language={language}&type={type}&key={API_KEY}'

    result = []

    while True:
        response = requests.get(url)
        data = response.json()

        if data.get('status') != 'OK':
            break

            for place in data.get('results', []):
                result.append({
                'name': place.get('name'),
                'address': place.get('formatted_address'),
                'rating': place.get('rating'),
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'types': place.get('types', []),
                'placeId': place.get('place_id'),
                })

                if len(result) >= count:
                    return result

        next_page_token = data.get('next_page_token')

        if next_page_token:
            time.sleep(3)
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&language={language}&type={type}&key={API_KEY}'
        else:
            break

    return result