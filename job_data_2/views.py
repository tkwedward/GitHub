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
    form = ContactForm()
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
        form.save()
        return redirect('success')
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
    paginator = Paginator(data_list, 25) # Show 25 contacts per page

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
                color = 'red'
            else:
                color = 'green'

            length = len(category_model.filter(week_total_hour__gte=float(x-1)).filter(week_total_hour__lt=float(x+4)))
            classification.append({'range':'{}-{}'.format(x-1, x+4), 'number':length, 'color':color})
            # print classification


            # print ('{}-{}小時的case有{}個'.format(x-1, x+4, length))
            # print classification
            # print (float(x), float(x+4))

            # print classification
            json_classification = json.dumps(classification)
            # print json_classification


    return render(request, '內頁.html', {'instance': instance, 'average':average, 'maximum':maximum, 'minimum':minimum, 'classification':classification, 'json_classification':json_classification, 'model':model_name, 'category': instance.category})


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
    salary = request.GET.get('salary')
    salary_type = request.GET.get('salary_type')
    salary_filter = request.GET.get('salary_filter')
    data_get_list = [position, industry, location, salary, salary_type]

    paginator_link = "?keyword={}&industry={}&location={}&salary_type={}&salary={}&salary_filter={}".format(position, industry, location, salary_type, salary, salary_filter)

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
    if salary:
        if salary_filter=='higher':
            data_list = data_list.filter(money__gte=salary)
        if salary_filter=='lower':
            data_list = data_list.filter(money__lte=salary)

    """paginator"""
    paginator = Paginator(data_list, 25) # Show 25 contacts per page

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
    return render(request, 'list_view2.html', {'list': data_show, 'form':search_form, 'paginator_link':paginator_link, 'show_page_list':show_page_list})
        # return HttpResponse(abc)
            # return render(request, 'list_view2.html', {'list': data_show, 'form':search_form})

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
