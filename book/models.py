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

    class AppInfo(models.Model):
        """
        流量监控,统计每个协议的流量
        """
        # 设备编号，在探针系统的界面上可以找到，位置：系统维护 -》设备编号
        devid = models.IntegerField(null=True)
        # 协议编号，可以在下面的palog.config表中查询
        apid = models.IntegerField(null=True)
        # 这条记录采集的时间，探针的时间
        time = models.BigIntegerField(null=True)
        # 记录采集的间隔
        inter = models.IntegerField(null=True)
        # 协议的连接数
        app_flowcont = models.IntegerField(null=True)
        # 上行流量
        app_upbytes = models.BigIntegerField(null=True)
        # 下行流量
        app_downbytes = models.BigIntegerField(null=True)
        # 链路的编号，分0，1，2，3，4，5，6，7，8，9其中0是监控模式，1-4为网桥，6-9为虚拟链路
        linkid = models.IntegerField(null=True)

        class Meta:
            db_table = 'app_info'


    













