from django.urls import path
from .views import MerchantView,CouponDetailView

urlpatterns = [
    path('me/', MerchantView.as_view()),
]