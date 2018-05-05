#coding:utf-8#-*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm, FreelanceForm, Search_Bar_Form
from .models import Job_detail, labor_gov, collected_data
from django.db.models import Count, Avg, Max, Min
import math
from django.contrib.auth.models import User
from django.templatetags.static import static
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

        #
        # week_total_hour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '一周實際工時'}))

        })
    form2 = Search_Bar_Form()
    # user = request.user
    # user_id = user.social_auth.get(provider='facebook').uid
    user = ""
    user_id=""
    return render(request, 'WKnews_web_draft 3_1.htm', {'form': form, 'form2':form2, 'type':'normal'})
    # return render(request, 'name.html', {'form': form, 'form2':form2, 'type':'normal', 'user':user, 'user_id':user_id})

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

@require_POST
def added(request):
    form = ContactForm(request.POST)

    if form.is_valid():
        print(form.cleaned_data['week_total_hour'])
        # category_model = labor_gov_model.filter(category=form.cleaned_data['industry'])
        category_model = labor_gov_model.filter(industry='商用服務業')
        print(category_model)
    #
        average = category_model.aggregate(average=Avg('week_total_hour'))
        maximum = category_model.aggregate(maximum=Max('week_total_hour'))
        minimum = category_model.aggregate(minimum=Min('week_total_hour'))
        print(minimum)
        model = labor_gov.objects.all()

        """傳送的data︰
        時間︰min, max, average
        組別︰category
        """
        range_min = int(math.floor(float(minimum['minimum'])))
        range_max = int(math.ceil(float(maximum['maximum'])))
        classification = []
        # print len(category_model)


        step = 5
        instance_hour = float(form.cleaned_data['week_total_hour'])
        for x in range(1, range_max, step):
            if instance_hour>=x-1 and instance_hour<x+4:
                color = 'RGB(247,147,30)'
            else:
                color = 'RGB(252, 238, 33)'

            length = len(category_model.filter(week_total_hour__gte=float(x-1)).filter(week_total_hour__lt=float(x+4)))
            classification.append({'range':'{}-{}'.format(x-1, x+4), 'number':length, 'color':color})

            json_classification = json.dumps(classification)
            # print json_classification

        return render(request, 'analysis.html', {'form': form.cleaned_data, 'json_classification':json_classification, 'category': form.cleaned_data['industry']})
        # {'instance': instance, 'average':average, 'maximum':maximum, 'minimum':minimum, 'classification':classification, 'json_classification':json_classification, 'model':model_name, 'category': instance.category})

    else:
        print(form.errors)

    return render(request, 'name.html', {'form': form})

def success(request):
    return HttpResponse('success')

