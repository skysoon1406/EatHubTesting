from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view()),
    path('login', views.LoginView.as_view()),
    path('me', views.MeView.as_view()),
    path('logout', views.LogoutView.as_view()),
]
