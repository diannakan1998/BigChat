from django.db import models
from django.core.validators import EmailValidator

# Create your models here.

class Users(models.Model):
     email = models.CharField( max_length=100, validators=[ EmailValidator() ], blank=False, unique=True)
     user_id = models.CharField(max_length=255, unique=True, blank=False)
     token = models.CharField(max_length=255, unique=True, blank=False)
     chatListId = models.CharField(max_length=255, unique=True, blank=False)

     class Meta:
         db_table = 'Users'


# ChatList Id... needs to be unique
def getChatListModel(db_table):
 class ChatList(models.Model):
     chat_table_name = models.CharField(max_length=100, unique=True)

     class Meta:
         db_table = db_table

 return ChatList



