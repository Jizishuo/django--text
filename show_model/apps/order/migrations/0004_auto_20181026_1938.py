# Generated by Django 2.0.7 on 2018-10-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20181026_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='transit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='运费'),
        ),
    ]
