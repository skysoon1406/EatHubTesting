我的收藏清單（查詢登入使用者已收藏的餐廳）

GET /api/v1/favorites/

Cookie: auth_token={user_uuid}:{token}

Success Response [200 OK]:
"""
{
    "restaurants": [
        {
            "name": "早餐店",
            "address": "蘆竹區南山北路二段32號",
            "latitude": 25.0956169,
            "longitude": 121.2777358,
            "phone": null,
            "openHours": null,
            "googleRating": 4.7,
            "placeId": "ChIJz4-jN0uhQjQRGhy3f6Y80PU",
            "imageUrl": null,
            "website": null,
            "userRatingsTotal": 7,
            "googlePhotoReference": "AXQCQNTFrXVfsaYcPkCizUlvrekvvMdPum9t-nh3flBpLWUeK_4-7-iD_yCI0G5ci4jtYkI1o-VvNfWa6brSF9NlJ-9VPsk9nwueO1PBTf4ZQFR_36nZt4KUbBpX2T_VjQKmcdfcW8SNB9SM1uPETz5vWYxNz7cVJQ83PlMYrkyEYytkDcSOGrkJtiELadRJfh0Fy_SnPn9tuhpCS_TUgcA82BfVRuBV4NYUFcdbEjdvmkcJwZS9XPE45f1D5qMQU7NNNfwQXoz9c3zTCrhxcggX0p0NjvdhSK1MkzA4949bIOzoyE8nhwixU-QeKxmNklJcx1aKbodZ8vSiBAuJbFSm3vfxLIBkwkwF6XzEgBbFFDlcyIGPZ1MK3Uqj9KeVI0vy8zR7Kt_d-qoc3Ov5Y21FhVe0N6YlKyzYTnAWVcUU0XwqWwiT-31XXETuQvWufW0-8ViEv9t4kL2AgDEcJcgTsLxr2KrvcrQfigibVKA5A4_s5a66PO_gpGDq4JhSQX_tRrBkRdYStBdY0qPGElYxVg5vNT_pQhFNqEHwkSU1cKgcnRFP03FkwsXEEA1VZH3iBBEJluNsNwPCHTGdqxy9vwdfDdZ-eyQe72yx3n-dZ55vrDSOsxketK30oVV3m3rT",
            "types": "restaurant,food,point_of_interest,establishment",
            "uuid": "8eb03a32-d421-4c41-a614-fdf0fa9ea651"
        },
        {
            "name": "尚豪轟炸雞翅（坑口店）",
            "address": "蘆竹區南山北路二段394號",
            "latitude": 25.1064591,
            "longitude": 121.2751541,
            "phone": null,
            "openHours": null,
            "googleRating": 4.9,
            "placeId": "ChIJEa6DZgChQjQRygS95FJ4xyU",
            "imageUrl": null,
            "website": null,
            "userRatingsTotal": 16,
            "googlePhotoReference": "AXQCQNTqFBY71vuZIkfyDEnslxHc3VYhNX8zNxyNaB_KSR2-qATCgtCK7mV5-XNbmnOwNPvYqDYOaLpFicoGME2VGcufPDQ1z0pdUtWXra_Y4ogpwCz4irj0L1DCdRY4ByHObB9GaVMeWvK8QmK6G8xR5dLB6jikMpU2GCq6ZD4vESvcqtMX6trw7JG7CdHbMJ5u7SABAZSvcUb8I_i-t0dzz65sg9mOTdZnbof-KADVO33Xz8Bc-lJtlOjahKXP3DsjZY9OSi7wrgvMS7YYhpDFbunMQhe5YZ3yhifH07gcxNSxxfHyonTpSg3VP38RYOr-eEg2u30ZpWs",
            "types": "meal_takeaway,restaurant,food,point_of_interest,establishment",
            "uuid": "8d5b46db-8337-4b45-a455-d0408cb13f85"
        }
    ]
}
"""
Error Response [401 Unauthorized]:
	未提供 token
	Token 無效或過期

收藏餐廳

POST /api/v1/restaurants/{uuid}/favorites/

Cookie:	auth_token={user_uuid}:{token}

Success Response [201 Created]:
"""
{
  "success": true
}
"""
Error Response [400 Bad Request]:
	該餐廳已經收藏過

Error Response [401 Unauthorized]:
	未登入

取消收藏

DELETE /api/v1/restaurants/{uuid}/favorites/

Cookie:	auth_token={user_uuid}:{token}

Success Response [204 No Content]:
"""
{
  "success": true
}
"""
Error Response [200 OK]:
	該餐廳沒有收藏紀錄（也會回 success: false）

Error Response [401 Unauthorized]:
	未登入
