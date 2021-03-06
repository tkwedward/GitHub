#coding=utf-8 #coding:utf-8#-*-

DISTRICT_LIST = [
    ('', u'工作地點'),
    (u'中西區', u'中西區'),
    (u'九龍城區', u'九龍城區'),
    (u'元朗區', u'元朗區'),
    (u'北區', u'北區'),
    (u'南區', u'南區'),
    (u'大埔區', u'大埔區'),
    (u'屯門區', u'屯門區'),
    (u'東區', u'東區'),
    (u'沙田區', u'沙田區'),
    (u'油尖旺區', u'油尖旺區'),
    (u'深水埗區', u'深水埗區'),
    (u'灣仔區', u'灣仔區'),
    (u'荃灣區', u'荃灣區'),
    (u'葵青區', u'葵青區'),
    (u'西貢區', u'西貢區'),
    (u'觀塘區', u'觀塘區'),
    (u'離島區', u'離島區'),
    (u'黃大仙區', u'黃大仙區'),
    (u'香港島', u'香港島'),
    (u'九龍半島', u'九龍半島'),
    (u'全港', u'全港'),
    (u'香港境外', u'香港境外'),
    # (u'小西灣', u'小西灣'),
    # (u'又一村', u'又一村'),
]


experience_choices=(('0', '請選擇'), ('1','1年或以下'), ('2','2年或以下'), ('3','3年或以下'))

OT_CHOICES = (('all', '加班情況'), (u'絕少','絕少'), (u'偶爾', '偶爾'), (u'經常', '經常'), (u'幾乎每天', '幾乎每天'))

OTP_CHOICES=(('all', '加班補償'), (u'有','有'), (u'沒有','沒有'),  (u'不知道','不知道'))

CHOICES = (('1', 'First',), ('2', 'Second',))

SEX_CHOICES=[('', '性別'),('m','男'), ('f','女'),  ('other','其他')]

TYPES_CHOICES=[('','職務型態'),(u'全職','全職'), (u'兼職(含打工)','兼職(含打工)'),  (u'實習','實習'), (u'臨時工','臨時工'), (u'約聘雇','約聘雇'),(u'派遣','派遣')]


INDUSTRY_LIST = [
    ('', '行業'),
    (u'商用服務業', '商用服務業'),
    (u'飲食業', '飲食業'),
    (u'通訊業', '通訊業'),
    (u'建造業', '建造業'),
    (u'住戶服務業', '住戶服務業'),
    (u'教育服務業', '教育服務業'),
    (u'金融業', '金融業'),
    (u'政府部門', '政府部門'),
    (u'醫院', '醫院'),
    (u'酒店業', '酒店業'),
    (u'進出口貿易', '進出口貿易'),
    (u'保險業', '保險業'),
    (u'電子製品業', '電子製品業'),
    (u'金屬製品業', '金屬製品業'),
    (u'塑膠製品業', '塑膠製品業'),
    (u'紡織業', '紡織業'),
    (u'服裝製品業', '服裝製品業'),
    (u'地產業', '地產業'),
    (u'零售業', '零售業'),
    (u'倉庫業', '倉庫業'),
    (u'運輸業', '運輸業'),
    (u'福利機構', '福利機構'),
    (u'批發業', '批發業'),
    (u'其他社區及社會服務業', '其他社區及社會服務業'),
    (u'其他製造業', '其他製造業'),
    (u'其他個人服務業', '其他個人服務業'),
    #
    # (u'雞場', u'雞場'),
    # (u'印度菜館', u'印度菜館'),
    # (u'四川火鍋店', u'四川火鍋店'),
    # (u'園藝工程', u'園藝工程'),
    # (u'傢俬設計及製造', u'傢俬設計及製造'),
    # (u'雲南菜館', u'雲南菜館'),
    # (u'其他商用服務', u'其他商用服務'),
    # (u'四川菜館', u'四川菜館'),
    # (u'其他', u'其他'),
    # (u'食米批發', u'食米批發'),
    # (u'養魚業', u'養魚業'),
    # (u'耕作業', u'耕作業'),
    # (u'汽車維修服務', u'汽車維修服務'),
    # (u'建築業', u'建築業'),
    # (u'冰凍甜點製造', u'冰凍甜點製造'),
    # (u'調味品製造', u'調味品製造'),
    # (u'殘疾人士院舍', u'殘疾人士院舍'),
    # (u'川滬菜館', u'川滬菜館'),
    # (u'安老院', u'安老院'),
    # (u'傢俬業', u'傢俬業'),
    # (u'豬場', u'豬場'),
    # (u'宗教團體', u'宗教團體'),
    # (u'泰國菜館', u'泰國菜館'),
    # (u'醬料及調味品製造', u'醬料及調味品製造')
]

SALARY_TYPE_LIST = [
    # ('年薪',u'年薪'),
    ('','支薪周期'),
    (u'月薪','月薪'),
    (u'半月薪', '半月薪'),
    (u'週薪', '週薪'),
    (u'日薪', '日薪'),
    (u'時薪', '時薪'),
    (u'件薪', '件薪'),
]

Freelance_category = [
    (u'攝影','攝影'),
    (u'文字','文字'),
    (u'藝術', '藝術'),
    (u'設計', '設計'),
    (u'飲食', '飲食'),
    (u'補習', '補習'),
    (u'其他', '其他')
]
