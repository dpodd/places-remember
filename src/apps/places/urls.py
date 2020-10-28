from django.contrib import admin
from django.urls import path
from .views import profile, HomePageView

urlpatterns = [
    path('', HomePageView.as_view()),
]