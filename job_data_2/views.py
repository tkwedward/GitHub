#coding:utf-8#-*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm, FreelanceForm, Search_Bar_Form
from .models import Job_detail, labor_gov, collected_data
from django.db.models import Count, Avg, Max, Min
import math
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.template.loader import render_to_string
import json
from itertools import chain
import re, datetime
import numpy as np
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict
# 製造頁面
from itertools import chain


collected_data_model = collected_data.objects.all()
labor_gov_model = labor_gov.objects.exclude(working_hours_number=None).exclude(working_hours_number='').exclude(week_total_hour=0.0)
# labor_gov_model = labor_gov.objects.all()
    # 第一頁
def homepage(request):
    form = ContactForm(
        initial={
        'company': '世紀帝國',
        'industry':'商用服務業',
        # 職位名稱
        'jobTitle':'巨投',
        # 工作地點
        'place':'東區',
        # 職務型態
        'job_type':'全職',
        #工作天數
        'date_number':'10',
        # 性別
        'gender':'f',
        # 你最近從事這份工作的年份
        'latest_year':2015,
        # 支薪周期
        'salary':'1',
        'salary_period':'月薪',
        # 行業年資
        'year':9000,
        # 合約列明一周工時
        'contract_hour':10,
        # 每周工時
        'week_total_hour':10,

        # 超時
        'OT_payment':'絕少',

        # 加班補償
        'OT_frequency': '有',

        # week_total_hour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '一周實際工時'}))

        })
    form2 = Search_Bar_Form()
    # user = request.user
    # user_id = user.social_auth.get(provider='facebook').uid
    user = ""
    user_id=""
    return render(request, 'WKnews_web_draft 3_1.htm', {'form': form, 'form2':form2, 'type':'normal'})

def about_us(request):
    return render(request, 'about_us.htm', {})

def get_name_2(request):
    form = FreelanceForm()
    return render(request, 'name.html', {'form': form, 'type2':'freelance'})

    #第二頁

def Freelance_add(request):
    if request.method == "POST":
        form = FreelanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = FreelanceForm()
    return render(request, 'freelance_form.html', {'form': form})

#功能
"""
type 是從 salary 或 working_hour 二選一
field1是放入由ajax 傳送過來的form中其中的field value，如果是 type 是 salary，這裏的field value會是工時，否則就是none
"""
category_model=None

def statistic(type, field1, data_list, model=None, form=None, step=None):
    # 這裏的field1 是薪金形態
    if type == 'salary':
        model_used = model.filter(salary_type=form['salary_period'])
    model_used = model.filter(salary_type='月薪')
    # 這裏的field1是 money或是 week_total_hour
    avg =model_used.aggregate(average=Avg(field1))
    max_list = model_used.aggregate(maximum=Max(field1))
    mini_list = model_used.aggregate(minimum=Min(field1))

    # 這裏是想取回這個例子的instance，例如清潔工的工作時間和人工是多少
    instance_data = float(form[type])

    # 這兩個是用來計算graph中x-axis的最小和最大值
    range_min = int(math.floor(float(mini_list['minimum'])))
    range_max = int(math.ceil(float(max_list['maximum'])))

    global combine_length
    global combine_number
    combine_length = 0
    combine_number = set()
    max_bar = 13
    # the following is for data generation
    for counter ,x in enumerate(range(range_min, range_max, step)):
        if instance_data>=x-step and instance_data<x+step:
            color = 'RGB(247,147,30)'
        else:
            color = 'RGB(252, 238, 33)'
        # print(x, color)
        if type == 'salary':
            if counter > max_bar:
                combine_number.add(math.floor(x/1000))
                combine_number.add(math.floor((x+step)/1000))
                sorted(combine_number, key=float)
                combine_length+= len(model.filter(money__gte=float(x-step)).filter(money__lt=float(x+step)))
            else:
                length = len(model.filter(money__gte=float(x-step)).filter(money__lt=float(x+step)))
                data_list.append({'range':'{}-{}'.format(math.floor(x/1000), math.floor((x+step)/1000)), 'number':length, 'color':color})
        else:
            length = len(model.filter(week_total_hour__gte=float(x-step)).filter(week_total_hour__lt=float(x+step)))
            data_list.append({'range':'{}-{}'.format(x, x+step), 'number':length, 'color':color})

    if type == 'salary' and len(data_list)>max_bar:
        last_item = '{}以上'.format(min(combine_number))
        print(last_item, combine_length)
        data_list.append({'range':last_item, 'number':combine_length, 'color':color})
        # print({'range':'{}-{}'.format(x, x+step), 'number':length, 'color':color})
        # salary_classification.append({'range':'{}-{}'.format(x, x+5000), 'number':length, 'color':color})
        # print({'range':'{}-{}'.format(x, x+step), 'number':length, 'color':color})

    return data_list
    # 返回 instance 的資料, 使用了的model，最小值和最大值



