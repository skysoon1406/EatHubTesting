from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
# 餐廳
class Restaurant(models.Model):
    name = models.CharField(max_length=255)  # 餐廳名稱
    address = models.CharField(max_length=255)  # 餐廳地址
    latitude = models.FloatField()  # 緯度
    longitude = models.FloatField()  # 經度
    phone = models.CharField(max_length=255, blank=True, null=True)  # 聯絡電話，可空
    open_hours = models.TextField(blank=True, null=True)  # 營業時間，可空
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間，自動填入
    google_rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=True,
        null=True
        )  # Google 評分（例如 1~5 顆星）
    place_id = models.CharField(max_length=100, unique=True)  # Google Maps 的 place_id
    img_url = models.URLField(max_length=255, blank=True, null=True)  # 圖片網址，可空
    url = models.URLField(max_length=255, blank=True, null=True)  # Google Map 網址，可空
    formatted_address = models.CharField(max_length=255, blank=True, null=True)  # Google 格式化地址，可空
    website = models.URLField(max_length=255, blank=True, null=True)  # 官網網址，可空
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

# 評論
class Review(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')  # 對應評論者FK
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='reviews')  # 被評論餐廳FK
    rating = models.IntegerField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=True,
        null=True
    )  # 評分，允許浮點數，0 到 5 分之間
    content = models.TextField()  # 評論內容（不限長度）
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間（自動填入）
    img_url = models.URLField(max_length=255, blank=True, null=True)  # 可附一張評論圖片
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

# 收藏
class Favorite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorites')  # 收藏者FK
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='favorited_by')  # 被收藏的餐廳FK
    created_at = models.DateTimeField(auto_now_add=True)  # 收藏時間，自動產生
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

