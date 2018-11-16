from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class media(models.Model):
    user_id = models.BigIntegerField()
    mediab = models.BinaryField()
    message_type = models.IntegerField()

    class Meta:
        db_table = "mediaTesting"
