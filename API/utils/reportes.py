
from collections import defaultdict
from datetime import datetime, timedelta, time
from django.db import transaction
from API.models import AttPunch, HrEmployee, EmpleadoTurno, AttShift
from API.utils.turnos import TURNOS, detectar_turno
from API.utils.festivos import es_festivo

# Grupos permitidos para turnos especiales
GRUPOS_TURNO_1 = [
    'producción bogotá 2-bogotá avenida 68',
    'producción bucaramanga 7-bucaramanga',
    'producción cali 5-cali'
]
GRUPOS_TURNO_2 = GRUPOS_TURNO_1

# 🔁 Lógica especializada para Turno 3 (nocturno cruzado de día)
def agrupar_marcaciones_3(marcaciones):
    bloques = []
    i = 0
    while i < len(marcaciones):
        entrada = marcaciones[i]
        print(f"🔍 Analizando entrada: {entrada}")
        
        for j in range(i+1, len(marcaciones)):
            salida = marcaciones[j]
            diferencia = salida - entrada
            print(f"    ↪️ Posible salida: {salida} | Diferencia: {diferencia}")

            if timedelta(hours=5) <= diferencia <= timedelta(hours=10):
                if entrada.time() >= time(20, 30) and salida.time() <= time(8, 30):
                    print(f"✅ Turno 3 detectado: Entrada {entrada} → Salida {salida}")
                    bloques.append((entrada, salida))
                    i = j + 1
                    break
        else:
            i += 1

    print(f"🔧 Total bloques detectados turno 3: {len(bloques)}")
    return bloques


@transaction.atomic
def procesar_marcaciones(fecha_inicio, fecha_fin):
    empleados = HrEmployee.objects.all()

    for empleado in empleados:
        grupo = getattr(empleado.emp_group, 'nombre', '').lower()
        if not grupo:
            continue

        # 🔍 Ampliamos el rango 1 día antes y después por Turno 3 cruzado
        marcaciones = AttPunch.objects.filter(
            employee=empleado,
            punch_time__range=[fecha_inicio - timedelta(days=1), fecha_fin + timedelta(days=1)]
        ).order_by('punch_time')

        if not marcaciones:
            continue

        marcaciones_list = list(marcaciones)
        fechas_turno_3 = set()

        # ==============================
        # 🕓 Turno 3 - Procesamiento nocturno cruzado
        # ==============================
        bloques_turno_3 = agrupar_marcaciones_3(marcaciones_list)
        for entrada, salida in bloques_turno_3:
            fecha = entrada.date()
            festivo = es_festivo(fecha)
            turno = detectar_turno(entrada.time(), salida.time(), grupo)

            if turno and turno["nombre"] == "Turno 3":
                fechas_turno_3.add(fecha)
                print(f"🌙 Turno 3 detectado: Entrada {entrada}, Salida {salida}")

                horas_base = turno["horas_turno"]
                horas_trabajadas = (salida - entrada).total_seconds() / 3600
                horas_extra = max(0, horas_trabajadas - horas_base)

                recargo = horas_base * turno["rango_recargo_nocturno"]["tasa"]
                recargo_festivo = horas_base * turno["rango_recargo_nocturno_festivo"]["tasa"]

                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": AttShift.objects.get(nombre="Turno 3"),
                        "hora_entrada": entrada,
                        "hora_salida": salida,
                        "festivo": festivo,
                        "horas_extras_diurnas": 0,
                        "horas_extras_nocturnas": horas_extra if not festivo else 0,
                        "horas_extras_festivas_diurnas": 0,
                        "horas_extras_festivas_nocturnas": horas_extra if festivo else 0,
                        "recargo_nocturno": recargo if not festivo else 0,
                        "recargo_nocturno_festivo": recargo_festivo if festivo else 0,
                        "aprobado_por_lider": False
                    }
                )

        # ==============================
        # 🕘 Turno 1 y Turno 2 - Procesamiento normal por día
        # ==============================
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
                print(f"❌ No se detectó turno para entrada: {entrada.time()} - salida: {salida.time()}")
                continue

            nombre_turno = turno["nombre"]
            print(f"✅ Detectado turno: {nombre_turno}")

            horas_base = turno["horas_turno"]
            descanso = timedelta(minutes=30) if turno.get("descuento_almuerzo_si_hay_extra") and salida > turno["hora_salida"] else timedelta()
            horas_trabajadas = (datetime.combine(fecha, salida.time()) - datetime.combine(fecha, entrada.time()) - descanso).total_seconds() / 3600
            horas_extra_total = max(0, horas_trabajadas - horas_base)

            if nombre_turno == "Turno 1":
                if grupo not in GRUPOS_TURNO_1:
                    continue

                EmpleadoTurno.objects.update_or_create(
                    empleado=empleado,
                    fecha=fecha,
                    defaults={
                        "turno": AttShift.objects.get(nombre="Turno 1"),
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

            elif nombre_turno == "Turno 2":
                if grupo not in GRUPOS_TURNO_2:
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
                        "turno": AttShift.objects.get(nombre="Turno 2"),
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
