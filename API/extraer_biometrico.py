import os
import csv
from zk import ZK
from datetime import datetime

# Configuración del biométrico
BIOMETRICO_IP = "192.168.0.211"  # Ajusta la IP según tu configuración
PUERTO = 4370

# Ruta de guardado en la carpeta "Documentos" del usuario
ruta_documentos = os.path.join(os.path.expanduser("~"), "Documents", "registros_biometrico.csv")

# Conectar al biométrico
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
    else:
        # Guardar en un archivo CSV dentro de "Documentos"
        with open(ruta_documentos, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "timestamp", "status"])  # Encabezado

            for r in registros:
                writer.writerow([r.user_id, r.timestamp.strftime('%Y-%m-%d %H:%M:%S'), r.status])

        print(f"📂 Datos exportados a '{ruta_documentos}'")

except Exception as e:
    print(f"❌ Error al conectar con el biométrico: {e}")

finally:
    if conn:
        conn.disconnect()
        print("🔌 Desconectado del biométrico")
