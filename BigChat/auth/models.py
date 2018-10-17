from django.db import models

# Create your models here.

class Users(models.Model):
    email = models.CharField(max_field=30)

    class Meta:
        db_table = 'Users'



