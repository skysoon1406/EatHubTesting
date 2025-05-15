from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendRestaurants),
    path('test_upload_image', views.test_upload_image),
    path('test', views.testRestaurants),
]
