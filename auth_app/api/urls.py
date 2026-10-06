from django.contrib import admin
from django.urls import path, include
from .views import RegistrationView, LoginView

urlpatterns = [
    path("registration/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
]