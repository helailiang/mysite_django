from django.db import models

# Create your models here.

class User(models.Model):
    #第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容
    gender=(
        ('man','男'),
        ('woman','女'),
    )
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False) #是否进行过邮件确认的属性
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'db_user'
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户1'

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User')
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name+':'+self.code
    class Meta:
        db_table = 'db_confirmstring'
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'