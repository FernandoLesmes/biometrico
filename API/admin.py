from django.contrib import admin
from .models import HrEmployee, HrGroup, EmpRole, EmpJob, EmpCostCenter, AttShift, GrupoSupervisor

admin.site.register(HrEmployee)
admin.site.register(HrGroup)
admin.site.register(EmpRole)
admin.site.register(EmpJob)
admin.site.register(EmpCostCenter)
admin.site.register(AttShift)
admin.site.register(GrupoSupervisor)
# Register your models here.
