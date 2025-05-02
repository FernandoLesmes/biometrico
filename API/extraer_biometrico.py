from zk import ZK
from datetime import datetime

BIOMETRICO_IP = "192.168.0.211"
PUERTO = 4370

cedula_usuario = "1051287060"
fecha_inicio = datetime(2025, 4, 22)
fecha_fin = datetime(2025, 4, 24)

zk = ZK(BIOMETRICO_IP, port=PUERTO, timeout=20, password=0, force_udp=False, ommit_ping=True)

try:
    print("⏳ Conectando al biométrico...")
    conn = zk.connect()
    conn.disable_device()

    print(f"👤 Buscando datos del usuario {cedula_usuario}...")
    usuarios = conn.get_users()
    user_found = False

    for user in usuarios:
        if str(user.user_id) == cedula_usuario:
            user_found = True
            print("🔍 Datos del usuario:")
            print(f"🆔 user_id: {user.user_id}")
            print(f"🔢 uid interno: {user.uid}")
            print(f"📛 nombre: {user.name}")
            print(f"🧾 privilegio: {user.privilege}")
            print(f"🧩 grupo: {user.group_id}")
            print(f"🃏 tarjeta: {user.card}")
            print(f"🔒 password (si tiene): {user.password}")
            print("-" * 40)

    if not user_found:
        print("⚠️ Usuario no encontrado en el biométrico")

    print("📥 Obteniendo marcaciones...")
    registros = conn.get_attendance()

    for r in registros:
        if str(r.user_id) == cedula_usuario and fecha_inicio <= r.timestamp <= fecha_fin:
            print(f"📅 {r.timestamp} - UID: {r.user_id} - Status: {r.status} - UID interno: {r.uid}")

    conn.enable_device()
    conn.disconnect()

except Exception as e:
    print("❌ Error:", e)

