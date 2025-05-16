from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendRestaurants),
    path('<uuid:uuid>', views.RestaurantDetailView.as_view())
]
