from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Contacts/', views.Contacts.as_view(), name='contact'),
    path('Profile/', views.profile.as_view(), name='profile'),
]