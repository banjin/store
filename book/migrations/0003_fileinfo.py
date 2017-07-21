# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0002_auto_20170718_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=128)),
                ('file_status', models.SmallIntegerField()),
                ('file_total_size', models.IntegerField()),
                ('file_curl_size', models.IntegerField()),
                ('hash_key', models.CharField(max_length=128)),
                ('file_name_uuid', models.CharField(max_length=64, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
