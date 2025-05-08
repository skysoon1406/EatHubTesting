from django.db import models
import uuid

# 店家會員
class MerchantUser(models.Model):
    name = models.CharField(max_length=255)  # 商家名稱或聯絡人名稱
    email = models.EmailField(unique=True, max_length=254)  # 聯絡信箱
    password = models.CharField(max_length=128)  # 密碼
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    is_vip = models.BooleanField(default=False)  # 是否為 VIP 商家
    img_url = models.URLField(max_length=255, blank=True, null=True)  # 商家照片
    license_number = models.CharField(max_length=255, blank=True, null=True)  # 執照編號（可無）
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='merchant_users') # 餐廳FK
    description = models.TextField(blank=True, null=True)  # 商家簡介
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid
