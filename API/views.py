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

from django.http import JsonResponse
from .models import AttShift
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from .models import AttShift

from .models import HrEmployee 

from API.models import EmpJob, EmpRole, EmpCostCenter
from API.utils.zk_helpers import registrar_en_biometrico
from .models import HrGroup, HrEmployee, GrupoSupervisor
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render


from .models import HrGroup, HrEmployee

from datetime import datetime, timedelta
from django.utils.timezone import make_aware


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from API.models import HrEmployee, EmpRole
from django.db import transaction


# ================== VISTAS GENERALES ==================
def home(request):
    return render(request, 'home.html')



from django.contrib.auth import update_session_auth_hash

def configuracion_view(request):
    if not hasattr(request.user, 'hremployee') or request.user.hremployee.emp_role.nombre != "Administrador":
        messages.error(request, "❌ No tienes permiso para ver esta sección.")
        return redirect("home")

    # Filtrar empleados activos con roles válidos
    roles_validos = ["Administrador", "Supervisor", "Jefe de Área", "Líder HSE"]
    empleados = HrEmployee.objects.filter(emp_active=True, emp_role__nombre__in=roles_validos)

    if request.method == "POST" and 'crear_usuario' in request.POST:
        usuario_id = request.POST.get("usuario_id")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmar_password = request.POST.get("confirmar_password")

        # Validaciones básicas
        if not all([usuario_id, username, password, confirmar_password]):
            messages.error(request, "❌ Todos los campos son obligatorios.")
            return redirect("configuracion")

        if password != confirmar_password:
            messages.error(request, "⚠️ Las contraseñas no coinciden.")
            return redirect("configuracion")

        try:
            empleado = HrEmployee.objects.get(id=usuario_id)

            if empleado.user:
                # Actualizar usuario existente
                empleado.user.username = username
                empleado.user.set_password(password)
                empleado.user.save()

                # Si es el mismo usuario que está en sesión, mantener la sesión activa
                if request.user == empleado.user:
                    update_session_auth_hash(request, empleado.user)
                    messages.success(request, f"🔐 Tu usuario fue restablecido sin cerrar la sesión.")
                else:
                    messages.success(request, f"🔐 Usuario actualizado: {empleado.user.username}")
            else:
                # Crear nuevo usuario si no existe
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"⚠️ El nombre de usuario '{username}' ya está en uso.")
                    return redirect("configuracion")

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=empleado.emp_firstname,
                    last_name=empleado.emp_lastname,
                    email=empleado.emp_email
                )
                empleado.user = user
                empleado.save()
                messages.success(request, f"✅ Usuario creado correctamente para {username}")

        except HrEmployee.DoesNotExist:
            messages.error(request, "❌ Empleado no encontrado.")

        return redirect("configuracion")

    return render(request, "configuracion.html", {"empleados": empleados})




# bloquer usuario de ingreso de sesion
def toggle_usuario_activo(request):
    if not hasattr(request.user, 'hremployee') or request.user.hremployee.emp_role.nombre != "Administrador":
        return JsonResponse({"success": False, "error": "No autorizado"}, status=403)

    usuario_id = request.POST.get("usuario_id")
    try:
        empleado = HrEmployee.objects.get(id=usuario_id)
        if empleado.user:
            empleado.user.is_active = not empleado.user.is_active
            empleado.user.save()
            return JsonResponse({"success": True, "nuevo_estado": empleado.user.is_active})
        else:
            return JsonResponse({"success": False, "error": "Este empleado no tiene usuario creado."})
    except HrEmployee.DoesNotExist:
        return JsonResponse({"success": False, "error": "Empleado no encontrado"})






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
#def turnos_view(request):
    #turnos = AttShift.objects.all().order_by('id')  # o .order_by('start_time') si prefieres por hora
    #return render(request, 'turnos.html', {'turnos': turnos})

def lista_turnos(request):
    turnos = AttShift.objects.all().order_by('id')
    
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
    
    if request.method == "GET":
        return JsonResponse({
            "id": turno.id,
            "shift_name": turno.shift_name,
            "start_time": turno.start_time.strftime('%H:%M'),
            "max_entry_time": turno.max_entry_time.strftime('%H:%M'),
            "end_time": turno.end_time.strftime('%H:%M'),
            "work_hours": turno.work_hours,
            "break_type": turno.break_type,
            "break_minutes": turno.break_minutes,
            "break_start": turno.break_start.strftime('%H:%M') if turno.break_start else "00:00",
            "break_end": turno.break_end.strftime('%H:%M') if turno.break_end else "00:00",
            "status": turno.status
        })

    elif request.method == "POST":
        form = ShiftForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": form.errors}, status=400)










