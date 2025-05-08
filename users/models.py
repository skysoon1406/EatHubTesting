from django.db import models
import uuid 
# 使用者
class User(models.Model):
    user_name = models.CharField(max_length=100)  # 使用者暱稱或顯示名
    email = models.EmailField(unique=True, max_length=254)  # Email 標準最大長度
    password = models.CharField(max_length=128)  # 密碼加密後最大長度為 128
    first_name = models.CharField(max_length=50, blank=True, null=True)  # 名
    last_name = models.CharField(max_length=50, blank=True, null=True)   # 姓
    img_url = models.URLField(max_length=300, blank=True, null=True)     # 頭像網址
    created_at = models.DateTimeField(auto_now_add=True)  # 註冊時間
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #uuid

# 使用者酷碰卷
class UserCoupon(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='coupons') #使用者FK
    coupon = models.ForeignKey('promotions.Coupon', on_delete=models.CASCADE, related_name='claimed_by') #酷碰FK
    claimed_at = models.DateTimeField(auto_now_add=True)  # 預設為領取時自動填入
    used_at = models.DateTimeField(blank=True, null=True)  # 使用時再更新
    is_used = models.BooleanField(default=False) #是否使用
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #uuid

