# Generated by Django 2.0.7 on 2018-08-02 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fans', models.CharField(blank=True, max_length=30, null=True)),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.CharField(blank=True, max_length=30, null=True)),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.Profile')),
            ],
        ),
    ]