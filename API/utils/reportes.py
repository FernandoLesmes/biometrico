from collections import defaultdict
from datetime import datetime, timedelta, time
from django.db import transaction
from django.shortcuts import render

from API.models import HrEmployee, HrGroup, AttPunch, EmpleadoTurno, AttShift
from API.utils.turnos import TURNOS, detectar_turno
from API.utils.festivos import es_festivo
from django.utils.timezone import now
from django.utils.timezone import make_aware

#from turnos import detectar_turno, agrupar_marcaciones_3, GRUPOS_TURNO_1, GRUPOS_TURNO_2



# ========================
# ✅ Función para parsear fechas
# ========================
def parse_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str.strip().rstrip('-'), "%Y-%m-%d").date()
    except Exception:
        return None


# ========================
# ✅ Reporte de asistencia básica
# ========================
from API.models import EmpleadoTurno  # Asegúrate de importarlo

def generar_reporte_basico(filtros):
    datos = []
    punches = AttPunch.objects.select_related('employee').order_by('punch_time')

    if filtros.get('cedula'):
        punches = punches.filter(employee__emp_pin__icontains=filtros['cedula'])

    if filtros.get("apellidos"):
        punches = punches.filter(employee__emp_lastname__icontains=filtros["apellidos"])

    if filtros.get("grupo"):
        punches = punches.filter(employee__emp_group_id=filtros["grupo"])

    punches = punches.filter(employee__emp_active=True)

    if filtros.get('desde'):
        punches = punches.filter(punch_time__date__gte=filtros['desde'])

    if filtros.get('hasta'):
        punches = punches.filter(punch_time__date__lte=filtros['hasta'])

    agrupado = defaultdict(lambda: defaultdict(list))
    for p in punches:
        empleado = p.employee
        fecha = p.punch_time.date()
        agrupado[empleado][fecha].append(p.punch_time)

    for empleado, dias in agrupado.items():
        grupo = empleado.emp_group.nombre.lower() if empleado.emp_group else ''
        for fecha, marcas in dias.items():
            marcas_ordenadas = sorted(marcas)
            entrada = marcas_ordenadas[0].time()
            salida = marcas_ordenadas[-1].time() if len(marcas_ordenadas) > 1 else None
            turno = detectar_turno(entrada, salida, grupo) if salida else None

            datos.append({
                'cedula': empleado.emp_pin,
                'nombre': empleado.emp_firstname,
                'apellidos': empleado.emp_lastname,
                'grupo': empleado.emp_group.nombre if empleado.emp_group else '',
                'fecha': fecha,
                'turno': turno["nombre"] if turno else '',
                'entradas_salidas': marcas_ordenadas
            })

    return datos






# ========================
# ✅ Reporte de horas extras
# ========================
def reporte_horas_extras(filtros):
    datos = []
    registros = EmpleadoTurno.objects.select_related('empleado', 'turno', 'empleado__emp_group')

    if filtros.get('cedula'):
        registros = registros.filter(empleado__emp_pin__icontains=filtros['cedula'])

    if filtros.get('apellidos'):
        registros = registros.filter(empleado__emp_lastname__icontains=filtros['apellidos'])

    if filtros.get('grupo'):
        registros = registros.filter(empleado__emp_group_id=filtros['grupo'])

    registros = registros.filter(empleado__emp_active=True)

    if filtros.get('desde'):
        registros = registros.filter(fecha__gte=filtros['desde'])

    if filtros.get('hasta'):
        registros = registros.filter(fecha__lte=filtros['hasta'])

    for r in registros:
        datos.append({
            'cedula': r.empleado.emp_pin,
            'nombre': r.empleado.emp_firstname,
            'apellidos': r.empleado.emp_lastname,
            'grupo': r.empleado.emp_group.nombre if r.empleado.emp_group else '',
            'fecha': r.fecha,
            'turno': r.turno.shift_name,
            'entrada': r.hora_entrada,
            'salida': r.hora_salida,
            'horas_extras_diurnas': r.horas_extras_diurnas,
            'horas_extras_nocturnas': r.horas_extras_nocturnas,
            'horas_extras_festivas_diurnas': r.horas_extras_festivas_diurnas,
            'horas_extras_festivas_nocturnas': r.horas_extras_festivas_nocturnas,
            'recargo_nocturno': r.recargo_nocturno,
            'recargo_nocturno_festivo': r.recargo_nocturno_festivo,
            'aprobado': r.aprobado_por_lider
        })

    return datos




