#coding:utf-8#-*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, FreelanceForm, Search_Bar_Form
from .models import Job_detail, jobs_gov, labor_gov
from django.db.models import Count
from django.contrib.auth.models import User
from django.templatetags.static import static
import json
from itertools import chain
import re, datetime
import numpy as np
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 製造頁面
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

    # 第一頁
def homepage(request):
    form = ContactForm()
    form2 = Search_Bar_Form()
    user = request.user
    return render(request, 'name.html', {'form': form, 'form2':form2, 'type':'normal', 'user':user})

def get_name_2(request):
    form = FreelanceForm()
    return render(request, 'name.html', {'form': form, 'type2':'freelance'})

    #第二頁
def job_list(request):#2.1
    model = Job_detail.objects.order_by('-date')
    return render(request, 'list_view.html', {'list':model})

def job_list_work_time(request):#2.2
    model = Job_detail.objects.order_by('working_hour')
    return render(request, 'list_view.html', {'list':model})

def job_list_salary(request):#2.3
    return render(request, 'name.html', {'form': form})

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

def added(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'name.html', {'form': form})


def search(request):
    keyword = request.GET['user_name']
    result = Job_detail.objects.all().filter(company__icontains=keyword)
    return render(request, 'job_search.html', locals())
    # return HttpResponse(keyword)

def customer_order(request):
    keyword = request.GET['orders']
    if keyword == "working_hr_descending":
        result = Job_detail.objects.all().order_by('-working_hour')
    elif keyword == "working_hr_ascending":
        result = Job_detail.objects.all().order_by("working_hour")
    elif keyword == "salary_descending":
        result = Job_detail.objects.all().order_by("-salary")
    elif keyword == "salary_ascending":
        result = Job_detail.objects.all().order_by("salary")

    elif keyword == "time_descending":
        result = Job_detail.objects.all().order_by("date")

    elif keyword == "time_ascending":
        result = Job_detail.objects.all().order_by("-date")

    return render(request, 'list_view.html', {'list':result})
    # return HttpResponse(keyword)


def example(request):
    return HttpResponse("success<br><a href='/job/form'>back home </a>")

# def json_input(request, category='建築/測量'):
#     with open('/Users/mac/Desktop/projects/selenium/data.txt') as data_file:
#         array = json.load(data_file)
#         for x in array:
#             number = x["編號"]
#             date = x["日期"]
#             jobTitle = x["職位"]
#             company = x["公司"]
#             location = x["地點"]
#             industry = x["行業"]
#             responsibility = x["職責"]
#             qualification = x["資歷"]
#             treatment = x["待遇"]
#             appNote = x["申請須知"]
#             remark = x["備註"]
#             jobs_gov.objects.create(number=number, date=date, jobTitle=jobTitle, company=company, location=location, industry=industry, responsibility=responsibility, qualification=qualification, treatment=treatment, appNote=appNote, remark=remark, category=category)
#     return HttpResponse("success")



def jobs_gov_data(request, category=None):

    if category==None:
        data_list = labor_gov.objects.none()
        # data_list_data = labor_gov.objects.all().values('industry').annotate(Count('industry'))
        industry_array = []

        # model_j = labor_gov.objects.all()
        model_j = labor_gov.objects.all()[20:100]

        position_statistic = model_j.values('jobTitle', 'company').annotate(Count('company')).annotate(Count('jobTitle'))

        for x in position_statistic:
            print '公司名稱是{}，有{}次重覆。這間公司的職位總類有{}, 分別是{}'.format(x['company'],x['company__count'], x['jobTitle__count'], x['jobTitle'])
            # if x['company__count']>1:
                # print '{}: {}'.format(x['company'], x['jobTitle__count'])

        # 記住了每個行業
        industry_statistic = labor_gov.objects.all().values('industry').annotate(Count('industry'))

        for category in industry_statistic:
            # print type(category)
            if category['industry__count'] > 100:
                category_queryset = labor_gov.objects.filter(industry=category['industry'])[:100]
                category['show_number'] = 100
            else:
                category_queryset = labor_gov.objects.filter(industry=category['industry'])
                category['show_number'] = category['industry__count']
            data_list = list(chain(data_list, category_queryset))

        # for index, value in data_list_data.items():
            # industry_array.append()

        # k = Time.objects.values('date').annotate(Count('event'))
        data_list_origin = labor_gov.objects.filter(company__contains="永安").values()
        # print data_list
        # data_list_origin = labor_gov.objects.filter(location2="")
        # data_list = labor_gov.objects.filter(company__contains="永安").distinct()
        # data_list=[]
        # empty=[]


        # 用來查有哪些只有一個地點，哪些有超過一個地點
        # for x in data_list_origin:
        #     if x.location.find(u',')==-1:
        #         # pass
        #         empty.append(x.location)
        #     else:
        #         pass
        #         # print x.location
        # print set(empty)

    else:
        data_list = labor_gov.objects.filter(working_day="")
    # data_list = labor_gov.objects.filter(location__contains="香港島,九龍半島,新界")
    # data_list = labor_gov.objects.filter(week_total_hour__gt=80)
    data_list = labor_gov.objects.filter(week_total_hour__gt=70.0).order_by('-week_total_hour')


    # data_list = labor_gov.objects.all()


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
    return render(request, 'list_view2.html', {'list': data_show, 'industry_statistic': industry_statistic})

