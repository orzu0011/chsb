# Generated by Django 5.1.6 on 2025-03-26 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
    ]
