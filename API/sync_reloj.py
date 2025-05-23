# sync_reloj.py
from zk import ZK
import django, os

# Configuración del entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from API.models import HrEmployee, AttPunch
from datetime import datetime

DISPOSITIVOS = [
    {'ip': '192.168.0.211', 'nombre': 'BIO-01'},
    {'ip': '192.168.1.211', 'nombre': 'BIO-02'},
    {'ip': '192.168.4.211', 'nombre': 'BIO-03'},
]

def sincronizar_dispositivo(ip, nombre_terminal):
    print(f"📡 Conectando a {nombre_terminal} ({ip})...")
    zk = ZK(ip, port=4370, timeout=5)
    conn = None

    try:
        conn = zk.connect()
        conn.disable_device()
        registros = conn.get_attendance()
        insertados = 0

        for r in registros:
            emp_pin = str(r.user_id).strip()
            punch_time = r.timestamp
            punch_type = str(r.status)  # 0 = entrada, 1 = salida...

            try:
                empleado = HrEmployee.objects.get(emp_pin=emp_pin)

                existe = AttPunch.objects.filter(employee=empleado, punch_time=punch_time).exists()
                if not existe:
                    AttPunch.objects.create(
                        employee=empleado,
                        punch_time=punch_time,
                        terminal_id=nombre_terminal,
                        punch_type=punch_type
                    )
                    insertados += 1

            except HrEmployee.DoesNotExist:
                print(f"⚠️ PIN no registrado: {emp_pin}")
                continue

        print(f"✅ {insertados} registros insertados desde {nombre_terminal}.\n")

    except Exception as e:
        print(f"❌ Error con {nombre_terminal}: {e}")
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()
            print(f"🔌 {nombre_terminal} desconectado.\n")

# 🔁 Ejecutar sincronización en todos los dispositivos
if __name__ == "__main__":
    for d in DISPOSITIVOS:
        sincronizar_dispositivo(d['ip'], d['nombre'])

