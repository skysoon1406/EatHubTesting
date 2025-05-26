from django.urls import path
from .views import MerchantDashboardView

urlpatterns = [
    path('me/', MerchantDashboardView.as_view()),
]