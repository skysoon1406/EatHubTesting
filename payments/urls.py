from django.urls import path
from . import views

urlpatterns=[
    path('subscribe/', views.SubscriptionCreateView.as_view())
]