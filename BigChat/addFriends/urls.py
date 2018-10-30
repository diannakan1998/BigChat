from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addFriend/', views.addFriends.as_view(), name='addFriend'),
]