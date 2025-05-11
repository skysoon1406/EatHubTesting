from django.urls import path
from . import views

urlpatterns = [
    path("v1/auth/signup", views.SignupView.as_view(), name="signup"),
    path("v1/auth/login", views.LoginView.as_view(), name="login"),
]
