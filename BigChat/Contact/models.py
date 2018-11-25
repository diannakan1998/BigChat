from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.



class Contact(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    friend_id = ArrayField(models.BigIntegerField(unique=True, blank=False), null=True)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contact_list'

class Profile(models.Model):
    email = models.CharField(max_length=255, unique=True)
    name = models.TextField(blank=True, null=True)
    profile_img = models.BinaryField(blank=True, null=True)
    profile_description = models.TextField(blank=True, null=True)
    profile_img_str = models.TextField(null=True)

    class Meta:
        db_table = 'profiles'

