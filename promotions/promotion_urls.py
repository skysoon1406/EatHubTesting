from django.urls import path
from .views import PromotionDetailView

urlpatterns = [
    
    path('<uuid:promotion_uuid>/', PromotionDetailView.as_view()),
    
]