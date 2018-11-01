from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import EmailValidator

# Create your models here.

class FriendRequests(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    friend_requests_emails_sent = ArrayField(models.CharField(max_length=255, validators=[ EmailValidator() ], unique=True, blank=False))
    friend_requests_emails_recieved = ArrayField(models.CharField(max_length=255, validators=[ EmailValidator() ], unique=True, blank=False))
    class Meta:
        db_table = 'friend_requests'