def refine_data(request):
    # for x in cake:
    #     labor_gov.objects.create(number=x.number, date=x.date, jobTitle=x.jobTitle, company=x.company, location=x.location, industry=x.industry, responsibility=x.responsibility, qualification=x.qualification, treatment=x.treatment, appNote=x.appNote, remark=x.remark, category=x.category, exported=x.exported, money=x.money)
    #     print x

    # 透過json入資料
    import json
    data = json.load(open('/Users/mac/Desktop/projects/e_learning/educa/files/18_district_location.json'))

    def search(Dict, word):
        for key, value in Dict.items():
            for v in value:
                if word in v:
                    return key

    model_objects = labor_gov.objects.filter(working_hours_number_float=0.0)
    # model_objects = labor_gov.objects.filter(working_hours_number__contains='每天工作')

    # model_objects = labor_gov.objects.all()
    show_data = model_objects
    number_found = model_objects.count()
    # model_objects = labor_gov.objects.all()

    # print "數字有:"+ str(labor_gov.objects.filter(location2="").count())
    # word_list = []

    # before = u'^筲箕灣$'
    # replace_location = u'東區'

    # word = re.compile(before)

    order = True
    order = False

    # 地區replacement

    # for x in model_objects:
    #     x.location2 = x.location2.replace('區區', '區')
    #     x.save()



    for x in model_objects:
        """用來處理工時等於零的fucntion"""
        pass

    """用來抽出數字和."""
    for x in model_objects:
        # print x.working_hours_number
        string_element = [symbol for symbol in x.working_hours_number if symbol=='.' or symbol.isdigit() or symbol=='-']

        # x. = ''.join(string_element)

        # print (''.join(string_element), x.working_hours_number)

        # x.location2 = x.location2.replace(',,', ',')
        # x.location2 = '全港'
        # before = x.location2
        # all_locations = x.location2.split(',')
        # all_locations = set(all_locations)
        #
        # x.location2 = ', '.join(all_locations)
        # x.save()





        # if search(data, x.location):
            # x.location2 = search(data, x.location)
        # x.location2 = x.location.replace('港九新界', '全港')
        # print x.location2


    # k = re.search(word, text)
    # print k.group()
    # for x in model_objects:
    #
    #     k = re.search(word, x.location)
    #     if k:
    #         word_list.append(before)
    #         x.location2 = replace_location
    #         if order:
    #             x.save()
            # print k.group()

        # if re.search(word, x.treatment):
        # print x.treatment
