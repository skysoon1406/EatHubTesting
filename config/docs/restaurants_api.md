POST api/v1/restaurants/

```python

body = {
    "flavors": ["日式", "韓式", "清蒸"],
    "mains": ["雞肉", "豬肉", "牛肉"],
    "staples": ["米飯", "麵條"],
    "userLocation": {
        "latitude": 25.0424,
        "longitude": 121.5137
    }
}

API = {
  "result": {
    "dish": "咖哩豬排飯",
    "restaurants": [
      {
        "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
        "name": "麵屋武藏 本店",
        "address": "100台灣台北市中正區忠孝西路一段36號B1",
        "google_rating": 4.3,
        "latitude": 25.0459993,
        "longitude": 121.5170414,
        "types": "restaurant,food,point_of_interest,establishment",
        "place_id": "ChIJpabH4qapQjQRqmx_I-V8sUg",
        "image_url": "https://res.cloudinary.com/.../麵屋.jpg",
        "phone": "02-2361-1000",
        "website": "https://example.com",
        "user_ratings_total": 1234,
        "google_photo_reference": "AXQ...abc"
      },
      {
        "uuid": "...",
        "name": "鳥人拉麵-西門店",
        ...
      }
      // 共 10 筆
    ]
  }
}
```