from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class chat(models.Model):
    chat_id = models.CharField(max_length=255)
    user_id = models.BigIntegerField()
    user_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    message = models.TextField()
    media = models.TextField()
    # mediab = ArrayField(models.BinaryField())
    message_type = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat"


