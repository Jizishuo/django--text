from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

#分类
class ShahuType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
#地点
class Location(models.Model):
    Location = models.CharField(max_length=15)

    def __str__(self):
        return self.Location

class Shahu(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    shahu_type = models.ForeignKey(ShahuType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<shahu: %s>" % self.title

    #获取具体傻乎连接
    def get_url(self):
        return reverse("shahu_detail", kwargs={"shahu_pk": self.pk})

    #获取具体傻乎email
    def get_email(self):
        return self.author.email

    class Meta:
        ordering = ['-created_time']
