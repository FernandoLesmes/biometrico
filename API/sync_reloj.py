from zk import ZK
import os
import sys
from datetime import datetime
from django.utils.timezone import make_aware

# Añadir la raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ Configurar entorno Django antes de importarlo
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from API.models import HrEmployee, AttPunch
from django.db.models import Max

# ===============================
# 🔍 Función para obtener última fecha por terminal
# ===============================
def obtener_ultima_fecha_terminal(nombre_terminal):
    ultima = AttPunch.objects.filter(terminal_id=nombre_terminal).aggregate(Max("punch_time"))["punch_time__max"]
    if ultima:
        return ultima
    else:
        return make_aware(datetime(2024, 1, 1, 0, 0, 0))  # Fecha base si no hay registros

# ===============================
# 🔄 Sincronizar un dispositivo
# ===============================
def sincronizar_dispositivo(ip, nombre_terminal):
    print(f"📡 Conectando a {nombre_terminal} ({ip})...")
    zk = ZK(ip, port=4370, timeout=10)
    conn = None
    fecha_minima = obtener_ultima_fecha_terminal(nombre_terminal)

    try:
        conn = zk.connect()
        conn.disable_device()

        registros = conn.get_attendance()
        insertados = 0

        for r in registros:
            marca = make_aware(r.timestamp)
            if marca > fecha_minima:
                emp_pin = str(r.user_id).strip()
                punch_type = str(r.status)

                try:
                    empleado = HrEmployee.objects.get(emp_pin=emp_pin)

                    if not AttPunch.objects.filter(employee=empleado, punch_time=marca).exists():
                        AttPunch.objects.create(
                            employee=empleado,
                            punch_time=marca,
                            terminal_id=nombre_terminal,
                            punch_type=punch_type
                        )
                        insertados += 1

                except HrEmployee.DoesNotExist:
                    print(f"⚠️ PIN no registrado: {emp_pin}")

        print(f"✅ {insertados} registros insertados desde {nombre_terminal}.\n")

    except Exception as e:
        print(f"❌ Error con {nombre_terminal}: {e}")
    finally:
        if conn:
            try:
                conn.enable_device()
                conn.disconnect()
            except:
                pass
            print(f"🔌 {nombre_terminal} desconectado.\n")

# ===============================
# Ejecutar sincronización
# ===============================
DISPOSITIVOS = [
    {'ip': '192.168.0.211', 'nombre': 'BIO-01'},
    {'ip': '192.168.1.211', 'nombre': 'BIO-02'},
    {'ip': '192.168.4.211', 'nombre': 'BIO-03'},
]

if __name__ == "__main__":
    for d in DISPOSITIVOS:
        sincronizar_dispositivo(d['ip'], d['nombre'])
