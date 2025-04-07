# Completar definición de turnos 4 al 10 con base en la imagen proporcionada

TURNOS = {
    1: {
        "nombre": "Turno 1",
        "hora_entrada_min": time(6, 0),
        "hora_entrada_max": time(6, 15),
        "hora_salida": time(14, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": False,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    2: {
        "nombre": "Turno 2",
        "hora_entrada_min": time(14, 0),
        "hora_entrada_max": time(14, 15),
        "hora_salida": time(22, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": False, "nocturnas": True, "festivas_diurnas": False,
            "festivas_nocturnas": False, "recargo_nocturno": True, "recargo_nocturno_festivo": False
        }
    },
    3: {
        "nombre": "Turno 3",
        "hora_entrada_min": time(22, 0),
        "hora_entrada_max": time(22, 15),
        "hora_salida": time(6, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": True, "festivas_diurnas": True,
            "festivas_nocturnas": True, "recargo_nocturno": True, "recargo_nocturno_festivo": True
        }
    },
    4: {
        "nombre": "Turno 4",
        "hora_entrada_min": time(13, 0),
        "hora_entrada_max": time(13, 15),
        "hora_salida": time(21, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": True,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    5: {
        "nombre": "Turno 5",
        "hora_entrada_min": time(7, 0),
        "hora_entrada_max": time(7, 15),
        "hora_salida": time(16, 0),
        "horas_turno": 9,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": True,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    6: {
        "nombre": "Turno 6",
        "hora_entrada_min": time(8, 0),
        "hora_entrada_max": time(8, 15),
        "hora_salida": time(17, 0),
        "horas_turno": 9,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": True,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    7: {
        "nombre": "Turno 7",
        "hora_entrada_min": time(9, 0),
        "hora_entrada_max": time(9, 15),
        "hora_salida": time(18, 0),
        "horas_turno": 9,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": True,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    8: {
        "nombre": "Turno 8",
        "hora_entrada_min": time(7, 0),
        "hora_entrada_max": time(7, 15),
        "hora_salida": time(17, 0),
        "horas_turno": 10,
        "autoriza_extra": False,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": False,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    9: {
        "nombre": "Turno 9",
        "hora_entrada_min": time(6, 30),
        "hora_entrada_max": time(6, 45),
        "hora_salida": time(15, 30),
        "horas_turno": 9,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": True,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    },
    10: {
        "nombre": "Turno 10",
        "hora_entrada_min": time(7, 0),
        "hora_entrada_max": time(7, 15),
        "hora_salida": time(15, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "extras_posibles": {
            "diurnas": True, "nocturnas": False, "festivas_diurnas": False,
            "festivas_nocturnas": False, "recargo_nocturno": False, "recargo_nocturno_festivo": False
        }
    }
}

from ace_tools import display_json
display_json(TURNOS, "TURNOS (estructura completa)")
