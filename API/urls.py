from django.urls import path
from . import views  # Importa desde el módulo actual (API/views.py)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),  # Esta es la ruta para la página de inicio
    
    path('turnos/', views.turnos_view, name='turnos'),
    path('empleados/', views.empleados_view, name='empleados'),
    path('asistencia/', views.asistencia_view, name='asistencia'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('configuracion/', views.configuracion_view, name='configuracion'),
]