@require_POST
def added(request):
    form = request.POST.dict()
    category_model = labor_gov_model.filter(industry=form['industry'])

    """傳送的data︰
    時間︰min, max, average
    組別︰category
    """
    salary_classification = []
    salary_step = None
    salary_start_value = None
    salary_color=None
    hour_classification = []
    hour_step = 5
    hour_start_value = 0
    hour_color=None

    if (form['salary_period']=='月薪'):
        salary_step = 2000
    elif (form['salary_period']=='日薪'):
        salary_step = 50
    elif (form['salary_period']=='時薪'):
        salary_step = 10

    # money
    salary_classification = json.dumps(statistic(type='salary', field1='money', data_list=salary_classification, model=category_model, form=form, step=salary_step))

    # working hour
    hour_classification = json.dumps(statistic(type='week_total_hour', field1='week_total_hour', data_list=hour_classification, model=category_model, form=form, step=hour_step))
    # print(hour_classification)
    # print(salary_classification)

    return JsonResponse({
        'form': form,
        'hour_classification':hour_classification,
        'salary_classification':salary_classification,
        'category': form['industry']}
        )

def success(request):
    return HttpResponse('success')

def jobs_gov_data_detail(request, model_name, id):
    if model_name == 'collected_data':
        instance = get_object_or_404(collected_data, id=id)
        average = None
        maximum = None
        minimum = None
        classification = None
        json_classification =None
    else:
        instance = get_object_or_404(labor_gov, id=id)

        category_model = labor_gov_model.filter(category=instance.category)
    #
        average = category_model.aggregate(average=Avg('week_total_hour'))
        maximum = category_model.aggregate(maximum=Max('week_total_hour'))
        minimum = category_model.aggregate(minimum=Min('week_total_hour'))

        model = labor_gov.objects.all()

        """傳送的data︰
        時間︰min, max, average
        組別︰category
        """
        range_min = int(math.floor(float(minimum['minimum'])))
        range_max = int(math.ceil(float(maximum['maximum'])))
        classification = []

        step = 5
        instance_hour = float(instance.week_total_hour)
        for x in range(1, range_max, step):
            if instance_hour>=x-1 and instance_hour<x+4:
                color = 'RGB(247,147,30)'
            else:
                color = 'RGB(252, 238, 33)'

            length = len(category_model.filter(week_total_hour__gte=float(x-1)).filter(week_total_hour__lt=float(x+4)))
            classification.append({'range':'{}-{}'.format(x-1, x+4), 'number':length, 'color':color})

            json_classification = json.dumps(classification)

    return render(request, 'analysis.html', {'instance': instance, 'average':average, 'maximum':maximum, 'minimum':minimum, 'classification':classification, 'json_classification':json_classification, 'model':model_name, 'category': instance.category})



# 用來在 search function 之中，找出想要display 出來的data list
def get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by="", data_list_sort_by="", data_list=labor_gov_model):
    print('I am using get_data_list')
    if position:
        data_list = data_list.filter(jobTitle__contains=position)
    if industry and industry!='all':
        data_list = data_list.filter(industry=industry)
    if location and location!='all':
        data_list = data_list.filter(location2=location)
    if salary_type:
        data_list = data_list.filter(salary_type=salary_type)
    if upper_limit and lower_limit:
        data_list = data_list.filter(money__gte=lower_limit).filter(money__lte=upper_limit)

    data_list_order_by = "" if data_list_order_by is None else data_list_order_by

    data_list_sort_by = "" if data_list_sort_by is None else data_list_sort_by

    result = data_list_order_by + data_list_sort_by

    if result =="":
        pass
    else:
        data_list=data_list.order_by(result)
    return data_list

