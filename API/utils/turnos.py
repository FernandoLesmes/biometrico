# Completar definición de turnos 4 al 10 con base en la imagen proporcionada
from datetime import datetime,time
from datetime import time

TURNOS = {
    1: {
        "nombre": "Turno 1",
        "hora_entrada_min": time(5, 0),  # ✅ Puede llegar desde las 5:00 a.m.
        "hora_entrada_max": time(6, 10),  # ✅ Máxima tolerancia 6:10 a.m.
        "hora_salida": time(14, 0),
        "horas_turno": 8,
        "autoriza_extra": True,
        "descuento_almuerzo_si_hay_extra": True,  # ✅ Se descuenta 30 minutos de almuerzo si hace extras
        "extras_posibles": {
            "diurnas": True,
            "nocturnas": False,
            "festivas_diurnas": True,
            "festivas_nocturnas": False,
            "recargo_nocturno": False,
            "recargo_nocturno_festivo": False
        },
        "rango_horas_extra_diurnas": {  # Para futuras validaciones si las quieres implementar
            "inicio": time(14, 0),
            "fin": time(18, 0),
            "tasa": 1.25
        }
    },
    # Aquí luego vienen los turnos 2, 3, etc...

    2: {
    "nombre": "Turno 2",
    "hora_entrada_min": time(14, 0),        # 2:00 p.m.
    "hora_entrada_max": time(14, 10),       # 2:10 p.m.
    "hora_salida": time(22, 0),             # 10:00 p.m.
    "horas_turno": 8,
    
    "sabados_horas_faltantes": 6,
    "resta_hora_almuerzo": False,
    "horas_totales_semanales": 46,

    # 👇 ESTA ES LA CLAVE QUE TE FALTABA
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
         "diurnas": True,                   #// De 6pm a 9pm si llega antes
         "nocturnas": True,                #// De 9pm a 10pm si hace extras
         "festivas_diurnas": True,         #// 6pm a 9pm si es festivo
         "festivas_nocturnas": True,       #// De 10pm a 6am si es festivo
         "recargo_nocturno": True,         #// De 10pm a 6am en día normal
         "recargo_nocturno_festivo": True  #// Solo si el turno inicia en domingo/lunes festivo desde las 22h
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


   
   
       # 
    
    
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
        "horas_turno": 9,
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

#from ace_tools import display_json
#display_json(TURNOS, "TURNOS (estructura completa)")def detectar_turno(entrada, salida, grupo_nombre=None):
def detectar_turno(entrada, salida, grupo_nombre=None):
    entrada_time = entrada.time() if isinstance(entrada, datetime) else entrada
    salida_time = salida.time() if isinstance(salida, datetime) else salida
    
    # 🔐 Validar grupo permitido
    GRUPOS_TURNOS_PERMITIDOS = [
        'producción bogotá 2-bogotá avenida 68',
        'producción bucaramanga 7-bucaramanga',
        'producción cali 5-cali'
    ]
    if grupo_nombre and grupo_nombre.lower() not in GRUPOS_TURNOS_PERMITIDOS:
        #print(f"🚫 Grupo no autorizado para turnos: {grupo_nombre}")
        return None

    for turno_id, turno in TURNOS.items():
        entrada_min = turno['hora_entrada_min']
        entrada_max = turno['hora_entrada_max']
        salida_turno = turno['hora_salida']

        # Entrada anticipada válida
        if turno.get("hora_extra_inicio") and turno.get("hora_extra_fin"):
            if turno["hora_extra_inicio"] <= entrada_time <= entrada_max:
                #print(f"✅ Detectado turno (anticipado): {turno['nombre']}")
                return turno

        # Turnos normales o cruzados
        if entrada_min > salida_turno:
            if entrada_time >= entrada_min or entrada_time <= salida_turno:
                #print(f"✅ Detectado turno nocturno: {turno['nombre']}")
                return turno
        else:
            if entrada_min <= entrada_time <= entrada_max:
               # print(f"✅ Detectado turno: {turno['nombre']}")
                return turno

    #print(f"❌ No se detectó turno para entrada: {entrada_time}")
    return None

