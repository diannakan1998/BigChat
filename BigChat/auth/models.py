from django.db import models
from django.core.validators import EmailValidator
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Users(models.Model):
     email = models.CharField( max_length=100, validators=[ EmailValidator() ], blank=False, unique=True)
     user_id = models.AutoField(primary_key=True)
     token = models.CharField(max_length=255, unique=True, blank=False)
     chat_list_id = models.TextField(default="")
     user_name = models.TextField(blank=True)
     profile_img = models.TextField(blank=True, null=True)
     class Meta:
         db_table = 'myAuth_users'


class ChatList(models.Model):
    user_id = models.BigIntegerField()
    chat_id = models.TextField(default="")
    message = models.TextField(default="")
    message_type = models.IntegerField(blank=True)
    flag = models.IntegerField(blank=True)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()
    name = models.TextField()

    class Meta:
        db_table = 'chat_list'

    # return ChatList


 # class chatTable(models.Model):
#      chatId = models.AutoField()
#      memberIds = ArrayField(models.IntegerField(), size=None, null=True)
#      date_added = models.DateTimeField()
#      date_modified = models.DateTimeField()

#      class Meta:
#          db_table = 'chatTable'

# ChatList Id... needs to be unique
