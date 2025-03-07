from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render

def turnos_view(request):
    return render(request, 'turnos.html')

def empleados_view(request):
    return render(request, 'empleados.html')

def asistencia_view(request):
    return render(request, 'asistencia.html')

def reportes_view(request):
    return render(request, 'reportes.html')

def configuracion_view(request):
    return render(request, 'configuracion.html')


# Vista para el login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticar al usuario
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect('home')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para el logout
# Vista para el logout
def logout_view(request):
    
    return redirect('login')  # Redirige a la página principal después de cerrar sesión

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')



# vistas 

def turnos_view(request):
    return render(request, 'turnos.html')

def empleados_view(request):
    return render(request, 'empleados.html')

def asistencia_view(request):
    return render(request, 'asistencia.html')

def reportes_view(request):
    return render(request, 'reportes.html')

def configuracion_view(request):
    return render(request, 'configuracion.html')

       
