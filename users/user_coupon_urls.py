from django.urls import path
from .views import UserCouponListView, UserCouponDeleteView

urlpatterns = [
    path('', UserCouponListView.as_view()), 
    path('<uuid:uuid>/', UserCouponDeleteView.as_view()),
]