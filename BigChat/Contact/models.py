from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Contact(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    friend_id = ArrayField(models.IntegerField())
    date_added = models.TimeField(auto_now= False)
    data_modified = models.TimeField(auto_now= True)

    class Meta:
        db_table = 'contact_list'


