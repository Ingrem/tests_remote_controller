from django.urls import path

from qa_remote_controller.apps.bc_mock_controller import views

urlpatterns = [
    path('', views.index, name='index'),
]