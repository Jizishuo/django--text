# Generated by Django 2.0.7 on 2018-10-24 03:23

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20181023_1509'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='address',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]