from django.urls import path
from .views import CreateCouponView, ClaimCouponView,CouponUsageView

urlpatterns = [
    path('', CreateCouponView.as_view()),
    path('<uuid:uuid>/claim/', ClaimCouponView.as_view()),
    path('<uuid:uuid>/usage/', CouponUsageView.as_view()),
]