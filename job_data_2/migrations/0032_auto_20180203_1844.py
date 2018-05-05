# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-03 18:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0031_auto_20180203_1839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collected_data',
            old_name='week_hour',
            new_name='week_total_hour',
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 2, 3, 18, 44, 3, 473689)),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 2, 3, 18, 44, 3, 471293)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 2, 3, 18, 44, 3, 472469)),
        ),
    ]