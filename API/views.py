from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

from .forms import ShiftForm
from .models import AttShift
from django.http import JsonResponse

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

#VISTA PARA REGISTRAR TURNOS

# 📌 Vista para listar y crear turnos
def lista_turnos(request):
    turnos = AttShift.objects.all()
    return render(request, 'turnos.html', {'turnos': turnos})

def crear_turno(request):
    if request.method == "POST":
        shift_name = request.POST.get("shift_name")
        start_time = request.POST.get("start_time")
        max_entry_time = request.POST.get("max_entry_time")
        end_time = request.POST.get("end_time")
        work_hours = request.POST.get("work_hours")
        break_type = request.POST.get("break_type")
        break_minutes = request.POST.get("break_minutes")
        break_start = request.POST.get("break_start")
        break_end = request.POST.get("break_end")
        status = request.POST.get("status")

        nuevo_turno = AttShift.objects.create(
            shift_name=shift_name,
            start_time=start_time,
            max_entry_time=max_entry_time,
            end_time=end_time,
            work_hours=work_hours,
            break_type=break_type,
            break_minutes=break_minutes,
            break_start=break_start,
            break_end=break_end,
            status=status
        )

        return JsonResponse({
            "success": True,
            "id": nuevo_turno.id,
            "shift_name": nuevo_turno.shift_name,
            "start_time": str(nuevo_turno.start_time),
            "max_entry_time": str(nuevo_turno.max_entry_time),
            "end_time": str(nuevo_turno.end_time),
            "work_hours": nuevo_turno.work_hours,
            "break_type": nuevo_turno.break_type,
            "break_minutes": nuevo_turno.break_minutes,
            "break_start": str(nuevo_turno.break_start) if nuevo_turno.break_start else "",
            "break_end": str(nuevo_turno.break_end) if nuevo_turno.break_end else "",
            "status": nuevo_turno.status
        })
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)

# ✅ EDITAR TURNO
def editar_turno(request, id):
    turno = get_object_or_404(AttShift, id=id)

    if request.method == "POST":
        form = ShiftForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Turno actualizado correctamente"})
        else:
            return JsonResponse({"success": False, "error": form.errors}, status=400)

    else:
        form = ShiftForm(instance=turno)

    return render(request, "dj/editar_turno.html", {"form": form, "turno": turno})


# ✅ ELIMINAR TURNO
def eliminar_turno(request, id):
    turno = get_object_or_404(AttShift, id=id)

    if request.method == "POST":
        turno.delete()
        return JsonResponse({"success": True, "message": "Turno eliminado correctamente"})

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)