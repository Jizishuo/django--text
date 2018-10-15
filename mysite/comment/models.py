import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string #render_to_string个参数一个 路径一个传入的内容

#多线程
class Sendmail(threading.Thread):
    #传入参数
    def __init__(self, suject, text, email, fail_silently=False):
        self.suject = suject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        #初始化
        threading.Thread.__init__(self)
    def run(self):
        send_mail(self.suject, "", \
                  settings.EMAIL_HOST_USER, [self.email], \
                  fail_silently=self.fail_silently,\
                  html_message=self.text)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def send_mail(self):
        if self.parent is None:
            #评论
            suject = "有人评论你的 博客"
            #models 也一个方法返回一个email
            email = self.content_object.get_email()
        else:
            #回复
            suject = "有人回复你的 博客"
            email = self.reply_to.email
        if email != "":
            # 反向解析url 得到地址reverse("shahu_detail", args=[comment.content_object.pk])
            # 或者设置models方法
            #text = '%s\n<a href="%s">%s</a>' % (self.text, self.content_object.get_url(), "点击查看")
            #使用模版
            content = {}
            content["comment_text"] = self.text
            content["url"] = self.content_object.get_url()
            text = render_to_string("comment/send_email.html", content)
            # 发送邮件 === 移植到上边多线程
            #send_mail(suject, text, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            #断电测试
            #import pdb
            #pdb.set_trace()
            #命令行exit（）退出 继续执行
            #多线程执行
            send_mail = Sendmail(suject, text, email)
            send_mail.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']

