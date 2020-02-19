from django.urls import path
from . import views

urlpatterns = [
            path('login/', views.login, name='login'),
            path('overview/', views.overview, name='overview'),
            path('shift/', views.shift, name='shift'),
        ]
