# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-19 03:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0003_auto_20171119_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 19, 3, 17, 34, 804158)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 19, 3, 17, 34, 805753)),
        ),
    ]