def jobs_gov_data(request):
    categories_list = labor_gov_model.values_list('category').distinct()
    CATEGORY_CHOICES = list()
    for x in categories_list:
        CATEGORY_CHOICES.append(x[0])

    data_list = labor_gov.objects.exclude(week_total_hour=0.0)

    order_desired =  request.get_full_path().split('/')[-1]
    print(order_desired)
    if order_desired == 'work-time-dashboard':
        data_list = labor_gov.objects.all().order_by('-week_total_hour').exclude(week_total_hour=0.0)
        # data_list.order_by('-week_total_hour')
    elif order_desired == 'salary-dashboard':
        data_list = labor_gov.objects.all().order_by('-money').exclude(week_total_hour=0.0)



    # data_list = labor_gov.objects.all()

    """paginator"""
    paginator = Paginator(data_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')

    if page is None:
        page = 1

    if int(page)-5 >0 :
        show_page_list = [int(page)+x-5 for x in range(11)]
        print (show_page_list)
    else:
        show_page_list = [1+x for x in range(11)]



    try:
        data_show = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_show = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_show = paginator.page(paginator.num_pages)

    search_form = Search_Bar_Form()

# bookmark
    # return render(request, 'gov_jobs_detial.html', {'list': data_show})

    return render(request, 'search_page.htm', {'list': data_show, 'form': search_form, 'category_list':CATEGORY_CHOICES, 'show_page_list':show_page_list})
    # return render(request, 'list_view2.html', {'list': data_show, 'form': search_form, 'category_list':CATEGORY_CHOICES, 'show_page_list':show_page_list})

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
        # print len(category_model)


        step = 5
        instance_hour = float(instance.week_total_hour)
        for x in range(1, range_max, step):
            if instance_hour>=x-1 and instance_hour<x+4:
                color = 'RGB(247,147,30)'
            else:
                color = 'RGB(252, 238, 33)'

            length = len(category_model.filter(week_total_hour__gte=float(x-1)).filter(week_total_hour__lt=float(x+4)))
            classification.append({'range':'{}-{}'.format(x-1, x+4), 'number':length, 'color':color})
            # print classification


            # print ('{}-{}小時的case有{}個'.format(x-1, x+4, length))
            # print classification
            # print (float(x), float(x+4))

            # print classification
            json_classification = json.dumps(classification)
            # print json_classification


    return render(request, 'overlay.html', {'instance': instance, 'average':average, 'maximum':maximum, 'minimum':minimum, 'classification':classification, 'json_classification':json_classification, 'model':model_name, 'category': instance.category})
    # return render(request, '內頁.html', {'instance': instance, 'average':average, 'maximum':maximum, 'minimum':minimum, 'classification':classification, 'json_classification':json_classification, 'model':model_name, 'category': instance.category})


# @login_required
# @require_POST
def ajax_order(request):
    position = request.POST.get('position')
    industry = request.POST.get('industry')
    location = request.POST.get('location')
    salary = request.POST.get('salary')
    salary_type = request.POST.get('salary_type')
    action = request.POST.get('action')
    action_id = request.POST.get('id')

    # print(action, action_id)
    # print (position, industry, location, salary, salary_type)
    # print (salary_type)
    data_list = labor_gov_model.order_by('location2')[0:20]
    if position:
         data_list.filter(jobTitle__contains=position)
    if industry and industry!='all':
        data_list = data_list.filter(industry=industry)
    if location and location!='all':
        data_list = data_list.filter(location2=location)
    if salary_type:
        data_list.filter(salary_type=salary_type)
    # data_list = data_list.order_by(action+action_id)

    template = render(request, 'list_table.html', {'list': data_list})
    # print(template)
    return JsonResponse({'template':template.content})

def get_search(request, position=None, industry=None, location=None, salary=None, salary_type=None, salary_filter=None):

    search_form = Search_Bar_Form(request.GET)
    position = request.GET.get('keyword')
    industry = request.GET.get('industry')
    location = request.GET.get('location')
    salary_up = request.GET.get('input-with-keypress-0')
    salary_low = request.GET.get('input-with-keypress-1')
    salary_type = request.GET.get('salary_type')
    data_get_list = [position, industry, location, salary_up, salary_low, salary_type]
    print (data_get_list)

    paginator_link = "?keyword={}&industry={}&location={}&salary_type={}&salary_up={}&salary_low={}".format(position.encode('utf8'), industry, location.encode('utf8'), salary_type.encode('utf8'), salary_up, salary_low)

    data_list = labor_gov_model
    # return HttpResponse(data_get_list)
    if position:
        data_list = data_list.filter(jobTitle__contains=position)
        print ('s')
    if industry and industry!='all':
        data_list = data_list.filter(industry=industry)
    if location and location!='all':
        data_list = data_list.filter(location2=location)
    if salary_type:
        data_list = data_list.filter(salary_type=salary_type)
    if salary_up and salary_low:
        data_list = data_list.filter(money__gte=salary_low).filter(money__lte=salary_up)

    """paginator"""
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
        # If page is not an integer, deliver first page.
        data_show = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_show = paginator.page(paginator.num_pages)
# bookmark
    # return render(request, 'gov_jobs_detial.html', {'list': data_show})
    # return render(request, 'list_view2.html', {'list': data_show, 'form':search_form, 'paginator_link':paginator_link, 'show_page_list':show_page_list})
    return render(request, 'search_page.htm', {'list': data_show, 'form':search_form, 'paginator_link':paginator_link, 'show_page_list':show_page_list})


def search(request):
    if request.method == "POST":
        search_form = Search_Bar_Form(request.POST)
        if search_form.is_valid():
            position = search_form.cleaned_data['keyword']
            industry = search_form.cleaned_data['industry']
            location = search_form.cleaned_data['location']
            salary = search_form.cleaned_data['salary']
            salary_type = search_form.cleaned_data['salary_type']

            data_list = labor_gov_model
            print (salary_type)
            if position:
                data_list = data_list.filter(jobTitle__contains=position)
            if industry and industry!='all':
                data_list = data_list.filter(industry=industry)
            if location and location!='all':
                data_list = data_list.filter(location2=location)
            if salary_type:
                data_list = data_list.filter(salary_type=salary_type)
            if salary:
                data_list = data_list.filter(money__gte=salary)
                # data_list.filter(salary_type=salary_type)

            """paginator"""
            paginator = Paginator(data_list, 25) # Show 25 contacts per page

            page = request.GET.get('page')
            try:
                data_show = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                data_show = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                data_show = paginator.page(paginator.num_pages)


        # bookmark
            # return render(request, 'gov_jobs_detial.html', {'list': data_show})
            return render(request, 'list_view2.html', {'list': data_show, 'form':search_form})
            # return redirect('jobs_gov_data_filter', position=None, industry=None, location=None ,salary=None)
            # return redirect('jobs_gov_data_filter', pk=element.id)
            # return HttpResponse([position, industry, location])
    else:
        search_form = Search_Bar_Form()
        return render(request, 'list_view2.html', {'form': search_form})

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
