# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index_page, name='index'),
    path('compare/', views.compare, name='compare'),
    path('check-tests/', views.check_tests, name='check_tests')
]