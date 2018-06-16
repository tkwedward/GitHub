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
        'company': '搵你笨保險有限公司',
        'industry':'政府部門',
        # 職位名稱
        'jobTitle':'保險推銷員',
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
        'salary_period':'月薪',
        'salary':'10000',
        # 行業年資
        'year':9,
        # 合約列明一周工時
        'contract_hour':40,
        # 每周工時
        'week_total_hour':40,

        # 超時
        'OT_payment':u'有',

        # 加班補償
        'OT_frequency': u'絕少',

        # week_total_hour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '一周實際工時'}))

        }
        )
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
    # avg =model_used.aggregate(average=Avg(field1))
    max_list = model_used.aggregate(maximum=Max(field1))
    mini_list = model_used.aggregate(minimum=Min(field1))
    print('max_list:{}, mini_list:{}'.format(max_list, mini_list))
    # 這裏是想取回這個例子的instance，例如清潔工的工作時間和人工是多少
    instance_data = float(form[type])

    # 這兩個是用來計算graph中x-axis的最小和最大值
    try:
        range_min = int(math.floor(float(mini_list['minimum'])))
    except Exception as e:
        print(e)
        range_min=0
    try:
        range_max = int(math.ceil(float(max_list['maximum'])))
    except Exception as e:
        print(e)
        range_max=50
    global combine_length
    global combine_number
    combine_length = 0
    combine_number = set()
    max_bar = 13
    # the following is for data generation
    print('step', 'x', 'x+step', 'instance_data', 'color')
    # step=10
    for counter ,x in enumerate(range(0, range_max, step)):
        if instance_data>=float(x) and instance_data<float(x+step):
            color = 'RGB(247,147,30)'
        else:
            color = 'RGB(252, 238, 33)'
        print(step, float(x), float(x+step), instance_data, color)
        if type == 'salary':
            if counter > max_bar:
                combine_number.add(math.floor(x/1000))
                combine_number.add(math.floor((x+step)/1000))
                sorted(combine_number, key=float)
                combine_length+= len(model.filter(money__gte=float(x)).filter(money__lt=float(x+step)))
            else:
                length = len(model.filter(money__gte=float(x)).filter(money__lt=float(x+step)))
                data_list.append({'range':'{}-{}'.format(math.floor(x/1000), math.floor((x+step)/1000)), 'number':length, 'color':color})
        else:
            length = len(model.filter(week_total_hour__gte=float(x-step)).filter(week_total_hour__lt=float(x+step)))
            data_list.append({'range':'{}-{}'.format(x, x+step), 'number':length, 'color':color})
    print(type, data_list, max_bar, combine_number)

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
    print(form)
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

    if (form['salary_period']==u'月薪'):
        salary_step = 2000
    elif (form['salary_period']==u'日薪'):
        salary_step = 50
    elif (form['salary_period']==u'時薪'):
        salary_step = 10
    print(salary_step)
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
        salary_classification = []
        salary_step = 2000
        salary_start_value = None
        salary_color=None
        hour_classification = []
        hour_step = 5
        hour_start_value = 0
        hour_color=None
        form = {
            'company': instance.company,
            'industry': instance.industry,
            'jobTitle':instance.jobTitle,
            'place': instance.location2,
            'salary_period': instance.salary_type,
            'date_number': instance.working_day_number,
            'week_total_hour': instance.week_total_hour,
            'salary': instance.money,
        }


        category_model = labor_gov_model.filter(category=instance.category)

        # money
        salary_classification = json.dumps(statistic(type='salary', field1='money', data_list=salary_classification, model=category_model, form=form, step=salary_step))

        # working hour
        hour_classification = json.dumps(statistic(type='week_total_hour', field1='week_total_hour', data_list=hour_classification, model=category_model, form=form, step=hour_step))
        # print(hour_classification)
        # print(salary_classification)

        result_file = {
            'hour_classification':hour_classification,
            'salary_classification':salary_classification,
            'category': form['industry']
            }

        json_file = json.dumps(result_file)
        # json_file = json.dumps(result_file).replace("\\","").replace("\"[","[").replace("]\"","]")
        print(json_file)






    return render(request, 'analysis.html', {'form': form,
    'hour_classification':hour_classification,
    'salary_classification':salary_classification,
    'category': form['industry'], 'json':json_file})



    #
    # return render(request, 'analysis.html', {'instance': instance, 'average':average, 'maximum':maximum, 'minimum':minimum, 'classification':classification, 'json_classification':json_classification, 'model':model_name, 'category': instance.category})



# 用來在 search function 之中，找出想要display 出來的data list
def get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by="", data_list_sort_by="", data_list=labor_gov_model):
    print('I am using get_data_list')
    if position:
        print('filter by {}'.format(position))
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
    industry = request.GET.get('industry')
    location = request.GET.get('location')
    upper_limit = request.GET.get('upper_limit')
    lower_limit = request.GET.get('lower_limit')
    salary_type = request.GET.get('salary_type')
    data_list_order_by = request.GET.get('order')
    data_list_sort_by = request.GET.get('type')
    page = request.GET.get('page', 1)
    print(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page)
    return position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page

def get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by):
    paginator_link = "keyword={}&industry={}&location={}&salary_type={}&upper_limit={}&lower_limit={}&data_list_order_by={}&data_list_sort_by={}".format(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)
    return paginator_link

def get_Paginator(data_list, request, page_from_link=None):
    paginator = Paginator(data_list, 10) # Show 25 contacts per page
    page = page_from_link

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
    search_form = Search_Bar_Form()

    position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page = get_data_from_the_url(request)

    paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

    data_list = labor_gov.objects.exclude(week_total_hour=0.0)

    data_show, show_page_list = get_Paginator(data_list, request, page)



    return render(request, 'search_page.htm', {'list': data_show, 'form': search_form, 'paginator_link':paginator_link, #'category_list':CATEGORY_CHOICES,
    'show_page_list':show_page_list})



def get_search(request, position="", industry="", location="", salary="", salary_type="", salary_filter="", data_list_order_by="", data_list_sort_by="", page_from_link=1):

    data_list = []
    if request.is_ajax():
        print(request.GET.get('keyword'))
        print('I am using ajax')
        position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page = get_data_from_the_url(request)
        # symbol = request.GET.get('symbol')
        print(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page)

        paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)
        print(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by)


        data_list = get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by)

        """paginator"""
        data_show, show_page_list = get_Paginator(data_list, request, page)



        # print (request.GET)
        # print(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, symbol)
        html = render_to_string('data_table.html', {'list': data_show, 'show_page_list':show_page_list, 'paginator_link':paginator_link})
        # print(html)
        return JsonResponse({'html':html})
        # return HttpResponse(json.dumps({'html':html}), content_type='application/json')
        # return render(request, 'search_page.htm', {})
    else:
        print('-------------------')
        print('I am using get_search function and not ajax')
        print('-------------------')
        search_form = Search_Bar_Form(request.GET)
        position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page = get_data_from_the_url(request)
        # symbol = request.GET.get('symbol')
        # data_get_list = [position, industry, location, upper_limit, lower_limit, salary_type]

        paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

        data_list = get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by)

        """paginator"""
        data_show, show_page_list = get_Paginator(data_list, request, page_from_link)
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
