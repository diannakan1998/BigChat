from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('FriendRequests/', views.FriendRequests.as_view(), name='friendrequests'),
]
