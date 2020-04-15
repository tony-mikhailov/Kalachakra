from django.urls import path
from rest_framework.urls import app_name

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]