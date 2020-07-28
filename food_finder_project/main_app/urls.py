from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('volunteer', views.volunteer),
    path('login', views.login),
    path('registration', views.registration),
    path('profile', views.profile),
]