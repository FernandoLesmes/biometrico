import csv
import pymysql

# Conexión
conexion = pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='root',
    password='Aceros123*',
    database='db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

archivo_csv = 'empleados.csv'  # mismo nombre

def obtener_id(cursor, tabla, campo, valor):
    sql = f"SELECT id FROM {tabla} WHERE {campo} = %s"
    cursor.execute(sql, (valor,))
    resultado = cursor.fetchone()
    return resultado['id'] if resultado else None

with conexion.cursor() as cursor:
    with open(archivo_csv, newline='', encoding='latin1') as csvfile:
        lector = csv.DictReader(csvfile, delimiter=';')
        insertados = 0
        errores = 0

        for fila in lector:
            try:
                cedula = fila['Cedula'].strip()
                nombre = fila['Nombre'].strip()
                apellidos = fila['Apellidos'].strip()
                cargo = fila['Cargo'].strip()
                grupo_nombre = fila['Grupo'].strip()
                rol = fila['Rol'].strip()
                centro_costo = fila['Centro De costo'].strip()
                correo = fila['Correo'].strip()

                # Buscar IDs
                job_id = obtener_id(cursor, 'emp_job', 'nombre', cargo)
                role_id = obtener_id(cursor, 'emp_role', 'nombre', rol)
                centro_id = obtener_id(cursor, 'emp_cost_center', 'nombre', centro_costo)
                grupo_id = obtener_id(cursor, 'hr_group', 'nombre', grupo_nombre)

                if not all([job_id, role_id, centro_id, grupo_id]):
                    print(f"❌ No se encontró ID para -> Cargo: {cargo}, Rol: {rol}, Centro: {centro_costo}, Grupo: {grupo_nombre}")
                    errores += 1
                    continue

                sql_insert = """
                    INSERT INTO hr_employee (
                        emp_pin, emp_firstname, emp_lastname, emp_job_id,
                        emp_group, emp_role_id, emp_cost_center_id,
                        emp_email, emp_active, emp_photo
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, NULL)
                """
                valores = (
                    cedula, nombre, apellidos, job_id,
                    grupo_id, role_id, centro_id,
                    correo
                )
                cursor.execute(sql_insert, valores)
                insertados += 1

            except Exception as e:
                print(f"⚠️ Error inesperado con cédula {cedula}: {e}")
                errores += 1

    conexion.commit()

print(f"\n✅ Empleados insertados: {insertados}")
print(f"⚠️ Empleados con errores: {errores}")
conexion.close()
