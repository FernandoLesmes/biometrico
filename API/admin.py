from django.contrib import admin
from .models import HrEmployee, HrGroup, EmpRole, EmpJob, EmpCostCenter

admin.site.register(HrEmployee)
admin.site.register(HrGroup)
admin.site.register(EmpRole)
admin.site.register(EmpJob)
admin.site.register(EmpCostCenter)
# Register your models here.
