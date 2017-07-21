# coding:utf-8

from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

    def __unicode__(self):
        return self.name
    

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class FileInfo(models.Model):
    """文件信息"""

    # 上传时间
    upload_time = models.DateTimeField(auto_now_add=True)
    # 最后修改事件
    # last_modify_time = models.DateTimeField(auto_now=True)
    # work_table = models.ForeignKey(WorkTable, null=True)
    # 需要使用
    file_name = models.CharField(max_length=128)
    # 上传状态 1.等待上传 2.正在上传 3.上传完成
    file_status = models.SmallIntegerField()
    # 文件总的大小
    file_total_size = models.IntegerField()
    # 文件上传当前大小
    file_curl_size = models.IntegerField()
    user = models.ForeignKey(User)
    hash_key = models.CharField(max_length=128)
    file_name_uuid = models.CharField(max_length=64, null=True)