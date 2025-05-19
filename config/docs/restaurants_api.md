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
    "result":[
        {
            "name": "麵屋武藏 本店",
            "address": "100台灣台北市中正區忠孝西路一段36號B1",
            "googleRating": 4.3,
            "latitude": 25.0459993,
            "longitude": 121.5170414,
            "types": [
                "restaurant",
                "food",
                "point_of_interest",
                "establishment"
            ],
            "placeId": "ChIJpabH4qapQjQRqmx_I-V8sUg",
            "imageUrl": "https:"
        },
        {
            "name": "鳥人拉麵-西門店",
            ...
        },
        {
            "name": "哥極拉麵 本店",
            ...
        }
        ...
        # 共 10 筆
    ]
}
```