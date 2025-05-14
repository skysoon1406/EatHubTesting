from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendRestaurants),
    path('<uuid:restaurant_uuid>/reviews', views.create_review),
]
