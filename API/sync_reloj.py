from zk import ZK

zk = ZK('192.168.0.211', port=4370, timeout=5)
conn = None

try:
    print("⏳ Conectando al biométrico...")
    conn = zk.connect()
    print("✅ Conexión exitosa!")

    print("\n📋 Obteniendo registros de asistencia...")
    registros = conn.get_attendance()

    if registros:
        for r in registros[:20]:  # Muestra los primeros 20 registros
            print(f"Usuario: {r.user_id}, Fecha: {r.timestamp}, Estado: {r.status}")
    else:
        print("⚠ No hay registros en el biométrico.")

except Exception as e:
    print(f"❌ Error al conectar: {e}")

finally:
    if conn:
        conn.disconnect()
        print("🔌 Desconectado del biométrico")
