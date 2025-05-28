from django.urls import path
from .views import CreateCouponView, ClaimCouponView,CouponUsageView,CouponDetailView

urlpatterns = [
    path('', CreateCouponView.as_view()),
    path('<uuid:coupon_uuid>/',CouponDetailView.as_view()),
    path('<uuid:uuid>/claim/', ClaimCouponView.as_view()),
    path('<uuid:uuid>/usage/', CouponUsageView.as_view()),
]