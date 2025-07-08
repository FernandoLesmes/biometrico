from collections import defaultdict
from datetime import datetime, timedelta, time, date
from django.db import transaction
from django.db.models import Q

from django.shortcuts import render

from API.models import HrEmployee, HrGroup, AttPunch, EmpleadoTurno, AttShift
from API.utils.turnos import TURNOS, detectar_turno
from API.utils.festivos import es_festivo
from django.utils.timezone import make_aware, get_current_timezone


# ========================
# ✅ Grupos rotativos (requieren lógica completa con Turno 3)
# ========================
GRUPOS_ROTATIVOS = [
    # Producción
    'producción bogotá 2-bogotá avenida 68',
    'producción bucaramanga 7-bucaramanga',
    'producción cali 5-cali',

    # Mantenimiento
    'mantenimiento 2-bogotá avenida 68',
    'mantenimiento 5-cali',
    'mantenimiento 7-bucaramanga',

    # Almacenamiento y Distribución
    'almacenamiento y distribución bogotá 2-bogotá avenida 68',
    'almacenamiento y distribución bucaramanga 7-bucaramanga',
    'almacenamiento y distribución cali 5-cali',
]

GRUPOS_TURNO_1 = [
    'producción bogotá 2-bogotá avenida 68',
    'producción bucaramanga 7-bucaramanga',
    'producción cali 5-cali'
]
GRUPOS_TURNO_2 = GRUPOS_TURNO_1


# ========================
# ✅ Función para parsear fechas
# ========================
def parse_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str.strip().rstrip('-'), "%Y-%m-%d").date()
    except Exception:
        return None