# ========================
# ✅ Vista de reportes (unificada)
# ========================


# ========================
# ✅ Turnos especiales (Turno 3)
# ========================
GRUPOS_TURNO_1 = [
    'producción bogotá 2-bogotá avenida 68',
    'producción bucaramanga 7-bucaramanga',
    'producción cali 5-cali'
]
GRUPOS_TURNO_2 = GRUPOS_TURNO_1
GRUPOS_TURNO_4 = GRUPOS_TURNO_1


def agrupar_marcaciones_3(marcaciones):
    bloques = []
    i = 0
    while i < len(marcaciones):
        entrada = marcaciones[i].punch_time
        for j in range(i + 1, len(marcaciones)):
            salida = marcaciones[j].punch_time
            diferencia = salida - entrada

            dia_salida = salida.date()
            dia_semana = salida.weekday()  # 0 = lunes, 6 = domingo
            es_viernes_o_sabado = dia_semana in [4, 5]  # 4 = viernes, 5 = sábado

            if (
                time(17, 0) <= entrada.time() <= time(22, 10) and
                diferencia >= timedelta(hours=6) and
                diferencia <= timedelta(hours=12) and
                (
                    (not es_viernes_o_sabado and time(5, 0) <= salida.time() <= time(8, 30)) or
                    (es_viernes_o_sabado and salida.time() >= time(5, 0))
                )
            ):
                bloques.append((entrada, salida))
                i = j + 1
                break
        else:
            i += 1
    return bloques



