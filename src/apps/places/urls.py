from django.urls import path
from .views import profile_view, memory_view

urlpatterns = [
    path('', profile_view),
    path('<int:pk>/', memory_view, name='memory_detail'),
]