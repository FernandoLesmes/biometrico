from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    crear_grupo, lista_grupos, obtener_grupos,
    lista_empleados, crear_empleado,
    reportes_view, reporte_horas_extras,aprobar_horas_extra,
)
from API.views import ejecutar_procesamiento
from API.views import historial_horas_extras_ajax


urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Vista principal de grupos (solo una)
    path('grupos/', views.grupos_view, name='grupos'),

    # Rutas auxiliares para otras vistas relacionadas a gruposA
    path('grupos/asistencia/', views.asistencia_view, name='asistencia_view'),
    path('grupos/listado/', lista_grupos, name='lista_grupos'),

    path('grupos/crear/', crear_grupo, name='crear_grupo'),
    path('grupos/obtener/', obtener_grupos, name='obtener_grupos'),
    path('grupo/<int:id>/detalle/', views.detalle_grupo, name='detalle_grupo'),
    path('grupo/<int:id>/asignar_roles/', views.asignar_roles_grupo, name='asignar_roles_grupo'),

    # Empleados
    path('empleados/', lista_empleados, name='empleados'),
    path('empleados/crear/', crear_empleado, name='crear_empleado'),
    path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/obtener/<int:id>/', views.obtener_empleado, name='obtener_empleado'),
    path("empleados/cambiar_estado/", views.cambiar_estado_empleado, name="cambiar_estado_empleado"),

    # Turnos
    path("turnos/", views.lista_turnos, name="turnos"),
    path("turnos/crear/", views.crear_turno, name="crear_turno"),
    path("turnos/editar/<int:id>/", views.editar_turno, name="editar_turno"),
    path("turnos/cambiar_estado/", views.cambiar_estado_turno, name="cambiar_estado_turno"),

    # Reportes
    path('reportes/', views.reportes_view, name='reportes_view'),
    path('reportes/turnos/', views.reporte_turnos, name='reporte_turnos'),
    path('reportes/horas_extras/', views.reporte_horas_extras, name='reporte_horas_extras'),

    # Procesamiento
    path('procesar-marcaciones/', views.ejecutar_procesamiento, name='procesar_marcaciones'),

    # Configuraciones
    path('configuracion/', views.configuracion_view, name='configuracion'),
    path('crear-cargo/', views.crear_cargo, name="crear_cargo"),
    path('crear-rol/', views.crear_rol, name="crear_rol"),
    path('crear-centro-costo/', views.crear_centro_costo, name="crear_centro_costo"),
    
    path("configuracion/toggle-usuario/", views.toggle_usuario_activo, name="toggle_usuario"),
    
    path("reportes/aprobar/", views.aprobar_horas_extra, name="aprobar_horas_extra"),

    path("exportar_excel/", views.exportar_excel_general, name="exportar_excel_general"),
    
    path("historial-horas-extras/ajax/", historial_horas_extras_ajax, name="historial_horas_extras_ajax"),
    
    

]


    

    




