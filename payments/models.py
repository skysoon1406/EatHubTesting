from django.db import models
from django.utils import timezone
import uuid
from users.models import User

# Create your models here.
class Product(models.Model):
    PLAN_CHOICES = [
        ('monthly', '月訂閱'),
        ('yearly', '年訂閱'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    amount = models.IntegerField()
    interval_days = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.get_plan_type_display()}'
    
class Subscription (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    product= models.ForeignKey(Product, on_delete=models.PROTECT, default=1)
    start_date = models.DateField(auto_now_add=True)
    ended_at = models.DateField(blank=True, null=True)
    next_payment_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.next_payment_date:
            self.next_payment_date = timezone.now().date() + timezone.timedelta(days=self.product.interval_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.user_name} 訂閱 {self.product}'

class PaymentOrder(models.Model):
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_orders' )
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=1)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = timezone.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:8]
            self.order_id = f'order_{today}_{random_suffix}'
        super().save(*args, **kwargs)

    def __str__(self):
        status = '已付款' if self.is_paid else '未付款'
        return f'{self.order_id} - {status}'
    
