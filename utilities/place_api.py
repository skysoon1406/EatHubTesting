import requests
import time
from dotenv import load_dotenv
import os

GOOGLE_MAP_API_BASE_URL = 'https://maps.googleapis.com/maps/api/place'
load_dotenv()

def text_search(keyword, location, radius, count=61):
    API_KEY = os.getenv('GOOGLE_API_KEY')
    query = keyword
    language = 'zh-TW'
    url = f'{GOOGLE_MAP_API_BASE_URL}/textsearch/json?query={query}&location={location}&radius={radius}&language={language}&key={API_KEY}'

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
                'google_rating': place.get('rating'),
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'types': place.get('types', []),
                'place_id': place.get('place_id'),
                'user_ratings_total': place.get('user_ratings_total'),
                'google_photo_reference': (
                    place.get('photos', [{}])[0].get('photo_reference')
                    if place.get('photos') else None
                )
            })

            if len(result) >= count:
                return result

        next_page_token = data.get('next_page_token')

        if next_page_token:
            time.sleep(3)
            url = f'{GOOGLE_MAP_API_BASE_URL}/textsearch/json?pagetoken={next_page_token}&key={API_KEY}'
        else:
            break

    return result

def get_google_photo(photo_reference, max_width = 400):
    API_KEY = os.getenv('GOOGLE_API_KEY')

    url = (
        'https://maps.googleapis.com/maps/api/place/photo'
        f'?maxwidth={max_width}&photo_reference={photo_reference}&key={API_KEY}'
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None