POST /api/v1/restaurants/{restaurant_uuid}/reviews
說明：對指定餐廳新增留言，需要登入。

認證方式：
    -類型：自訂 Token (存在Cookie中)
    -Cookie名稱：auth_token
    -格式：user_uuid:token

Request Body :

{
    'rating':'5',
    'content':'這家餐廳很好吃，環境也很棒！',
    'image_url':'https://example.com/photo.jpg' /非必填
}

Success Respones [201 Created]:
{
    "uuid": "d1e8d...abc1",
    "user": 5,
    "restaurant": 10,
    "rating": 5,
    "content": "這家餐廳很好吃，環境也很棒！",
    "img_url": "https://example.com/photo.jpg",
    "created_at": "2025-05-14T15:01:32Z"
}

Error Respones [404 Not Found]:
    -找不到該餐廳
Error Respones [401 Unauthorized]:
    -未提供Token
Error Respones [400 Bad Request]:
    -This field is required.