# ========================
# ✅ Turnos especiales (Turno 3)
# ========================
def agrupar_marcaciones_3(marcaciones):
    bloques = []
    i = 0
    while i < len(marcaciones):
        entrada = marcaciones[i].punch_time
        for j in range(i + 1, len(marcaciones)):
            salida = marcaciones[j].punch_time
            diferencia = salida - entrada

            dia_semana = salida.weekday()
            es_viernes_o_sabado = dia_semana in [4, 5]

            if (
                time(17, 0) <= entrada.time() <= time(22, 10) and
                timedelta(hours=6) <= diferencia <= timedelta(hours=12) and
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
# ✅ Reporte de asistencia básica
# ========================
def generar_reporte_basico(filtros):
    datos = []
    punches = AttPunch.objects.select_related('employee').order_by('punch_time')

    if filtros.get("buscar"):
        q = filtros["buscar"]
        punches = punches.filter(
            Q(employee__emp_pin__icontains=q) |
            Q(employee__emp_lastname__icontains=q)
        )

    if filtros.get("grupo"):
        if isinstance(filtros["grupo"], list):
            punches = punches.filter(employee__emp_group_id__in=filtros["grupo"])
        else:
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

    for empleado in agrupado:
        grupo = empleado.emp_group.nombre.lower() if empleado.emp_group else ''
        dias = agrupado[empleado]
        fechas = sorted(dias.keys())

        fechas_usadas_como_entrada_de_turno3 = set()

        resultados_temporales = []
        for fecha in fechas:
            marcas_actual = dias[fecha]
            marcas_anteriores = dias.get(fecha - timedelta(days=1), [])
            todas_marcas = sorted(marcas_anteriores + marcas_actual)

            fake_punches = [
                type('Punch', (), {'punch_time': m})
                for m in todas_marcas
            ]

            bloques_turno_3 = agrupar_marcaciones_3(fake_punches)
            turno_nombre = ''
            entradas_salidas = []

            for entrada, salida in bloques_turno_3:
                if salida.date() == fecha:
                    turno_nombre = "Turno 3"
                    entradas_salidas = [entrada, salida]
                    fechas_usadas_como_entrada_de_turno3.add(entrada.date())
                    break

            resultados_temporales.append({
                'fecha': fecha,
                'turno': turno_nombre,
                'entradas_salidas': entradas_salidas,
                'marcas_actual': sorted(marcas_actual)
            })

        for r in resultados_temporales:
            fecha = r['fecha']
            turno_nombre = r['turno']
            entradas_salidas = r['entradas_salidas']
            marcas_actual = r['marcas_actual']

            if turno_nombre == "Turno 3":
                datos.append({
                    'cedula': empleado.emp_pin,
                    'nombre': empleado.emp_firstname,
                    'apellidos': empleado.emp_lastname,
                    'grupo': empleado.emp_group.nombre if empleado.emp_group else '',
                    'fecha': fecha,
                    'turno': turno_nombre,
                    'entradas_salidas': entradas_salidas
                })
            else:
                if fecha in fechas_usadas_como_entrada_de_turno3 and len(marcas_actual) == 1:
                    continue

                if len(marcas_actual) >= 2:
                    entrada = marcas_actual[0].time()
                    salida = marcas_actual[-1].time()
                    turno = detectar_turno(entrada, salida, grupo)
                    turno_nombre = turno["nombre"] if turno else ''
                else:
                    turno_nombre = ''

                datos.append({
                    'cedula': empleado.emp_pin,
                    'nombre': empleado.emp_firstname,
                    'apellidos': empleado.emp_lastname,
                    'grupo': empleado.emp_group.nombre if empleado.emp_group else '',
                    'fecha': fecha,
                    'turno': turno_nombre,
                    'entradas_salidas': marcas_actual
                })

    return datos


# ========================
# ✅ Reporte de horas extras
# ========================
def reporte_horas_extras(filtros):
    datos = []
    registros = EmpleadoTurno.objects.select_related('empleado', 'turno', 'empleado__emp_group')

    if filtros.get("buscar"):
        q = filtros["buscar"]
        registros = registros.filter(
            Q(empleado__emp_pin__icontains=q) |
            Q(empleado__emp_lastname__icontains=q)
        )

    if filtros.get('grupo'):
        if isinstance(filtros["grupo"], list):
            registros = registros.filter(empleado__emp_group_id__in=filtros['grupo'])
        else:
            registros = registros.filter(empleado__emp_group_id=filtros['grupo'])

    registros = registros.filter(empleado__emp_active=True)

    if filtros.get('desde'):
        registros = registros.filter(fecha__gte=filtros['desde'])

    if filtros.get('hasta'):
        registros = registros.filter(fecha__lte=filtros['hasta'])

    for r in registros:
        datos.append({
            'id': r.id,
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
            'aprobado_supervisor': r.aprobado_supervisor,
            'aprobado_jefe_area': r.aprobado_jefe_area,
        })

    return datos
# ========================
# ✅ Procesamiento general de marcaciones
# ========================
def aware(dt):
    if dt.tzinfo is None:
        return make_aware(dt, get_current_timezone())
    return dt


@transaction.atomic
def procesar_marcaciones(fecha_inicio=None, fecha_fin=None):
    if not fecha_inicio or not fecha_fin:
        fecha_fin = date.today()
        fecha_inicio = fecha_fin - timedelta(days=30)
    else:
        if hasattr(fecha_inicio, "date"):
            fecha_inicio = fecha_inicio.date()
        if hasattr(fecha_fin, "date"):
            fecha_fin = fecha_fin.date()

    print(f"📅 Procesando del {fecha_inicio} al {fecha_fin}")

    empleados = HrEmployee.objects.filter(emp_active=True)

    for empleado in empleados:
        grupo = getattr(empleado.emp_group, 'nombre', '').lower()
        if not grupo:
            continue

        fecha_inicio_query = fecha_inicio - timedelta(days=1)

        marcaciones = AttPunch.objects.filter(
            employee=empleado,
            punch_time__date__range=[fecha_inicio_query, fecha_fin]
        ).order_by('punch_time')

        if not marcaciones:
            continue

        marcaciones_list = list(marcaciones)

        # 💠 ➜ ✅ Turno 3 primero (solo para grupos rotativos)
        fechas_turno_3 = set()
        if grupo in GRUPOS_ROTATIVOS:
            bloques_turno_3 = agrupar_marcaciones_3(marcaciones_list)
            for entrada, salida in bloques_turno_3:
                if entrada.date() != salida.date():
                    fin_dia_entrada = aware(datetime.combine(entrada.date(), time(23, 59, 59)))
                    horas_en_entrada_dia = (min(fin_dia_entrada, salida) - entrada).total_seconds() / 3600
                    if horas_en_entrada_dia < 0:
                        horas_en_entrada_dia = 0

                    inicio_dia_salida = aware(datetime.combine(salida.date(), time(0, 0, 0)))
                    horas_en_salida_dia = (salida - max(inicio_dia_salida, entrada)).total_seconds() / 3600
                    if horas_en_salida_dia < 0:
                        horas_en_salida_dia = 0

                    fecha = salida.date() if horas_en_salida_dia >= horas_en_entrada_dia else entrada.date()

                    if not (fecha_inicio <= fecha <= fecha_fin):
                        continue

                    festivo = es_festivo(fecha)
                    turno_db = AttShift.objects.filter(shift_name="Turno 3", status="Activo").first()
                    if not turno_db:
                        continue

                    fechas_turno_3.add(fecha)

                    horas_base = 8
                    horas_trabajadas = (salida - entrada).total_seconds() / 3600
                    horas_extra = max(0, horas_trabajadas - horas_base)

                    horas_extra_diurna = 0
                    if entrada.time() < time(18, 0):
                        horas_extra_diurna = (
                            datetime.combine(fecha, time(22, 0)) -
                            datetime.combine(fecha - timedelta(days=1), entrada.time())
                        ).total_seconds() / 3600

                    turno_existente = EmpleadoTurno.objects.filter(empleado=empleado, fecha=fecha).first()
                    datos = {
                        "turno": turno_db,
                        "hora_entrada": entrada,
                        "hora_salida": salida,
                        "festivo": festivo,
                        "horas_extras_diurnas": horas_extra_diurna if not festivo else 0,
                        "horas_extras_festivas_diurnas": horas_extra_diurna if festivo else 0,
                        "horas_extras_nocturnas": horas_extra if not festivo else 0,
                        "horas_extras_festivas_nocturnas": horas_extra if festivo else 0,
                        "recargo_nocturno": 0,
                        "recargo_nocturno_festivo": 0,
                        "aprobado_supervisor": turno_existente.aprobado_supervisor if turno_existente else False,
                        "aprobado_jefe_area": turno_existente.aprobado_jefe_area if turno_existente else False,
                    }

                    EmpleadoTurno.objects.update_or_create(
                        empleado=empleado,
                        fecha=fecha,
                        defaults=datos
                    )

        # 💠 ➜ ✅ Procesar días normales (tanto administrativos como rotativos)
        dias = defaultdict(list)
        for m in marcaciones_list:
            f = m.punch_time.date()
            if f not in fechas_turno_3 and (fecha_inicio <= f <= fecha_fin):
                dias[f].append(m.punch_time)

        for fecha, marcas in dias.items():
            marcas.sort()
            if len(marcas) < 2:
                continue

            # 💡 Aquí se parte en BLOQUES de pares Entrada/Salida
            for i in range(0, len(marcas) - 1, 2):
                entrada = marcas[i]
                salida = marcas[i + 1]

                festivo = es_festivo(fecha)
                turno = detectar_turno(entrada.time(), salida.time(), grupo)
                if not turno:
                    continue

                nombre_turno = turno["nombre"]
                horas_base = turno["horas_turno"]

                descanso = timedelta()
                if not festivo and turno.get("descuento_almuerzo_si_hay_extra") and salida.time() > turno["hora_salida"]:
                    descanso = timedelta(minutes=30)

                horas_trabajadas = (
                    datetime.combine(fecha, salida.time()) -
                    datetime.combine(fecha, entrada.time()) -
                    descanso
                ).total_seconds() / 3600

                horas_extra_total = horas_trabajadas if festivo else max(0, horas_trabajadas - horas_base)

                turno_db = AttShift.objects.filter(shift_name=nombre_turno, status="Activo").first()
                if not turno_db:
                    continue

                datos_base = {
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
                }

                if nombre_turno == "Turno 1" and grupo in GRUPOS_TURNO_1:
                    datos_base["horas_extras_diurnas"] = horas_extra_total if not festivo else 0
                    datos_base["horas_extras_festivas_diurnas"] = horas_extra_total if festivo else 0

                elif nombre_turno == "Turno 2" and grupo in GRUPOS_TURNO_2:
                    if festivo:
                        entrada_dt = datetime.combine(fecha, entrada.time())
                        salida_dt = datetime.combine(fecha, salida.time())

                        festiva_diurna_inicio = datetime.combine(fecha, time(14, 0))
                        festiva_diurna_fin = datetime.combine(fecha, time(19, 0))
                        festiva_nocturna_inicio = datetime.combine(fecha, time(19, 0))
                        festiva_nocturna_fin = datetime.combine(fecha, time(22, 0))

                        inter_diurna_inicio = max(entrada_dt, festiva_diurna_inicio)
                        inter_diurna_fin = min(salida_dt, festiva_diurna_fin)
                        if inter_diurna_inicio < inter_diurna_fin:
                            horas_diurnas = (inter_diurna_fin - inter_diurna_inicio).total_seconds() / 3600
                            datos_base["horas_extras_festivas_diurnas"] = round(horas_diurnas, 2)

                        inter_nocturna_inicio = max(entrada_dt, festiva_nocturna_inicio)
                        inter_nocturna_fin = min(salida_dt, festiva_nocturna_fin)
                        if inter_nocturna_inicio < inter_nocturna_fin:
                            horas_nocturnas = (inter_nocturna_fin - inter_nocturna_inicio).total_seconds() / 3600
                            datos_base["horas_extras_festivas_nocturnas"] = round(horas_nocturnas, 2)
                    else:
                        if entrada.time() < turno["hora_entrada_min"]:
                            tiempo_extra = (
                                datetime.combine(fecha, turno["hora_entrada_min"]) -
                                datetime.combine(fecha, entrada.time())
                            ).total_seconds() / 3600
                            datos_base["horas_extras_diurnas"] = min(
                                tiempo_extra, max(turno.get("rangos_horas_extra_diurna", [0]))
                            )

                        if salida.time() > time(19, 0):
                            recargo_inicio = max(entrada.time(), time(19, 0))
                            recargo_fin = min(salida.time(), time(22, 0))
                            if recargo_inicio < recargo_fin:
                                recargo_horas = (
                                    datetime.combine(fecha, recargo_fin) -
                                    datetime.combine(fecha, recargo_inicio)
                                ).total_seconds() / 3600
                                datos_base["recargo_nocturno"] = round(recargo_horas, 2)

                turno_existente = EmpleadoTurno.objects.filter(empleado=empleado, fecha=fecha).first()
                datos_base["aprobado_supervisor"] = turno_existente.aprobado_supervisor if turno_existente else False
                datos_base["aprobado_jefe_area"] = turno_existente.aprobado_jefe_area if turno_existente else False

                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults=datos_base
                )
