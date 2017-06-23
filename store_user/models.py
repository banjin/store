from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=11, null=True)

    class Meta:
        db_table = 'company'


class UserInfo(models.Model):

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11, null=True)
    company = models.ForeignKey(Company, null=True)

    class Meta:
        db_table = 'user_info'



