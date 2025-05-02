from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import ShiftForm, HrGroupForm
from .models import (
    HrGroup, HrEmployee, AttShift, EmpleadoTurno,
    EmpJob, EmpRole, EmpCostCenter, AttPunch
)

from API.utils.turnos import detectar_turno
from API.utils.reportes import (
    procesar_marcaciones, generar_reporte_basico, reporte_horas_extras
)

from API.utils.reportes import procesar_marcaciones
from datetime import datetime
from django.utils.timezone import make_aware
from django.shortcuts import redirect

# ================== VISTAS GENERALES ==================
def home(request):
    return render(request, 'home.html')

def configuracion_view(request):
    return render(request, 'configuracion.html')

def asistencia_view(request):
    return render(request, 'grupos.html')

# ================== LOGIN ==================
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    return redirect('login')

# ================== TURNOS ==================
def turnos_view(request):
    return render(request, 'turnos.html')

def lista_turnos(request):
    turnos = AttShift.objects.all()
    return render(request, 'turnos.html', {'turnos': turnos})

def crear_turno(request):
    if request.method == "POST":
        data = {key: request.POST.get(key) for key in [
            "shift_name", "start_time", "max_entry_time", "end_time",
            "work_hours", "break_type", "break_minutes", "break_start", "break_end", "status"
        ]}
        nuevo_turno = AttShift.objects.create(**data)
        return JsonResponse({"success": True, "id": nuevo_turno.id, **{k: str(getattr(nuevo_turno, k)) for k in data}})
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)

def editar_turno(request, id):
    turno = get_object_or_404(AttShift, id=id)
    if request.method == "POST":
        form = ShiftForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": form.errors}, status=400)
    return render(request, "dj/editar_turno.html", {"form": ShiftForm(instance=turno), "turno": turno})

def eliminar_turno(request, id):
    turno = get_object_or_404(AttShift, id=id)
    if request.method == "POST":
        turno.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)

# ================== GRUPOS ==================
def crear_grupo(request):
    if request.method == "POST":
        form = HrGroupForm(request.POST)
        if form.is_valid():
            grupo = form.save()
            return JsonResponse({"success": True, "id": grupo.id, "nombre": grupo.nombre}, status=201)
        return JsonResponse({"success": False, "error": form.errors.as_json()}, status=400)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def lista_grupos(request):
    grupos = HrGroup.objects.all()
    return render(request, 'grupos.html', {'grupos': grupos})

def obtener_grupos(request):
    if request.method == 'GET':
        grupos = list(HrGroup.objects.values('id', 'nombre'))
        return JsonResponse({'grupos': grupos})

# ================== EMPLEADOS ==================
def empleados_view(request):
    return render(request, 'empleados.html')

def lista_empleados(request):
    context = {
        "empleados": HrEmployee.objects.all(),
        "grupos": HrGroup.objects.all(),
        "cargos": EmpJob.objects.all(),
        "roles": EmpRole.objects.all(),
        "centros_costos": EmpCostCenter.objects.all(),
    }
    return render(request, "empleados.html", context)

def crear_empleado(request):
    if request.method == "POST":
        try:
            data = {
                "emp_pin": request.POST["emp_pin"],
                "emp_firstname": request.POST["emp_firstname"],
                "emp_lastname": request.POST["emp_lastname"],
                "emp_job": get_object_or_404(EmpJob, id=request.POST["emp_job"]),
                "emp_group": get_object_or_404(HrGroup, id=request.POST["emp_group"]),
                "emp_role": get_object_or_404(EmpRole, id=request.POST["emp_role"]),
                "emp_cost_center": get_object_or_404(EmpCostCenter, id=request.POST["emp_cost_center"]),
                "emp_email": request.POST["emp_email"],
                "emp_active": request.POST.get("emp_active") == "on",
            }
            HrEmployee.objects.create(**data)
            return redirect("empleados")
        except Exception as e:
            context = {
                "empleados": HrEmployee.objects.all(),
                "grupos": HrGroup.objects.all(),
                "cargos": EmpJob.objects.all(),
                "roles": EmpRole.objects.all(),
                "centros_costos": EmpCostCenter.objects.all(),
                "error": str(e),
            }
            return render(request, "empleados.html", context)
    return redirect("empleados")

# ================== REPORTES ==================
def reporte_turnos(request):
    asignaciones = EmpleadoTurno.objects.select_related('empleado', 'turno').all()
    return render(request, 'reportes/turnos.html', {'asignaciones': asignaciones})

def reportes_view(request):
    tipo = request.GET.get("tipo", "basico")
    cedula = request.GET.get("cedula")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    from API.utils.reportes import parse_fecha  # Evitamos import circular
    fecha_inicio = parse_fecha(desde)
    fecha_fin = parse_fecha(hasta)

    if fecha_inicio and fecha_fin:
        procesar_marcaciones(fecha_inicio, fecha_fin)

    filtros = {
        'cedula': cedula,
        'desde': fecha_inicio,
        'hasta': fecha_fin,
    }

    datos = generar_reporte_basico(filtros) if tipo == 'basico' else reporte_horas_extras(filtros)
    return render(request, 'reportes.html', {'datos': datos, 'tipo': tipo})


def ejecutar_procesamiento(request):
    # Definimos el rango de fechas (mismo que el de tu proyecto)
    FECHA_INICIO = make_aware(datetime(2025, 4, 6, 0, 0, 0))
    FECHA_FIN = make_aware(datetime(2025, 4, 25, 23, 59, 59))

    procesar_marcaciones(FECHA_INICIO, FECHA_FIN)

    # Después de procesar, te devuelve al reporte
    return redirect('reportes_view')  # asegúrate que el nombre coincida con el nombre de la vista del reporte