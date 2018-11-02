from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class FriendRequest(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    friend_requests_emails_sent = ArrayField(models.CharField(max_length=255, unique=True, blank=False), null=True)
    friend_requests_emails_recieved = ArrayField(models.CharField(max_length=255, unique=True, blank=False), null=True)
    class Meta:
        db_table = 'friend_requests'


class chatMember(models.Model):
    member_id =  ArrayField(models.BigIntegerField())
    date_added = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_members"
