from collections import defaultdict
from datetime import datetime, timedelta, time
from django.db import transaction
from django.shortcuts import render

from API.models import HrEmployee, HrGroup, AttPunch, EmpleadoTurno, AttShift
from API.utils.turnos import TURNOS, detectar_turno
from API.utils.festivos import es_festivo

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
def generar_reporte_basico(filtros):
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


# ========================
# ✅ Reporte de horas extras
# ========================
def reporte_horas_extras(filtros):
    datos = []
    registros = EmpleadoTurno.objects.select_related('empleado', 'turno')

    if filtros.get('cedula'):
        registros = registros.filter(empleado__emp_pin__icontains=filtros['cedula'])
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
def reportes_view(request):
    tipo = request.GET.get("tipo", "basico")
    cedula = request.GET.get("cedula")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    fecha_inicio = parse_fecha(desde)
    fecha_fin = parse_fecha(hasta)

    if fecha_inicio and fecha_fin:
        procesar_marcaciones(fecha_inicio, fecha_fin)

    filtros = {
        'cedula': cedula,
        'desde': fecha_inicio,
        'hasta': fecha_fin,
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
            if timedelta(hours=5) <= diferencia <= timedelta(hours=10):
                if entrada.time() >= time(20, 30) and salida.time() <= time(8, 30):
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
    empleados = HrEmployee.objects.all()

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

        marcaciones_list = list(marcaciones)
        fechas_turno_3 = set()

        bloques_turno_3 = agrupar_marcaciones_3(marcaciones_list)

        for entrada, salida in bloques_turno_3:
            fecha = salida.date()  # Turno 3 cruza de día, la fecha debe ser la de salida
            festivo = es_festivo(fecha)
            turno = detectar_turno(entrada.time(), salida.time(), grupo)

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
                        "turno": AttShift.objects.get(shift_name="Turno 3"),
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
                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": AttShift.objects.get(shift_name="Turno 1"),
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
                        "turno": AttShift.objects.get(shift_name="Turno 2"),
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
