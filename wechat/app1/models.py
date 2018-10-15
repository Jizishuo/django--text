from django.db import models
from django.contrib.auth.models import User


class Show(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)

    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<show: %s>" % self.title

class Userinfo(models.Model):
    user_type_chicese = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_chicese)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)

    #group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<user: %s>" % self.username

class Usertoken(models.Model):
    user = models.OneToOneField(to='Userinfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
