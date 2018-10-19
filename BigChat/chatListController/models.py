from django.db import models
from django.core.validators import EmailValidator

# Create your models here.

# ChatList Id... needs to be unique
def getChatListModel(db_table):
 class ChatList(models.Model):
     chat_table_name = models.CharField(max_length=100, unique=True)

     class Meta:
         db_table = db_table

 return ChatList


def getMessageHistoryModel(db_table):
 class Messages(models.Model):
     email = models.CharField( max_length=100)
     message = models.CharField(max_length=255)

     class Meta:
         db_table = db_table

 return Messages


