from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, ClaimCouponView

router = DefaultRouter()
router.register('', CouponViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:uuid>/claim/', ClaimCouponView.as_view())
]