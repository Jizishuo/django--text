# Generated by Django 2.0.5 on 2018-06-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0003_musbuy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=20)),
                ('trackid', models.CharField(max_length=20)),
            ],
        ),
    ]
