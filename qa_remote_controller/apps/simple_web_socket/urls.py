from django.urls import path
from django.urls import re_path

from qa_remote_controller.apps.simple_web_socket import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:cache_hash>/', views.saved_text, name='saved_text'),
]
