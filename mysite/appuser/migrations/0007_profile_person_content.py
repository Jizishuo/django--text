# Generated by Django 2.0.7 on 2018-08-06 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0006_fans_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='person_content',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