#
# 從資料data的 labor_gov.treatment 中抽出工作時間，將它寫入labor_gov.working_date
#
    # filter出labor_gov中，working_date中為空的data
    # model_objects = labor_gov.objects.filter(working_hours_number='')

    # before為想找的文字
    # word 是將 before 中的文字轉為 re Pattern object

    working_hours_number_pattern = u'每天工作\s?\d\s?-\s?\d{,2}(.5)?\s?小時'
    # working_hours_number_pattern = u'(每週)?工作\s?\d(\.\d)?\s?[或-]?(\s?\d(\.\d)?\s?)?天'

    working_day_number_pattern = u'(每週)?工作\s?\d(\.\d)?\s?[或-]?(\s?\d(\.\d)?\s?)?天'

    working_hours_pattern_1= u'((上午)|(中午)|(下午)|(凌晨))\s?[\d]{,2}\s?時(\d{,2})?[半|分]?[至|-]((上午)|(中午)|(下午)|(凌晨)|(午夜))\s?[\d]{,2}\s?時(\d{,2})?[半|分]?'
    working_hours_pattern_2=u'(\d{,2}:\d{,2}(AM)|(PM))-(\d{,2}:\d{,2}(AM|PM))',


    king = [  working_hours_number_pattern, ]
    # 中午12時至下午6時
    #  上午8時半至中午12時半
# 下午6時至凌晨3時
    # 上午8時45分至下午6時,

    word = [re.compile(patterns) for patterns in king]

    # order = True
    # order = False
    #
    # number_found = 0

    # loop through model_objects
    # 利用 re 中的 search function，找出 labor_gov.treatment 有沒有想找的 word pattern
    # 如果有的話，就將數字加1，如果order為True，就將instance中的 working_date 寫入 word pattern
    # word pattern 例如 上午[\d]+時至下午[\d]+時, 每週工作[\d]天, 每天工作[\s]?\d[\s]?小時
    # 找到的話，將instance放入去show_data之中
    # k.group()是找到的文字
    # show_data = []

    # for x in model_objects:
        # word pattern 為 compile object list中的instance
        # word = [re.compile(patterns) for patterns in king]
        # output = []
        # for word_pattern in word:
        #     k = re.search(word_pattern, x.treatment)
        #     if k:
        #         output.append(k.group())
        #         number_found+=1
        #         show_data.append(x)
        # if order:
        #     for dummy in output:
        #         print dummy
        #         if re.search(re.compile(working_hours_number_pattern), dummy):
        #             x.working_hours_number = dummy
        #             x.save()
                # if re.search(re.compile(u'星期一'), dummy):
                #     x.working_week = dummy
                #     x.save()
                # if re.search(re.compile(working_day_number_pattern), dummy):
                #     x.working_day_number = dummy
                #     x.save()
                #     print x
                # if re.search(re.compile(u'(\d{,2}:\d{,2}(AM)|(PM))-(\d{,2}:\d{,2}(AM|PM))'), dummy) or re.search(re.compile(working_hours_pattern_1), dummy):
                #     x.working_hours = dummy
                #     x.save()



                # if re.search(re.compile(u'輪休'), dummy):
                #     x.working_shift = dummy
                #     x.save()
            # x.working_date = ", ".join(dummy for dummy in output)
            # output_text = ",".join(dummy for dummy in output)
            # print "{}的工作時間是{} \n原文︰{}\n".format(x.jobTitle,output_text, x.treatment)
#
    # show_data = labor_gov.objects.filter(working_hours_number='')
    # show_data = labor_gov.objects.filter(treatment__contains=u'每天').filter(working_hours_number='')
    # show_data = labor_gov.objects.all()
    # print labor_gov.objects.filter(working_hours_number='').count()

    return render(request, 'gov_jobs_detial.html', {'list': show_data, 'number_found': number_found})


def average_data():
    '''
    以下部分是將每天時時的data轉為float
    '''
    for x in model_objects:
        '''
        將每週工作天的data斬剩數字部份
        '''
        u = x.working_day_number
        u = x.working_day_number.replace('每週工作', '').replace('天半', '.5').replace('天至','-').replace('天', '').replace('至','-')
        x.working_shift = u
        x.save()

        # k將工時數字分為list
        # 例如'8-9', 轉為['8','9']
        k = x.working_hours_number_float.split('-')
        # u為 '8', '9'
        if len(k)>1:
            average = (float(k[0])+float(k[1]))/2
            x.working_hours_number_float = average
            x.save()

        else:
            x.working_hours_number_float = float(k[0])

