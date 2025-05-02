from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import crear_grupo
from .views import lista_grupos
from .views import obtener_grupos
from .views import lista_empleados, crear_empleado
from .views import reportes_view
from API.views import ejecutar_procesamiento


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),

    # 🔹 Rutas corregidas con los nombres correctos
    #path('empleados/', views.empleados_view, name='empleados'),
    path('grupos/', views.asistencia_view, name='grupos'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('configuracion/', views.configuracion_view, name='configuracion'),

    # 🔹 Rutas para turnos
    path("turnos/", views.lista_turnos, name="turnos"),
    path("turnos/crear/", views.crear_turno, name="crear_turno"),
    path("turnos/editar/<int:id>/", views.editar_turno, name="editar_turno"),
    path("turnos/eliminar/<int:id>/", views.eliminar_turno, name="eliminar_turno"),
    #grupos
    path("grupos/", lista_grupos, name="grupos"),
    path("grupos/crear/", crear_grupo, name="crear_grupo"),
    path('grupos/obtener/', obtener_grupos, name='obtener_grupos'),
    
    
    #empleados
    path('empleados/', lista_empleados, name='empleados'),
    #path('empleados/', lista_empleados, name="lista_empleados"),
    path('empleados/crear/', crear_empleado, name="crear_empleado"),
    
    # empleado turno, definimos reportes para horas extras
    path('reportes/turnos/', views.reporte_turnos, name='reporte_turnos'),

    #solo reportes basicos 
    path('reportes', views.reportes_view, name='reportes_view'),
    
    #reportes de horas extras
    path('reportes/horas_extras', views.reporte_horas_extras, name='reporte_horas_extras'),
    path('procesar-marcaciones/', ejecutar_procesamiento, name='procesar_marcaciones'),

   

    

    
]



