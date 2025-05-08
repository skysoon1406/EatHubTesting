from django.db import models
import uuid

# 最新消息
class Promotion(models.Model):
    title = models.CharField(max_length=255)  # 活動標題
    description = models.TextField(blank=True, null=True)  # 活動描述
    started_at = models.DateTimeField(blank=True, null=True)  # 活動開始時間
    ended_at = models.DateTimeField(blank=True, null=True)    # 活動結束時間
    created_at = models.DateTimeField(auto_now_add=True)      # 建立時間
    merchant = models.ForeignKey('merchants.MerchantUser', on_delete=models.CASCADE, related_name='promotions')  # 商家
    img_url = models.URLField(max_length=255, blank=True, null=True)  # 活動圖片
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

# 酷碰卷
class Coupon(models.Model):
    serial_number = models.CharField(max_length=255)  # 序號
    expired_at = models.DateTimeField(blank=True, null=True)  # 到期日
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    merchant = models.ForeignKey('merchants.MerchantUser', on_delete=models.CASCADE, related_name='coupons')  # 發行商家
    title = models.CharField(max_length=255)  # 折扣名稱
    description = models.TextField(blank=True, null=True)  # 說明文字
    discount_type = models.CharField(max_length=255)  # 折扣型態，例如 %、金額
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 折扣數值
    total = models.IntegerField(blank=True, null=True)  # 發行數量
    is_archived = models.BooleanField(default=False)  # 是否封存/下架
    started_at = models.DateTimeField(blank=True, null=True)  # 可使用起始時間
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid
