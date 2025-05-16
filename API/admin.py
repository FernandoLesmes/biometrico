from django.contrib import admin
from .models import HrEmployee, HrGroup, EmpRole, EmpJob, EmpCostCenter, AttShift

admin.site.register(HrEmployee)
admin.site.register(HrGroup)
admin.site.register(EmpRole)
admin.site.register(EmpJob)
admin.site.register(EmpCostCenter)
admin.site.register(AttShift)

# Register your models here.
