from django.urls import path
from . import views

urlpatterns=[
    path('subscribe/', views.SubscriptionCreateView.as_view()),
    path('order-status/<str:order_id>/', views.LinePayOrderStatusView.as_view()),
]