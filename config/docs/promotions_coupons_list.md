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
PATCH /api/v1/coupons/<uuid:uuid>/




GET /api/v1/coupons/<uuid:uuid>/
API = {
    "result": {
        "restaurant": {
            "name": "金元寶炒飯",
            "imageUrl": "https://res.cloudinary.com/dtdsmynjy/image/upload/v1747368408/restaurants/ChIJl9MJJgmpQjQRrzEhGT-_Zp0.jpg"
        },
        "discount": "100元 折價券",
        "serialNumber": "CouponTest20250528",
        "endedAt": "2025-05-31T03:28:42Z",
        "createdAt": "2025-05-28T03:30:38.164597Z",
        "title": "測試餐廳Coupon",
        "description": "TEST",
        "discountType": "金額",
        "discountValue": 100,
        "total": 500,
        "isArchived": false,
        "startedAt": "2025-05-01T03:30:37Z",
        "uuid": "b65f0069-3bf5-4b0c-bdfa-96cc98040db4"
    }
}