# Generated by Django 2.0.7 on 2018-08-05 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0004_fans_fans_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fans',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='user_type',
        ),
        migrations.DeleteModel(
            name='Fans',
        ),
        migrations.DeleteModel(
            name='Friends',
        ),
    ]
