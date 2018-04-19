from django.contrib import admin
from .models import Job_detail, User, Freelance
from .models import  labor_gov
# Register your models here.

class labor_govAdmin(admin.ModelAdmin):
    model = labor_gov
    list_display = ('jobTitle', 'category', 'location2')
    search_fields = ('jobTitle', 'category', 'location2', 'company')


admin.site.register(Job_detail)
admin.site.register(labor_gov, labor_govAdmin)
admin.site.register(Freelance)
admin.site.register(User)