# ========================
# ✅ Procesamiento general de marcaciones
# ========================
@transaction.atomic
def procesar_marcaciones(fecha_inicio, fecha_fin):
    primer_punch = AttPunch.objects.earliest("punch_time").punch_time
    ultimo_punch = AttPunch.objects.latest("punch_time").punch_time
    fecha_inicio = primer_punch.date()
    fecha_fin = ultimo_punch.date()
    
    print(f"📅 Procesando desde {fecha_inicio} hasta {fecha_fin}")
    empleados = HrEmployee.objects.filter(emp_active=True)


    for empleado in empleados:
        grupo = getattr(empleado.emp_group, 'nombre', '').lower()
        if not grupo:
            continue

        marcaciones = AttPunch.objects.filter(
            employee=empleado,
            punch_time__range=[fecha_inicio - timedelta(days=1), fecha_fin + timedelta(days=1)]
        ).order_by('punch_time')

        if not marcaciones:
            continue

        marcaciones_list = list(marcaciones)  # queryset con objetos AttPunch
        fechas_turno_3 = set()

        bloques_turno_3 = agrupar_marcaciones_3(marcaciones_list)
        for entrada, salida in bloques_turno_3:
            fecha = salida.date()  # Turno 3 cruza de día, la fecha debe ser la de salida
            festivo = es_festivo(fecha)
            turno = detectar_turno(entrada.time(), salida.time(), grupo)
            
            
            #aca es parta no asigana rturno si este esat inactivo
            
            if not turno:
                continue  # si no se detectó ningún turno

                    # Validar si el turno está activo en la base de datos
            turno_db = AttShift.objects.filter(shift_name=turno["nombre"], status="Activo").first()
            if not turno_db:
                continue  # ❌ no se asigna turno si está inactivo

            

            if turno and turno["nombre"] == "Turno 3":
                fechas_turno_3.add(fecha)

                horas_base = turno["horas_turno"]
                horas_trabajadas = (salida - entrada).total_seconds() / 3600
                horas_extra = max(0, horas_trabajadas - horas_base)

                horas_extra_diurna = 0
                if entrada.time() < time(18, 0):
                    horas_extra_diurna = (datetime.combine(fecha, time(22, 0)) - datetime.combine(fecha - timedelta(days=1), entrada.time())).total_seconds() / 3600

                recargo = horas_base * turno["rango_recargo_nocturno"]["tasa"]
                recargo_festivo = horas_base * turno["rango_recargo_nocturno_festivo"]["tasa"]

                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": turno_db, # aca se replazo la linea "turno": AttShift.objects.get(shift_name="Turno 3"), por la q esta ahora  lo mismo par alos demas 
 
                        "hora_entrada": entrada,
                        "hora_salida": salida,
                        "festivo": festivo,
                        "horas_extras_diurnas": horas_extra_diurna if not festivo else 0,
                        "horas_extras_festivas_diurnas": horas_extra_diurna if festivo else 0,
                        "horas_extras_nocturnas": horas_extra if not festivo else 0,
                        "horas_extras_festivas_nocturnas": horas_extra if festivo else 0,
                        "recargo_nocturno": recargo if not festivo else 0,
                        "recargo_nocturno_festivo": recargo_festivo if festivo else 0,
                        "aprobado_por_lider": False
                    }
                )

        dias = defaultdict(list)
        for m in marcaciones_list:
            f = m.punch_time.date()
            if f not in fechas_turno_3:
                dias[f].append(m.punch_time)
                
                
                
                

        for fecha, marcas in dias.items():
            if len(marcas) < 2:
                continue

            entrada = marcas[0]
            salida = marcas[-1]
            festivo = es_festivo(fecha)

            turno = detectar_turno(entrada.time(), salida.time(), grupo)
            if not turno:
                
            
                continue

            nombre_turno = turno["nombre"]
            horas_base = turno["horas_turno"]
            descanso = timedelta(minutes=30) if turno.get("descuento_almuerzo_si_hay_extra") and salida.time() > turno["hora_salida"] else timedelta()
            horas_trabajadas = (datetime.combine(fecha, salida.time()) - datetime.combine(fecha, entrada.time()) - descanso).total_seconds() / 3600
            horas_extra_total = max(0, horas_trabajadas - horas_base)

            if nombre_turno == "Turno 1" and grupo in GRUPOS_TURNO_1:
                turno_db = AttShift.objects.filter(shift_name=nombre_turno, status="Activo").first()
                if not turno_db:
                    continue
                
                
                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": turno_db,
                        "hora_entrada": entrada,
                        "hora_salida": salida,
                        "festivo": festivo,
                        "horas_extras_diurnas": horas_extra_total if not festivo else 0,
                        "horas_extras_festivas_diurnas": horas_extra_total if festivo else 0,
                        "horas_extras_nocturnas": 0,
                        "horas_extras_festivas_nocturnas": 0,
                        "recargo_nocturno": 0,
                        "recargo_nocturno_festivo": 0,
                        "aprobado_por_lider": False
                    }
                )

            elif nombre_turno == "Turno 2" and grupo in GRUPOS_TURNO_2:
                
                turno_db = AttShift.objects.filter(shift_name=nombre_turno, status="Activo").first()
                if not turno_db:
                    continue
                
                horas_extras_diurnas = 0
                if entrada.time() < turno["hora_entrada_min"]:
                    tiempo_extra_antes = (datetime.combine(fecha, turno["hora_entrada_min"]) - datetime.combine(fecha, entrada.time())).total_seconds() / 3600
                    horas_extras_diurnas = min(tiempo_extra_antes, max(turno.get("rangos_horas_extra_diurna", [0])))

                recargo_nocturno = 1 if time(21, 0) <= salida.time() <= time(22, 0) else 0
                recargo_nocturno_festivo = 1 if festivo and recargo_nocturno else 0

                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": turno_db,
                        "hora_entrada": entrada,
                        "hora_salida": salida,
                        "festivo": festivo,
                        "horas_extras_diurnas": horas_extras_diurnas if not festivo else 0,
                        "horas_extras_festivas_diurnas": horas_extras_diurnas if festivo else 0,
                        "horas_extras_nocturnas": 0,
                        "horas_extras_festivas_nocturnas": 0,
                        "recargo_nocturno": recargo_nocturno if not festivo else 0,
                        "recargo_nocturno_festivo": recargo_nocturno_festivo,
                        "aprobado_por_lider": False
                    }
                )

            else:
                # ✅ Cualquier otro turno (Turno 4 al 10, administrativos, etc.)
                
                # ✅ Para otros turnos, validar si están activos antes
                turno_db = AttShift.objects.filter(shift_name=nombre_turno, status="Activo").first()
                if not turno_db:
                    continue 
                
                
                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": turno_db,
                        "hora_entrada": entrada,
                        "hora_salida": salida,
                        "festivo": festivo,
                        "horas_extras_diurnas": 0,
                        "horas_extras_festivas_diurnas": 0,
                        "horas_extras_nocturnas": 0,
                        "horas_extras_festivas_nocturnas": 0,
                        "recargo_nocturno": 0,
                        "recargo_nocturno_festivo": 0,
                        "aprobado_por_lider": False
                    }
                )
                     # ✅ Registro de asistencia sin salida (empleado aún en empresa)
    
       