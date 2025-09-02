from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
]
