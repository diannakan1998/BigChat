from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('MessageHistory/', views.MessageHistory.as_view(), name='messageHistory'),
	path('chatlist/', views.chatlist.as_view(), name='chatlist'),
]