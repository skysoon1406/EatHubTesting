最新動態與優惠券清單

GET /api/v1/merchants/me/

```python

API = {
    "result": {
        "restaurant": {
            "name": "麵屋武藏 本店",
            "uuid": "8eb03a32-d421-4c41-a614-fdf0fa9ea651"
        }
        "promotions": [
            {
            "title": "週年慶活動",
            "description": string,
            "created_at":"2025-05-12T12:34:56Z",
            "started_at": "2025-05-15T12:34:56Z",
            "ended_at": "2025-05-15T12:34:56Z",
            "image_url": string | null,
            "uuid": "d123e456-78ab-90cd-ef12-345678901234"
             },
        ]
        "coupons": [
            {
            "serial_number": "ABC123XYZ",
            "created_at":"2025-05-15T12:34:56Z",
            "started_at": "2025-05-15T12:34:56Z",
            "ended_at": "2025-05-15T12:34:56Z",
            "title": "買一送一",
            "description": "限內用，僅限週末使用",
            "discount": string,
            "total": 100,
            "uuid": "f234e567-89bc-01de-gh23-456789012345",
            "redeemed_count": 42,
            "used_count": 18,

            }
        ]
    }
}
```

軟刪除最新動態、優惠券
PATCH /api/v1/promotions/<uuid:uuid>/
GET /api/v1/promotions/<uuid:uuid>/

```PYTHON
{
  "result": {
    "uuid": "ed07f9ea-98c7-43d9-93a0-b9e9e1ab2b3a",
    "title": "夏季優惠大放送",
    "description": "指定套餐買一送一！活動期間內所有套餐都享有優惠，歡迎來店體驗。",
    "started_at": "2025-06-01T00:00:00Z",
    "ended_at": "2025-06-15T23:59:59Z",
    "image_url": "https://res.cloudinary.com/xxx/promo1.jpg",
    "created_at": "2025-05-23T12:00:00Z",
    "updated_at": "2025-05-23T12:00:00Z",
    "is_active": true
  }
}
```

PATCH /api/v1/coupons/<uuid:uuid>/
