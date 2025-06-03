# payment_flow.py
import uuid
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from payments.models import PaymentOrder, Subscription


def prepare_payment_order(user, product, amount):
    #建立付款訂單前，確認是否在 7 天內可以續訂。
    today = timezone.now().date()
    latest_sub = Subscription.objects.filter(user=user).order_by('-ended_at').first()

    if latest_sub and latest_sub.ended_at and latest_sub.ended_at >= today:
        days_remaining = (latest_sub.ended_at - today).days
        if days_remaining > 7:
            raise ValidationError(f'尚未到期，目前剩餘 {days_remaining} 天，請於到期前 7 日內續訂。')
        start_date = latest_sub.ended_at +timedelta(days=1)
    else:
        start_date = today

    next_date = start_date + timedelta(days=product.interval_days -1)

    order_id = f"order_{today.strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
    payment_order = PaymentOrder.objects.create(
        order_id=order_id,
        user=user,
        subscription=None,  # 訂閱待確認付款成功後建立
        amount=amount,
        product=product,
        is_paid=False
    )

    return payment_order, start_date, next_date
