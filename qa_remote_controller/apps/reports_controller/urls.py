from django.urls import path
from qa_remote_controller.apps.reports_controller import views

urlpatterns = [
    path('', views.index),
]