def cambiar_estado_turno(request):
    if request.method == "POST":
        turno_id = request.POST.get("id")
        nuevo_estado = request.POST.get("estado")
        
        print("🛠 CAMBIO RECIBIDO")
        print(f"➡️ ID: {turno_id}")
        print(f"➡️ ESTADO: {nuevo_estado}")
        
        
        
        try:
            turno = AttShift.objects.get(id=turno_id)
            print(f"✅ Turno encontrado: {turno.shift_name}")
            turno.status = nuevo_estado
            turno.save()
            print(f"💾 Guardado: {turno.status}")
            return JsonResponse({"success": True})
        except AttShift.DoesNotExist:
            print("❌ Turno no encontrado")
            return JsonResponse({"success": False, "error": "Turno no encontrado"})
    print("❌ Método no permitido")    
    return JsonResponse({"success": False, "error": "Método no permitido"})

    






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
    
    
    

def detalle_grupo(request, id):
    try:
        grupo = HrGroup.objects.get(id=id)
        empleados = HrEmployee.objects.filter(emp_group=grupo)
        supervisores = GrupoSupervisor.objects.filter(grupo=grupo)

        data = {
            'grupo': grupo.nombre,
            'jefe_planta': f"{grupo.jefe_planta.emp_firstname} {grupo.jefe_planta.emp_lastname}" if grupo.jefe_planta else "No asignado",
            'supervisores': [f"{sup.supervisor.emp_firstname} {sup.supervisor.emp_lastname}" for sup in supervisores],
            'empleados': [f"{emp.emp_firstname} {emp.emp_lastname}" for emp in empleados],
        }

        return JsonResponse(data)
    except HrGroup.DoesNotExist:
        return JsonResponse({'error': 'Grupo no encontrado'}, status=404)   
    
    
    
@require_POST
def asignar_roles_grupo(request, id):
    grupo = get_object_or_404(HrGroup, id=id)

    jefe_id = request.POST.get('jefe_planta')
    supervisores_ids = request.POST.getlist('supervisores')

    # Verifica y asigna el jefe de planta
    if jefe_id:
        jefe = HrEmployee.objects.get(id=jefe_id)
        if jefe.emp_role.nombre.lower() == "jefe de área":  # ¡CORREGIDO!
            grupo.jefe_planta = jefe
            grupo.save()
        else:
            return JsonResponse({'error': 'El empleado seleccionado no tiene el rol de jefe de área'}, status=400)

    # Reemplaza los supervisores actuales por los nuevos
    GrupoSupervisor.objects.filter(grupo=grupo).delete()
    for sup_id in supervisores_ids:
        supervisor = HrEmployee.objects.get(id=sup_id)
        if supervisor.emp_role.nombre.lower() == "supervisor":
            GrupoSupervisor.objects.create(grupo=grupo, supervisor=supervisor)

    return JsonResponse({'success': True})


def grupos_view(request):
    print("🚨 ENTRÓ A grupos_view") 
    grupos = HrGroup.objects.all()

    # ✅ Aquí filtras por roles correctos
    empleados_jefes = HrEmployee.objects.filter(emp_role__nombre__iexact="Jefe de Área", emp_active=True)
    empleados_supervisores = HrEmployee.objects.filter(emp_role__nombre__iexact="Supervisor", emp_active=True)

    
    print("Jefes encontrados:", empleados_jefes)  # DEBUG
    print("Supervisores encontrados:", empleados_supervisores)  # DEBUG

    return render(request, "grupos.html", {
        "grupos": grupos,
        "empleados_jefes": empleados_jefes,
        "empleados_supervisores": empleados_supervisores,
    })
        
   
    

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
            ip_biometrico = request.POST.get("biometrico")  # 🔹 Ciudad seleccionada
            emp_pin = request.POST["emp_pin"]
            emp_nombre = request.POST["emp_firstname"]
            
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
            
              # 🔹 REGISTRAR EN EL BIOMÉTRICO
            if ip_biometrico:
                registrar_en_biometrico(emp_pin, emp_nombre, ip_biometrico)
            
            
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


# views.py
def cambiar_estado_empleado(request):
    if request.method == "POST":
        empleado_id = request.POST.get("id")
        nuevo_estado = request.POST.get("estado")

        try:
            empleado = HrEmployee.objects.get(id=empleado_id)
            empleado.emp_active = True if nuevo_estado == "Activo" else False
            empleado.save()
            return JsonResponse({"success": True})
        except HrEmployee.DoesNotExist:
            return JsonResponse({"success": False, "error": "Empleado no encontrado"})

    return JsonResponse({"success": False, "error": "Método no permitido"})






