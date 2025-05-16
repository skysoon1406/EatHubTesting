from django.urls import path
from .views import UserCouponListView

urlpatterns = [
    path('', UserCouponListView.as_view()), 
]