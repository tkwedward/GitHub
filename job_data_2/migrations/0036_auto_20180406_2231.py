# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-06 22:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0035_auto_20180401_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_detail',
            name='salary_type',
            field=models.CharField(blank='True', choices=[('', '\u652f\u85aa\u5468\u671f'), ('month', '\u6708\u85aa'), ('half-month', '\u534a\u6708\u85aa'), ('week', '\u9031\u85aa'), ('day', '\u65e5\u85aa'), ('hour', '\u6642\u85aa'), ('item', '\u4ef6\u85aa')], default='1', max_length=10),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='sex',
            field=models.CharField(blank=True, choices=[('', '\u6027\u5225'), ('male', '\u7537'), ('female', '\u5973'), ('other', '\u5176\u4ed6')], default='male', max_length=100),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='types',
            field=models.CharField(blank=True, choices=[('', '\u8077\u52d9\u578b\u614b'), ('full_time', '\u5168\u8077'), ('part_time', '\u517c\u8077(\u542b\u6253\u5de5)'), ('interm', '\u5be6\u7fd2'), ('temporary', '\u81e8\u6642\u5de5'), ('contract', '\u7d04\u8058\u96c7'), ('deliver', '\u6d3e\u9063')], default='full_time', max_length=100),
        ),
    ]