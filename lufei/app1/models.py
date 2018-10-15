from django.db import models

#课程表
class Course(models.Model):
    title = models.CharField(verbose_name='课程名称', max_length=32)
    course_img = models.CharField(verbose_name='课程图片', max_length=64)
    level_chioces = (
        (1, '初级'),
        (2, '中级'),
        (3, '高级'),
    )
    level = models.IntegerField(verbose_name='课程难度',choices=level_chioces, default=1)

    def __str__(self):
        return self.title

#课程详细表
class CourseDetail(models.Model):
    course = models.OneToOneField(to='Course', on_delete=models.CASCADE)
    why_study = models.CharField(verbose_name='为啥要学', max_length=255)
    course_slogan = models.CharField(verbose_name='口号', max_length=255)
    #prerequisite = models.ManyToManyField(verbose_name='必备技能', to='Course')
    recommend_course = models.ManyToManyField(verbose_name='推荐课程', to='Course', related_name='rc')

    def __str__(self):
        return "课程详细" + self.course.title


#章节
class Chapter(models.Model):
    num = models.IntegerField(verbose_name='章节')
    chapter_name = models.CharField(verbose_name='章节名称', max_length=32)
    course = models.ForeignKey(verbose_name='所属课程', to='Course', on_delete=models.CASCADE)

    def __str__(self):
        return "第%s章" % self.num


#用户
class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)

    def __str__(self):
        return self.user

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)



