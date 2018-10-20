from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

def chatModel(chatId):
    class chat(models.Model):
        # user_id = models.IntegerField()
        # user_name = models.CharField()
        user_email = models.CharField()
        message = models.CharField()
        media = ArrayField(models.BinaryField())
        message_type = models.IntegerField()
        date_added = models.TimeField()
        data_modified = models.TimeField()

        class Meta:
            db_table = chatId
    
    return chat

