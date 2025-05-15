GET api/v1/restaurants/<id>

```python

API = {
    "result":{
        "restaurant": {
            "name": "麵屋武藏 本店",
            "address": "100台灣台北市中正區忠孝西路一段36號B1",
            "googleRating": 4.3,
            "placeId": "ChIJpabH4qapQjQRqmx_I-V8sUg",
            "imageUrl": "https:",
            "latitude": "",
            "longitude": "",
            "phone": "num" or None,
            "openHours": {
                "monday": "" or None,
                "tuesday": "" or None,
                "wednesday": "" or None,
                "thursday": "" or None,
                "firday": "" or None,
                "saturday": "" or None,
                "sunday": "" or None
            },
            "website": "",
            "userRatingsTotal": ""
        },
        "promotion": {
            "title": "",
            "description": "",
            "started_at": "",
            "ended_at": "",
            "image_url": ""
        } or None,
        "coupon": {
            "serial_number": "",
            "started_at": "",
            "ended_at": "",
            "title": "",
            "description": "",
            "discount_type": "",
            "discount_value": "",
            "uuid": ""
        } or None,
        "reviews": [
            {
                "user": "",
                "rating": "",
                "content": "",
                "created_at": "",
                "image_url": ""
            },
            ...
        ]
    }
}

```