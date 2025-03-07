from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('API.urls')),
    path('login/', auth_views.LogoutView.as_view(), name='login/'),
]
