import os
import sys
import django
from zk import ZK
from datetime import datetime, timedelta

# Configuración de Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  
django.setup()

# Configuración del biométrico
BIOMETRICO_IP = "192.168.0.211"
PUERTO = 4370

def ajustar_registros():
    """Detectar y corregir errores en la alternancia de registros (entrada/salida)"""
    zk = ZK(BIOMETRICO_IP, port=PUERTO, timeout=5)
    conn = None

    try:
        print("⏳ Conectando al biométrico...")
        conn = zk.connect()
        print("✅ Conectado al biométrico")

        registros = conn.get_attendance()
        if not registros:
            print("⚠ No hay registros en el biométrico.")
            return

        registros_ordenados = sorted(registros, key=lambda r: (r.user_id, r.timestamp))  # Ordenar por usuario y fecha
        registros_por_usuario = {}

        for r in registros_ordenados:
            if r.user_id not in registros_por_usuario:
                registros_por_usuario[r.user_id] = []
            registros_por_usuario[r.user_id].append(r)

        print("\n📋 **Verificando alternancia de registros:**")
        for user_id, registros in registros_por_usuario.items():
            for i in range(1, len(registros)):
                prev = registros[i - 1]
                curr = registros[i]

                if prev.user_id == curr.user_id:
                    tiempo_entre_registros = curr.timestamp - prev.timestamp

                    if prev.status == curr.status:  # Si dos registros seguidos son entrada o salida
                        print(f"⚠ Posible error detectado para usuario {user_id}:")
                        print(f"   📌 {prev.timestamp} → {curr.timestamp} (ambos como '{prev.status}')")

                        # Si el tiempo entre registros es menor a 6 horas, corregimos automáticamente
                        if tiempo_entre_registros < timedelta(hours=6):
                            nuevo_status = 4 if prev.status == 1 else 1
                            print(f"   🔄 Corrigiendo: {curr.timestamp} será cambiado a {nuevo_status}")

        print("✅ Ajuste finalizado.")

    except Exception as e:
        print(f"❌ Error al conectar con el biométrico: {e}")

    finally:
        if conn:
            conn.disconnect()
            print("🔌 Desconectado del biométrico")

if __name__ == "__main__":
    ajustar_registros()




