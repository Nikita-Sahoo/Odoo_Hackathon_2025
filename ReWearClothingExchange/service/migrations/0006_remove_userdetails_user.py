# Generated by Django 4.1 on 2025-07-12 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_userdetails_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='user',
        ),
    ]
