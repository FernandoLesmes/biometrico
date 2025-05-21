from zk import ZK, const

def registrar_en_biometrico(emp_pin, emp_nombre, ip_biometrico):
    try:
        zk = ZK(ip_biometrico, port=4370, timeout=10, password=0, force_udp=False, ommit_ping=True)
        conn = zk.connect()
        conn.disable_device()

        uid = int(emp_pin) % 65535  # 🔹 Asegura que no exceda el rango permitido
        conn.set_user(
            uid=uid,
            name=emp_nombre,
            privilege=const.USER_DEFAULT,
            password='',
            group_id='',
            user_id=emp_pin  # Este sí puede ser largo, es como el "número real"
        )

        print(f"✅ Usuario {emp_pin} - {emp_nombre} registrado en el biométrico {ip_biometrico}")
        conn.enable_device()
        conn.disconnect()
    except Exception as e:
        print(f"❌ Error registrando en biométrico {ip_biometrico}: {e}")

