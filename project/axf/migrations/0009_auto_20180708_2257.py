# Generated by Django 2.0.5 on 2018-07-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0008_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=20)),
                ('userid', models.CharField(max_length=20)),
                ('progress', models.IntegerField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='cart',
            managers=[
            ],
        ),
    ]
