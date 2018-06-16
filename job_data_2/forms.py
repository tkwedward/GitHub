#coding=utf-8 #coding:utf-8#-*-
from django import forms
from django.forms.widgets import HiddenInput
from .models import Job_detail, User, Freelance, labor_gov, collected_data
from django.utils.timezone import datetime

from .important_list import DISTRICT_LIST, INDUSTRY_LIST, SALARY_TYPE_LIST, SEX_CHOICES, TYPES_CHOICES, OTP_CHOICES, OT_CHOICES

"""高於、低於、等於"""
SALARY_FILTER = [
('higher', '高於'),
('lower', '低於'),
('equal', '等於')]

# print(CATEGORY_CHOICES)
class Search_Bar_Form(forms.Form):
    """
    以下是form的內容
    """

    keyword = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '職位'}),
        max_length=30,
        label='',
        required=False
        )

    location = forms.CharField(
        widget=forms.Select(choices=DISTRICT_LIST), required=False, label='', initial='all'
    )

    industry = forms.CharField(
        widget=forms.Select(choices=INDUSTRY_LIST), required=False, label='', initial='all'
    )

    salary_type = forms.CharField(
        widget=forms.Select(choices=SALARY_TYPE_LIST), required=False, label='', initial='all'
    )

    salary_filter = forms.CharField(
        widget=forms.Select(choices=SALARY_FILTER), required=False, label='', initial='all'
    )

    salary = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '薪金'}),
        max_length=30,
        label='',
        required=False,
        )

    upper_limit = forms.CharField(
        max_length=10,
        label='',
        required=False,
        )
    lower_limit = forms.CharField(
        max_length=10,
        label='',
        required=False,
        )


OT_choices = (
    ('','加班頻率'),
    ('seldom','絕少'),
    ('sometimes', '偶爾'),
    ('often', '經常'),
    ('always', '幾乎每天')
)

OTP_choices=(
    ('','加班費'),
    ('yes','有'),
    ('yes_yes','可選擇補水或補假'),
    ('no_yes','沒有補水，有補假'),
    ('no_no','沒有補水，沒有補假'),
    ('no_idea','不知道')
)

class FreelanceForm(forms.ModelForm):
    job_name = forms.CharField(label='工作名稱', max_length=30)
    job_location = forms.CharField(label='地點', max_length=30)
    date = forms.DateField(label='日期', initial=datetime.today())

    class Meta:
        model = Freelance

        fields = '__all__'

class ContactForm(forms.ModelForm):

    company = forms.CharField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'公司名稱'}),
    )

    industry = forms.ChoiceField(widget=forms.Select(), choices=INDUSTRY_LIST, label='', initial='all')

    # 職位名稱
    jobTitle = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': u'職位名稱'}))

    # 工作地點
    place = forms.ChoiceField(widget=forms.Select(), choices=DISTRICT_LIST, label='', initial='all')

    # 職務型態
    job_type = forms.ChoiceField(widget=forms.Select(), choices=TYPES_CHOICES, label='', initial='')

     # 工作天數
    date_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'工作天數'}))


    # 性別
    gender=forms.ChoiceField(widget=forms.Select(), choices=SEX_CHOICES, label='', initial='')

    # 你最近從事這份工作的年份
    latest_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'你最近從事這份工作的年份（例如由2014年做到2016年，請填2016；如現正從事這份工作，請填2017年）'}))


    # 支薪周期
    salary_period = forms.ChoiceField(widget=forms.Select(), choices=SALARY_TYPE_LIST, label='')

    # 行業年資
    year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'行業年資'}))

    # 合約列明一周工時
    contract_hour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'合約列明一周工時（如沒有合約或沒有標明，請填0）'}))

    OT_payment = forms.ChoiceField(widget=forms.Select(), choices=OTP_CHOICES, label='')

    #
    OT_frequency = forms.ChoiceField(widget=forms.Select(), choices=OT_CHOICES)

    week_total_hour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'一周實際工時'}))

    date = forms.DateField(initial=datetime.today())



    class Meta:
        model = collected_data
        widgets = {
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '薪資'}),

            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '電郵'}),

            'OT': forms.TextInput(attrs={'class': 'form-control', 'value':'seldom'}),
# label='Overtime_human_read'
        }

        error_messages = {
                'company':{
                    'required': '請填入資料'
                }
        }

        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['company'].error_messages = {'required': 'custom required message'}

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = 'user_name', 'password'


class RegForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
