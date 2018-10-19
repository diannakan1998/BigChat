from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authenticate/', views.Authenticate.as_view(), name='authenticate'),
    path('updateToken/', views.updateUserToken.as_view(), name='updateUserToken'),

]