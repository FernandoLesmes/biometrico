from datetime import datetime, time, timedelta
from API.models import AttShift


TURNOS = {
    1: {
        "nombre": "Turno 1",
        "hora_entrada_min": time(5, 0),
        "hora_entrada_max": time(6, 10),
        "hora_salida": time(14, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": True,
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": False,
            "festivas_diurnas": True,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
        "rango_horas_extra_diurnas": {
            "inicio": time(14, 0),
            "fin": time(18, 0),
            "tasa": 1.25
        }
    },
    2: {
        "nombre": "Turno 2",
        "hora_entrada_min": time(14, 0),
        "hora_entrada_max": time(14, 10),
        "hora_salida": time(22, 0),
        "horas_turno": 8,
        "sabados_horas_faltantes": 6,
        "resta_hora_almuerzo": False,
        "horas_totales_semanales": 46,
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": False,
            "festivas_diurnas": True,
            "festivas_nocturnas": True,
            "recargo_nocturno": True,
            "recargo_nocturno_festivo": False
        },
        "permite_horas_extra": True,
        "hora_extra_inicio": time(10, 0),
        "hora_extra_fin": time(13, 59),
        "tarifa_extra_diurna": 1.25,
        "rangos_horas_extra_diurna": [3.5, 3, 2.5, 2, 1.5, 1],
        "descontar_almuerzo_extra": True,
        "minutos_descuento_almuerzo": 30,
        "permite_extra_despues_turno": False,
        "tarifa_extra_nocturna": 1.75,
        "extra_festiva_diurna": {
            "tarifa": 2.0,
            "max_horas": 8
        },
        "extra_festiva_nocturna": {
            "tarifa": 2.5,
            "max_horas": 1
        },
        "recargo_nocturno": {
            "activo": True,
            "desde": time(21, 0),
            "hasta": time(22, 0),
            "tarifa": 0.35
        },
        "recargo_nocturno_festivo": {
            "activo": False,
            "tarifa": 2.1
        }
    },
    3: {
        "nombre": "Turno 3",
        "hora_entrada_min": time(22, 0),
        "hora_entrada_max": time(22, 10),
        "hora_salida": time(6, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": False,
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": True,
            "festivas_diurnas": True,
            "festivas_nocturnas": True,
            "recargo_nocturno": True,
            "recargo_nocturno_festivo": True
        },
        "rango_extras_diurnas": {
            "inicio": time(18, 0),
            "fin": time(21, 0),
            "maximo_horas": 3,
            "tasa": 1.25
        },
        "rango_extras_nocturnas": {
            "inicio": time(21, 0),
            "fin": time(22, 0),
            "tasa": 1.75
        },
        "rango_recargo_nocturno": {
            "inicio": time(22, 0),
            "fin": time(6, 0),
            "tasa": 0.35
        },
        "rango_recargo_nocturno_festivo": {
            "inicio": time(22, 0),
            "fin": time(6, 0),
            "tasa": 2.1
        },
        "logica_turno": {
            "entrada_dia_siguiente": True,
            "salida_dia_anterior": True
        }
    },
     4: {
        "nombre": "Turno 4",
        "hora_entrada_min": time(6, 0),
        "hora_entrada_max": time(7, 10),
        "hora_salida": time(16, 0),
        "horas_turno": 9,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": True,
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": False,
            "festivas_diurnas": True,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
    },
    5: {
        "nombre": "Turno 5",
        "hora_entrada_min": time(5, 0),
        "hora_entrada_max": time(6, 10),
        "hora_salida": time(15, 0),
        "horas_turno": 9,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": True,
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": False,
            "festivas_diurnas": True,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
    },
    6: {
        "nombre": "Turno 6",
        "hora_entrada_min": time(6, 0),
        "hora_entrada_max": time(7, 10),
        "hora_salida": time(15, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": True,
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": False,
            "festivas_diurnas": True,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
    },
    7: {
        "nombre": "Turno 7",
        "hora_entrada_min": time(14, 0),
        "hora_entrada_max": time(14, 10),
        "hora_salida": time(23, 0),
        "horas_turno": 9,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": False,
        "extras_posibles": {
            "diurnas": False,
            "nocturnas": True,
            "festivas_diurnas": False,
            "festivas_nocturnas": True,
            "recargo_nocturno": True,
            "recargo_nocturno_festivo": True
        },
    },
    8: {
        "nombre": "Turno 8",
        "hora_entrada_min": time(6, 0),
        "hora_entrada_max": time(7, 10),
        "hora_salida": time(17, 0),
        "horas_turno": 9,
        "autoriza_extra": False,
        "descuento_almuerzo_si_hay_extra": False,
        "extras_posibles": {
            "diurnas": False,
            "nocturnas": False,
            "festivas_diurnas": False,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
    },
    9: {
        "nombre": "Turno 9",
        "hora_entrada_min": time(6, 0),
        "hora_entrada_max": time(7, 10),
        "hora_salida": time(16, 0),
        "horas_turno": 9,
        "autoriza_extra": False,
        "descuento_almuerzo_si_hay_extra": False,
        "extras_posibles": {
            "diurnas": False,
            "nocturnas": False,
            "festivas_diurnas": False,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
    },
    10: {
        "nombre": "Turno 10",
        "hora_entrada_min": time(6, 0),
        "hora_entrada_max": time(7, 10),
        "hora_salida": time(14, 0),
        "horas_turno": 8,
        "autoriza_extra": False,
        "descuento_almuerzo_si_hay_extra": False,
        "extras_posibles": {
            "diurnas": False,
            "nocturnas": False,
            "festivas_diurnas": False,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
    },
} 


def detectar_turno(entrada, salida, grupo_nombre=None):
    entrada_time = entrada.time() if isinstance(entrada, datetime) else entrada
    salida_time = salida.time() if isinstance(salida, datetime) else salida
    grupo_nombre = grupo_nombre.lower() if grupo_nombre else ""

    for turno in TURNOS.values():
        entrada_min = turno['hora_entrada_min']
        entrada_max = turno['hora_entrada_max']
        salida_turno = turno['hora_salida']
        
        try:
            turno_db = AttShift.objects.get(shift_name=turno["nombre"])
            if turno_db.status != "Activo":
                continue  # ⚠️ Si está inactivo, no considerar este turno
        except AttShift.DoesNotExist:
            continue

        if grupo_nombre == "administradores" and turno.get("nombre") == "Turno 8":
            return turno

        if entrada_min > salida_turno:
            if entrada_time >= entrada_min or entrada_time <= salida_turno:
                return turno

        if entrada_min <= entrada_time <= entrada_max:
            return turno

        if turno.get("hora_extra_inicio") and turno.get("hora_extra_fin"):
            if turno["hora_extra_inicio"] <= entrada_time <= entrada_max:
                return turno

    return None


# ========================
# Turnos especiales (Turno 3)
# ========================

GRUPOS_TURNO_1 = [
    'producción bogotá 2-bogotá avenida 68',
    'producción bucaramanga 7-bucaramanga',
    'producción cali 5-cali'
]
GRUPOS_TURNO_2 = GRUPOS_TURNO_1


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
