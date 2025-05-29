from django.db import models
from django.utils import timezone
import uuid
from users.models import User

# Create your models here.
class Subscription (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    product_name = models.CharField(max_length=100)
    start_data = models.DateField(auto_created=True)
    next_payment_data = models.DateField()
    interval_days = models.IntegerChoices(default=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.user_name} 訂閱 {self.product_name}'

class PaymentOrder(models.Model):
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_orders')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_oders')
    amout = models.ImageField()
    product_name = models.CharField(max_length=100)
    ia_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = timezone.now().strftime('%Y%M%D')
            random_suffix = uuid.uuid4().hex[:8]
            self.order_id = f'order_{today}_{random_suffix}'
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_id}-{'已付款' if self.is_paid else '未付款'}'
    