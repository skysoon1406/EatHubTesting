from django.urls import path
from . import views

urlpatterns=[
    path('products/', views.ProductListView.as_view()),
    path('linepay/subscribe/', views.SubscriptionCreateView.as_view()),
    path('linepay/confirm/', views.LinePayConfirmView.as_view()),
]