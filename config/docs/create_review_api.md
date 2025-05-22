POST /api/v1/restaurants/{restaurant_uuid}/reviews/
說明：對指定餐廳新增留言，需要登入。

認證方式：
    -類型：自訂 Token (存在Cookie中)
    -Cookie名稱：auth_token
    -格式：user_uuid:token

Request Body :
(Content-Type: application/json)
{
    'rating':5,
    'content':'這家餐廳很好吃，環境也很棒！',
    'image_bytes':(非必填) 圖片會上傳至雲端
}
圖片限制：
單張圖片大小限制為：1MB
超過限制：回傳錯誤訊息
檔案欄位名稱：image

Success Respones [201 Created]:
{
  "uuid": "70b31c60-c2c6-4fe1-8b41-22e49d1f9282",
  "user": {
    "userName": 'ext',
    "imageUrl": 'null,
    "uuid": "2a1b...fa21"
  },
  "restaurant": '15',
  "rating":'5',
  "content": "好吃",
  "created_at": "2025-05-21T09:13:03.784073Z",
  "image_url": "https://res...jpg"
}

Error Respones [404 Not Found]:
    -找不到該餐廳
Error Respones [401 Unauthorized]:
    -未提供Token
Error Respones [400 Bad Request]:
    -image_url: ["Enter a valid URL."]
    -detail": 該餐廳已評論過。