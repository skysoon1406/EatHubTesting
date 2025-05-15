GET api/v1/restaurants/<id>

```python

API = {
    "result":{
        "restaurant": {
            "name": "麵屋武藏 本店",
            "address": "100台灣台北市中正區忠孝西路一段36號B1",
            "googleRating": 4.3,
            "placeId": "ChIJpabH4qapQjQRqmx_I-V8sUg",
            "imageUrl": string | null,
            "latitude": 25.0459993,
            "longitude": 121.5170414,
            "phone": string | null,
            "openHours": {
                "monday": string | null,
                "tuesday": string | null,
                "wednesday": string | null,
                "thursday": string | null,
                "friday": string | null,
                "saturday": string | null,
                "sunday": string | null
            },
            "website": string | null,
            "userRatingsTotal": 123
        },
        "promotion": {
            "title": string,
            "description": string,
            "startedAt": "2025-05-15T12:34:56Z",
            "endedAt": "2025-05-15T12:34:56Z",
            "imageUrl": string | null
        } or null,
        "coupon": {
            "serialNumber": string,
            "startedAt": "2025-05-15T12:34:56Z",
            "endedAt": "2025-05-15T12:34:56Z",
            "title": string,
            "description": string,
            "discountType": string,
            "discountValue": 30,
            "uuid": string
        } or null,
        "reviews": [
            {
                "user": string,
                "rating": 5,
                "content": string,
                "createdAt": "2025-05-15T12:34:56Z",
                "imageUrl": string | null
            },
            ...
        ]
    }
}

```