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
    path('zipsearch', views.zipsearch),
    path('donate', views.donate2),
    path('donate2', views.donate),
    path('charge', views.charge),
    path('thank_you/<int:donator_id>', views.thank_you),
    path('delete_db', views.delete_db),
    path('backup', views.backup),
]