def get_data_from_the_url(request):
    print('I am using get_data_from_the_url')
    position = request.GET.get('keyword')
    print('here is the position: {}'.format(position))
    industry = request.GET.get('industry')
    location = request.GET.get('location')
    upper_limit = request.GET.get('upper_limit')
    lower_limit = request.GET.get('lower_limit')
    salary_type = request.GET.get('salary_type')
    data_list_order_by = request.GET.get('order')
    data_list_sort_by = request.GET.get('type')
    page = request.GET.get('page')
    print(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)
    return position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by

def get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by):
    paginator_link = "keyword={}&industry={}&location={}&salary_type={}&upper_limit={}&lower_limit={}&data_list_order_by={}&data_list_sort_by={}".format(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)
    return paginator_link

def get_Paginator(data_list, request):
    paginator = Paginator(data_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')

    if page is None:
        page = 1
    if paginator.num_pages < 11:
        number_page_show = paginator.num_pages
    else:
        number_page_show = 11
    if int(page)-5 >0 :
        show_page_list = [int(page)+x-5 for x in range(number_page_show)]
    else:
        show_page_list = [1+x for x in range(number_page_show)]
    try:
        data_show = paginator.page(page)
    except PageNotAnInteger:
        data_show = paginator.page(1)
    except EmptyPage:
        data_show = paginator.page(paginator.num_pages)
    return data_show, show_page_list


def jobs_gov_data(request):
    data_list = labor_gov.objects.exclude(week_total_hour=0.0)

    data_show, show_page_list = get_Paginator(data_list, request)

    search_form = Search_Bar_Form()

    position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by = get_data_from_the_url(request)

    paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

    return render(request, 'search_page.htm', {'list': data_show, 'form': search_form, 'paginator_link':paginator_link, #'category_list':CATEGORY_CHOICES,
    'show_page_list':show_page_list})



def get_search(request, position="", industry="", location="", salary="", salary_type="", salary_filter="", data_list_order_by="", data_list_sort_by=""):

    data_list = []
    if request.is_ajax():
        print('I am using get_search_ajax')
        position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by = get_data_from_the_url(request)
        # symbol = request.GET.get('symbol')

        data_list = get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by)
        """paginator"""
        data_show, show_page_list = get_Paginator(data_list, request)

        paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

        # print (request.GET)
        # print(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, symbol)
        html = render_to_string('data_table.html', {'list': data_show, 'show_page_list':show_page_list, 'paginator_link':paginator_link})
        # print(html)

        return HttpResponse(json.dumps({'html':html}), content_type='application/json')
        # return render(request, 'search_page.htm', {})
    else:
        print('-------------------')
        print('I am using get_search function and not ajax')
        print('-------------------')
        search_form = Search_Bar_Form(request.GET)
        position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by = get_data_from_the_url(request)
        # symbol = request.GET.get('symbol')
        # data_get_list = [position, industry, location, upper_limit, lower_limit, salary_type]

        paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

        data_list = get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by)

        """paginator"""
        data_show, show_page_list = get_Paginator(data_list, request)
        # print(data_show, show_page_list, data_list)
        return render(request, 'search_page.htm', {'list': data_show, 'form':search_form, 'paginator_link':paginator_link, 'show_page_list':show_page_list})

def add_json_data(request):
    name_cat = u'生產/工廠職位'

    data = json.load(open('/Users/mac/Desktop/projects/selenium/生產.txt'))

    for x in data:
        try:
            labor_gov.objects.create(
            number=x['number'],
            company=x['company'],
            location=x['location'],
            treatment= x['treatment'],
            date=x['date'],
            responsibility=x['responsibility'],
            industry=x['industry'],
            jobTitle=x['jobTitle'],
            category= name_cat,
            week_total_hour=0
            )
        except:
            print (x)
    return HttpResponse('ok')