def obtener_empleado(request, id):
    empleado = get_object_or_404(HrEmployee, id=id)
    data = {
        "emp_pin": empleado.emp_pin,
        "emp_firstname": empleado.emp_firstname,
        "emp_lastname": empleado.emp_lastname,
        "emp_job": empleado.emp_job.id,
        "emp_group": empleado.emp_group.id,
        "emp_role": empleado.emp_role.id,
        "emp_cost_center": empleado.emp_cost_center.id,
        "emp_email": empleado.emp_email,
        "emp_active": empleado.emp_active,
    }
    return JsonResponse(data)




@csrf_exempt
def editar_empleado(request, id):
    if request.method == "POST":
        try:
            empleado = get_object_or_404(HrEmployee, id=id)

            # Actualiza datos del empleado
            empleado.emp_pin = request.POST.get("emp_pin")
            empleado.emp_firstname = request.POST.get("emp_firstname")
            empleado.emp_lastname = request.POST.get("emp_lastname")
            empleado.emp_email = request.POST.get("emp_email")
            empleado.emp_job_id = request.POST.get("emp_job")
            empleado.emp_group_id = request.POST.get("emp_group")
            empleado.emp_role_id = request.POST.get("emp_role")
            empleado.emp_cost_center_id = request.POST.get("emp_cost_center")
            empleado.emp_active = request.POST.get("emp_active") == "true"
            empleado.save()

            # ⏺️ Verifica si se quiere registrar en el biométrico
            ip_biometrico = request.POST.get("biometrico")
            if ip_biometrico:
                registrar_en_biometrico(empleado.emp_pin, empleado.emp_firstname, ip_biometrico)

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)







@csrf_exempt
def crear_cargo(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            EmpJob.objects.create(nombre=nombre)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def crear_rol(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            EmpRole.objects.create(nombre=nombre)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def crear_centro_costo(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            EmpCostCenter.objects.create(nombre=nombre)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)





# ================== REPORTES ==================
def reporte_turnos(request):
    asignaciones = EmpleadoTurno.objects.select_related('empleado', 'turno').all()
    return render(request, 'reportes/turnos.html', {'asignaciones': asignaciones})

def reportes_view(request):
    tipo = request.GET.get("tipo", "basico")
    cedula = request.GET.get("cedula")
    apellidos = request.GET.get("apellidos")
    grupo = request.GET.get("grupo")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    from API.utils.reportes import parse_fecha  # Evitamos import circular
    fecha_inicio = parse_fecha(desde)
    fecha_fin = parse_fecha(hasta)

    if hasattr(request.user, 'hremployee'):
        empleado = request.user.hremployee
        rol = empleado.emp_role.nombre.lower()

        if rol != 'administrador':
            # ✅ Listado de grupos que puede ver este usuario (como jefe o supervisor)
            grupos_jefe = HrGroup.objects.filter(jefe_planta=empleado).values_list('id', flat=True)
            grupos_supervisor = GrupoSupervisor.objects.filter(supervisor=empleado).values_list('grupo_id', flat=True)
            grupos_autorizados = set(grupos_jefe) | set(grupos_supervisor)

            # ❌ Si pidió un grupo que no le pertenece, lo bloqueamos
            if grupo and int(grupo) not in grupos_autorizados:
                return render(request, 'reportes.html', {'error': '❌ No tienes permiso para ver este grupo.'})

            # Si no se especificó grupo y tiene acceso a alguno, se lo asignamos automáticamente
            if not grupo and grupos_autorizados:
                grupo = list(grupos_autorizados)[0]
        
        

    filtros = {
        'apellidos': apellidos,
        'grupo': grupo,
        'cedula': cedula,
        'desde': fecha_inicio,
        'hasta': fecha_fin,
    }

    datos = generar_reporte_basico(filtros) if tipo == 'basico' else reporte_horas_extras(filtros)
    return render(request, 'reportes.html', {'datos': datos, 'tipo': tipo})


def ejecutar_procesamiento(request):
    hoy = datetime.now()
    hace_tres_dias = hoy - timedelta(days=3)

    FECHA_INICIO = make_aware(hace_tres_dias.replace(hour=0, minute=0, second=0))
    FECHA_FIN = make_aware(hoy.replace(hour=23, minute=59, second=59))

    procesar_marcaciones(FECHA_INICIO, FECHA_FIN)

    return redirect('reportes_view')  # 👈 asegúrate que el name en urls.py sea correcto

