# Generated by Django 2.1.2 on 2018-10-21 22:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('email', models.CharField(max_length=100, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('chat_list_id', models.TextField(blank=True, default='')),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]
