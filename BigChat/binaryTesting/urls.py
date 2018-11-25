from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mediaMessage/', views.binaryMessages.as_view(), name='binaryMessages'),

]
