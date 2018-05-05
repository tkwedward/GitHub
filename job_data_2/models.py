#coding:utf-8#-*-

from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import datetime
from django.urls import reverse
from .important_list import DISTRICT_LIST, INDUSTRY_LIST, SALARY_TYPE_LIST, SEX_CHOICES, TYPES_CHOICES, OTP_CHOICES, OT_CHOICES

class User(models.Model):
    user_name = models.CharField( max_length=100)
    password = models.CharField(max_length=32)



# Create your models here.
employed_choices = (('yes','在職'), ('no','無業'))

experience_choices=(('0', '請選擇'), ('1','1年或以下'), ('2','2年或以下'), ('3','3年或以下'))


CHOICES = (('1', 'First',), ('2', 'Second',))


class Freelance(models.Model):
    job_name = models.CharField( max_length=100)
    job_location = models.CharField( max_length=100)
    average = models.IntegerField(default=None)
    max_salary = models.IntegerField(default=None)
    min_salary = models.IntegerField(default=None)
    date = models.DateField(default=datetime.today())

    def __unicode__(self):
        return self.job_name

class Job_detail(models.Model):
    time_stamp = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=50)
    jobTitle = models.CharField(max_length=50, default='')
    location2 = models.CharField(max_length=50, blank=True)
    job_type = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=5, default='')
    latest_year = models.FloatField(blank=True, null=True)

    # 薪資
    salary = models.FloatField(blank=True, null=True)

    year = models.FloatField(blank=True, null=True)

    week_total_hour = models.FloatField(blank=True, null=True)

    OT_frequency = models.CharField(max_length=20, default='')

    OT_payment = models.CharField(max_length=50, default='')

    email = models.EmailField( default='')

    date = models.DateField(default=datetime.today())

    contract_week_hour = models.FloatField(blank=True, null=True)

    salary_period = models.CharField(max_length=50, default='')

    account_identify = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.jobTitle
    def __unicode__(self):
        return self.jobTitle
    def get_absolute_url(self):
        return reverse('jobs_gov_data_detail', kwargs={'model_name': 'collected_data','id':self.id})


class collected_data(models.Model):
    time_stamp = models.CharField(max_length=50, blank=True, null=True)

    company = models.CharField(max_length=50)

    jobTitle = models.CharField(max_length=50)

    # 地點
    location2 = models.CharField(max_length=50, blank=True)

    # 工作形態
    job_type = models.CharField(max_length=50, choices=TYPES_CHOICES)

    gender = models.CharField(max_length=5, choices=SEX_CHOICES)

    latest_year = models.FloatField(blank=True, null=True)

    salary = models.FloatField(blank=True, null=True)

    year = models.FloatField(blank=True, null=True)

    week_total_hour = models.FloatField(blank=True, null=True)

    OT_frequency = models.CharField(max_length=20,choices=OT_CHOICES)

    OT_payment = models.CharField(max_length=50, choices=OTP_CHOICES)

    email = models.EmailField(blank=True, null=True)

    date = models.DateField(default=datetime.today())

    contract_week_hour = models.FloatField(blank=True, null=True)

    salary_period = models.CharField(max_length=50)

    account_identify = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.jobTitle
    def __unicode__(self):
        return self.jobTitle
    def get_absolute_url(self):
        return reverse('jobs_gov_data_detail', kwargs={'model_name': 'collected_data','id':self.id})

class labor_gov(models.Model):
    number = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    jobTitle = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    responsibility = models.TextField()

    treatment = models.TextField()

    category = models.CharField(max_length=10, null=True)
    exported = models.BooleanField(default=False)
    money3 = models.CharField(max_length=50, blank=True)
    money = models.FloatField(blank=True, null=True)
    salary_type = models.CharField(max_length=10, blank=True)
    working_date = models.CharField(max_length=50, blank=True)
    location2 = models.CharField(max_length=50, blank=True)

    working_week = models.CharField(max_length=50, blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    working_hours_number = models.CharField(max_length=50, blank=True)
    working_day_number= models.CharField(max_length=50, blank=True)
    working_shift = models.CharField(max_length=50, blank=True)
    working_hours_number_float = models.FloatField(blank=True, null=True)
    working_day_number_float= models.FloatField(blank=True, null=True)

    start_time = models.TextField()

    end_time = models.TextField()

    week_total_hour = models.TextField()

    def __str__(self):
        return self.jobTitle
    def __unicode__(self):
        return self.jobTitle

    def get_absolute_url(self):
        return reverse('jobs_gov_data_detail', kwargs={'model_name': 'labor_gov','id':self.id})
