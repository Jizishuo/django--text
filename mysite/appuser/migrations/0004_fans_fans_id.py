# Generated by Django 2.0.7 on 2018-08-02 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0003_friends_friend_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='fans',
            name='fans_id',
            field=models.IntegerField(default=1),
        ),
    ]