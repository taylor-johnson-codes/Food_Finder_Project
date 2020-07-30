from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('volunteer', views.volunteer),
    path('login', views.login),
    path('process_login', views.process_login),
    path('registration', views.registration),
    path('register', views.register),
    path('profile', views.profile),
    path('change_picture', views.change_picture),
    path('edit_profile', views.edit_profile),
    path('update_profile', views.update_profile),
    path('delete', views.delete),
    path('logout', views.logout),
    path('search', views.search),
    path('donate', views.donate),
]