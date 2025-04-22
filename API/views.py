from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

from .forms import ShiftForm
from .models import AttShift
from django.http import JsonResponse

from .models import HrGroup
from  .forms import HrGroupForm

from django.views.decorators.csrf import csrf_exempt

from .models import HrEmployee,  EmpJob, EmpRole, EmpCostCenter, HrGroup

from .models import EmpleadoTurno
#aca solo para reporte basico
from .models import HrEmployee, HrGroup, AttPunch
from datetime import datetime, timedelta





from API.utils.turnos import detectar_turno


from API.utils.reportes import procesar_marcaciones


def turnos_view(request):
    return render(request, 'turnos.html')

def empleados_view(request):
    return render(request, 'empleados.html')

def asistencia_view(request):
    return render(request, 'grupos.html')

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

def grupos_view(request):
    return render(request, 'grupos.html')

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

#grupos

#csrf_exempt  # 🔴 Desactiva la protección CSRF (Úsalo solo si es necesario)
def crear_grupo(request):
    if request.method == "POST":
        form = HrGroupForm(request.POST)
        if form.is_valid():
            grupo = form.save()
            return JsonResponse({
                "success": True,
                "id": grupo.id,  
                "nombre": grupo.nombre  # ✅ Devuelve los datos correctos
            }, status=201)
        else:
            print("Errores en el formulario:", form.errors)  # 🔍 Ver errores en terminal
            return JsonResponse({"success": False, "error": form.errors.as_json()}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def lista_grupos(request):
    grupos = HrGroup.objects.all()
    return render(request, 'grupos.html', {'grupos': grupos})  # ✅ Enviar grupos a la plantilla

# ✅ Nueva vista para devolver los datos en JSON (para AJAX)
def obtener_grupos(request):
    if request.method == 'GET':
        grupos = list(HrGroup.objects.values('id', 'nombre'))  # Extrae datos de la BD
        return JsonResponse({'grupos': grupos})  # Devuelve JSON





#empleados
def lista_empleados(request):
    empleados = HrEmployee.objects.all()
    grupos = HrGroup.objects.all()
    cargos = EmpJob.objects.all()
    roles = EmpRole.objects.all()
    centros_costos = EmpCostCenter.objects.all()

    return render(request, "empleados.html", {
        "empleados": empleados,
        "grupos": grupos,
        "cargos": cargos,
        "roles": roles,
        "centros_costos": centros_costos
    })

# Vista para crear un nuevo empleado

def crear_empleado(request):
    if request.method == "POST":
        try:
            emp_pin = request.POST["emp_pin"]
            emp_firstname = request.POST["emp_firstname"]
            emp_lastname = request.POST["emp_lastname"]
            emp_job = get_object_or_404(EmpJob, id=request.POST["emp_job"])
            emp_group = get_object_or_404(HrGroup, id=request.POST["emp_group"])
            emp_role = get_object_or_404(EmpRole, id=request.POST["emp_role"])
            emp_cost_center = get_object_or_404(EmpCostCenter, id=request.POST["emp_cost_center"])
            emp_email = request.POST["emp_email"]
            emp_active = request.POST.get("emp_active", False) == "on"

            HrEmployee.objects.create(
                emp_pin=emp_pin,
                emp_firstname=emp_firstname,
                emp_lastname=emp_lastname,
                emp_job=emp_job,
                emp_group=emp_group,
                emp_role=emp_role,
                emp_cost_center=emp_cost_center,
                emp_email=emp_email,
                emp_active=emp_active
            )
            return redirect("empleados")

        except Exception as e:
            # 👇 Cargar los datos nuevamente
            empleados = HrEmployee.objects.all()
            grupos = HrGroup.objects.all()
            cargos = EmpJob.objects.all()
            roles = EmpRole.objects.all()
            centros_costos = EmpCostCenter.objects.all()

            return render(request, "empleados.html", {
                "empleados": empleados,
                "grupos": grupos,
                "cargos": cargos,
                "roles": roles,
                "centros_costos": centros_costos,
                "error": str(e)
            })

    return redirect("empleados")







#empleado turno
def reporte_turnos(request):
    asignaciones = EmpleadoTurno.objects.select_related('empleado', 'turno').all()

    return render(request, 'reportes/turnos.html', {
        'asignaciones': asignaciones
    })
    

# ✅ Reporte de asistencia básica
def generar_reporte_basico(filtros):
    datos = []
    empleados = HrEmployee.objects.select_related('emp_group')

    if filtros.get('cedula'):
        empleados = empleados.filter(emp_pin__icontains=filtros['cedula'])

    for emp in empleados:
        registros = AttPunch.objects.filter(employee_id=emp.id).order_by('punch_time')

        # Filtro por rango de fechas
        if filtros.get('desde'):
            registros = registros.filter(punch_time__date__gte=filtros['desde'])
        if filtros.get('hasta'):
            registros = registros.filter(punch_time__date__lte=filtros['hasta'])

        dias = {}
        for r in registros:
            fecha = r.punch_time.date()
            dias.setdefault(fecha, []).append(r.punch_time)

        for fecha, marcas in dias.items():
            if len(marcas) < 2:
                continue

            entrada = marcas[0]
            salida = marcas[-1]
            turno = detectar_turno(entrada, salida)

            datos.append({
                'cedula': emp.emp_pin,
                'nombre': emp.emp_firstname,
                'apellidos': emp.emp_lastname,
                'grupo': emp.emp_group.nombre if emp.emp_group else '',
                'fecha': fecha,
                'turno': turno['nombre'] if turno else 'Desconocido',
                'entradas_salidas': marcas
            })

    return datos












# ✅ Reporte de horas extras
def reporte_horas_extras(filtros):
    datos = []
    empleados = HrEmployee.objects.select_related('emp_group')

    if filtros.get('cedula'):
        empleados = empleados.filter(emp_pin__icontains=filtros['cedula'])

    for emp in empleados:
        registros = AttPunch.objects.filter(employee_id=emp.id).order_by('punch_time')

        if filtros.get('desde'):
            registros = registros.filter(punch_time__date__gte=filtros['desde'])
        if filtros.get('hasta'):
            registros = registros.filter(punch_time__date__lte=filtros['hasta'])

        dias = {}
        for r in registros:
            fecha = r.punch_time.date()
            dias.setdefault(fecha, []).append(r.punch_time)

        for fecha, marcas in dias.items():
            if len(marcas) < 2:
                continue

            entrada = marcas[0]
            salida = marcas[-1]
            turno = detectar_turno(entrada, salida)

            total_horas = (salida - entrada).total_seconds() / 3600
            horas_trabajo = turno["horas_turno"] if turno else 8
            horas_extra = max(0, total_horas - horas_trabajo)

            datos.append({
                'cedula': emp.emp_pin,
                'nombre': emp.emp_firstname,
                'apellidos': emp.emp_lastname,
                'grupo': emp.emp_group.nombre if emp.emp_group else '',
                'fecha': fecha,
                'turno': turno['nombre'] if turno else 'Desconocido',
                'entrada': entrada.time(),
                'salida': salida.time(),
                'horas_extras_diurnas': horas_extra if entrada.hour < 18 else 0,
                'horas_extras_nocturnas': horas_extra if entrada.hour >= 18 else 0,
                'horas_extras_festivas_diurnas': 0,
                'horas_extras_festivas_nocturnas': 0,
                'recargo_nocturno': turno["extras_posibles"]["recargo_nocturno"] if turno else 0,
                'recargo_nocturno_festivo': turno["extras_posibles"]["recargo_nocturno_festivo"] if turno else 0,
                'aprobado': False
            })

    return datos


# ✅ Vista unificada para mostrar reportes
def reportes_view(request):
    tipo = request.GET.get("tipo", "basico")
    cedula = request.GET.get("cedula")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    # Ejecutar procesamiento si hay fechas definidas
    if desde and hasta:
        fecha_inicio = datetime.strptime(desde, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(hasta, "%Y-%m-%d").date()
        procesar_marcaciones(fecha_inicio, fecha_fin)

    filtros = {
        'cedula': cedula,
        'desde': desde,
        'hasta': hasta
    }

    if tipo == 'basico':
        datos = generar_reporte_basico(filtros)
    elif tipo == 'horas_extras':
        datos = reporte_horas_extras(filtros)
    else:
        datos = []

    return render(request, 'reportes.html', {
        'datos': datos,
        'tipo': tipo
    })
