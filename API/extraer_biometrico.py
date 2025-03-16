import os
import sys
import django
import csv
from zk import ZK
from datetime import datetime
from collections import defaultdict

# Configuración de Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# Configuración del biométrico
BIOMETRICO_IP = "192.168.0.211"
PUERTO = 4370

# Ruta para guardar el archivo en Documentos
ruta_documentos = os.path.join(os.path.expanduser("~"), "Documents", "registros_biometrico.csv")

def extraer_registros():
    zk = ZK(BIOMETRICO_IP, port=PUERTO, timeout=5)
    conn = None

    try:
        print("⏳ Conectando al biométrico...")
        conn = zk.connect()
        print("✅ Conectado al biométrico")

        # Obtener registros de asistencia
        registros = conn.get_attendance()
        if not registros:
            print("⚠ No hay registros en el biométrico.")
            return

        # Obtener la lista de usuarios registrados en el biométrico
        usuarios = conn.get_users()
        user_info = {u.uid: u.name for u in usuarios}  # Diccionario de ID -> Nombre

        # Organizar registros por usuario y fecha
        registros_por_usuario = defaultdict(list)
        for r in registros:
            fecha = r.timestamp.strftime('%Y-%m-%d')  # Extraer solo la fecha
            registros_por_usuario[(r.user_id, fecha)].append((r.timestamp, r.status))

        print("\n📊 **Registros de Entrada y Salida:**")
        registros_limpios = []

        for (user_id, fecha), registros in registros_por_usuario.items():
            registros.sort()  # Ordenar por tiempo
            entrada = None
            salida = None
            nombre_usuario = user_info.get(user_id, "Desconocido")  # Buscar nombre por user_id

            for timestamp, status in registros:
                if status == 1 and entrada is None:  # Primera entrada del día
                    entrada = timestamp
                elif status == 16 and entrada is not None:  # Primera salida después de una entrada
                    salida = timestamp
                    registros_limpios.append([user_id, nombre_usuario, fecha, entrada.strftime('%H:%M:%S'), salida.strftime('%H:%M:%S')])
                    entrada = None  # Reiniciar para la siguiente entrada/salida

            # Si al final del día no hay salida registrada, mostramos advertencia
            if entrada is not None and salida is None:
                registros_limpios.append([user_id, nombre_usuario, fecha, entrada.strftime('%H:%M:%S'), "FALTA SALIDA"])

        # Guardar en un archivo CSV dentro de "Documentos"
        with open(ruta_documentos, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "nombre", "fecha", "hora_entrada", "hora_salida"])  # Encabezado
            writer.writerows(registros_limpios)

        print(f"📂 Datos exportados a '{ruta_documentos}'")

    except Exception as e:
        print(f"❌ Error al conectar con el biométrico: {e}")

    finally:
        if conn:
            conn.disconnect()
            print("🔌 Desconectado del biométrico")

if __name__ == "__main__":
    extraer_registros()


