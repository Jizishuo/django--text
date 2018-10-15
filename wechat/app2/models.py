from django.db import models

class UserGroup(models.Model):
    title = models.CharField(max_length=32)


class Userinfomsg(models.Model):
    user_type_chicese = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_chicese)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)

    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role')

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<user: %s>" % self.username


class Usertokenmsg(models.Model):
    user = models.OneToOneField(to='Userinfomsg', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

class Role(models.Model):
    title = models.CharField(max_length=32)
