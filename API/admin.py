from django.contrib import admin
from .models import HrEmployee, HrGroup, EmpRole, EmpJob, EmpCostCenter, AttShift, GrupoSupervisor, PermisoRol

admin.site.register(HrEmployee)
admin.site.register(HrGroup)
admin.site.register(EmpRole)
admin.site.register(EmpJob)
admin.site.register(EmpCostCenter)
admin.site.register(AttShift)
admin.site.register(GrupoSupervisor)



class PermisoRolAdmin(admin.ModelAdmin):
    list_display = ('rol', 'vista', 'tiene_acceso')  # columnas visibles
    list_filter = ('vista', 'tiene_acceso')          # filtros laterales
    search_fields = ('rol__nombre', 'vista')         # búsqueda por nombre del rol o vista

admin.site.register(PermisoRol, PermisoRolAdmin)