def clean_function(k):
    '''
    將分為兩個部份
    '''
    list_date = k.working_shift.split('至')
    k.remark = list_date[1]
    k.appNote = list_date[0]

    '''
    取代部份
    '''
    k.appNote = k.appNote.replace('時半',':30').replace('時',':00')
    k.appNote = k.appNote.replace('0045',':45')

    k.remark = k.remark.replace('時半',':30').replace('時',':00')
    k.remark = k.remark.replace('0045',':45')

    print k.appNote.find('上午')
    if k.appNote.find('上午')==0:
        k.appNote = k.appNote.replace('上午','')+'AM'
    if k.appNote.find('下午')==0:
        k.appNote = k.appNote.replace('下午','')+'PM'

    if k.remark.find('下午')==0:
        k.remark = k.remark.replace('下午','')+'PM'

    start_time = datetime.datetime.strptime(k.appNote, '%I:%M%p')
    end_time = datetime.datetime.strptime(k.remark, '%I:%M%p')
    time_delta = end_time - start_time
    time_list = str(time_delta).split(':')
    total_time = int(time_list[0])+ (int(time_list[1])/60.0)
    print(total_time)
    k.responsibility = total_time

    k.working_day_number_float = float(k.working_day_number_float )
    k.working_hours_number_float = float(k.responsibility )

def filter_out_start_and_end(x):
    """將上午8時半至下午5時半 filter 到start_time和end_time，變為8:30am和5:30pm"""
    start_to_end = x.working_hours.split('至')

    # time_list = [(u'上午', 'am'), (u'下午', 'pm'), (u'凌晨', 'am'), (u'中午','pm')]
    time_list = [(u'中午','pm'), ]
    for time in time_list:
        if re.search(time[0], start_to_end[0]):
            new_text = start_to_end[0].replace(time[0], '').replace('分','').replace('時', ':').replace('半', '30') + time[1]
            print x.start_time
            x.start_time = new_text

    for time in time_list:
        if re.search(time[0], start_to_end[1]):
            new_text = start_to_end[1].replace(time[0], '').replace('時', ':').replace('半', '30') + time[1]
            x.end_time = new_text
            print x.end_time
            # x.save()

def handle_special_case(x):
    """處理 :pm 和 :am 等情況"""
    x.end_time = x.end_time.replace(':pm',':00pm')
    x.end_time = x.end_time.replace(':am',':00am')
    x.start_time = x.start_time.replace(':pm',':00pm')
    x.start_time = x.start_time.replace(':am',':00am')

def calculate_how_many_hours(x):
        start_time = datetime.datetime.strptime(x.start_time, '%I:%M%p')
        end_time = datetime.datetime.strptime(x.end_time, '%I:%M%p')
        time_delta = end_time - start_time
        time_list = str(time_delta).split(':')
        total_time = int(time_list[0])+ (int(time_list[1])/60.0)
        print(total_time)
        x.responsibility = round(total_time, 2)
        x.end_time = x.end_time.replace('分','')
        # x.working_d
        x.end_time = x.end_time.replace('分','')
        x.working_day_number_float = float(x.working_day_number_float)
        x.working_hours_number_float = round(float(x.responsibility),2)

def calculate_week_hours(x):
    """計算每周工時"""
    a = float(x.working_day_number_float)
    x.working_day_number_float = a
    b = float(x.working_hours_number_float)
    x.working_hours_number_float = b
    print (a, b)
    x.week_total_hour = a*b
    x.save()
    # print x.week_total_hour

def refine_data2(request):
    """選取的model有些甚麼"""
    # model_objects = labor_gov.objects.filter(working_shift='')
    # model_objects = labor_gov.objects.all()[10:60]
    # model_objects = labor_gov.objects.filter(week_total_hour=0.0)
    # model_objects = labor_gov.objects.all()[20:200]
    model_objects = labor_gov.objects.all()

    """model中的物件"""
    for x in model_objects:
        try:

            # filter_out_start_and_end(x)
            # handle_special_case(x)
            # calculate_how_many_hours(x)
            calculate_week_hours(x)

        except Exception as e:
            pass

    # model_objects = labor_gov.objects.filter(working_hours_number_float=0.0)

    return render(request, 'gov_jobs_detial.html', {'list': model_objects})
