from django.urls import path
from qa_remote_controller.apps.main_page import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qa_main_page/', views.index_admin, name='index'),
]
