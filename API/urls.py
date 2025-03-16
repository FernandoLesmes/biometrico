from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),

    # 🔹 Rutas corregidas con los nombres correctos
    path('empleados/', views.empleados_view, name='empleados'),
    path('asistencias/', views.asistencia_view, name='asistencia'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('configuracion/', views.configuracion_view, name='configuracion'),

    # 🔹 Rutas para turnos
    path("turnos/", views.lista_turnos, name="turnos"),
    path("turnos/crear/", views.crear_turno, name="crear_turno"),
    path("turnos/editar/<int:id>/", views.editar_turno, name="editar_turno"),
    path("turnos/eliminar/<int:id>/", views.eliminar_turno, name="eliminar_turno"),
]



