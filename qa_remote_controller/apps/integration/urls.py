from django.urls import path

from qa_remote_controller.apps.integration import views

urlpatterns = [
    path('', views.index, name='index'),
]
