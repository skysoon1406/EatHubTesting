from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, ClaimCouponView, CouponUsageView

router = DefaultRouter()
router.register('', CouponViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:uuid>/claim/', ClaimCouponView.as_view()),
    path('<uuid:uuid>/usage/', CouponUsageView.as_view()),
]