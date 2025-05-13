from django.urls import path
from . import views

urlpatterns = [
    path('v1/auth/signup', views.SignupView.as_view()),
    path('v1/auth/login', views.LoginView.as_view()),
    path('v1/auth/me', views.MeView.as_view()),
    path('v1/auth/logout', views.LogoutView.as_view()),
]
