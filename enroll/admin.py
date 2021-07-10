from django.contrib import admin
from .models import *

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display=['p_id','f_name', 'l_name', 'age']

class QuesAdmin(admin.ModelAdmin):
    list_display=['q_id','q_text']

class ResultAdmin(admin.ModelAdmin):
    list_display = ['p_id', 'q_id', 'ans_text']

# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(Question, QuesAdmin)
admin.site.register(Result, ResultAdmin)