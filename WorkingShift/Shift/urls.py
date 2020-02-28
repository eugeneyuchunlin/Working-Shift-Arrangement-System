from django.urls import path
from . import views

urlpatterns = [
            path('index/', views.loginPage, name='index'),
            path('login/', views.login, name='login'),
            path('overview/', views.overview, name='overview'),
            path('shift/', views.shift, name='shift'),
            path('saveshift/', views.shift, name='saveshift'),
            path('postshift/', views.postShift, name='postshift'),
        ]
