from django.db import models
from django.contrib.auth.models import User

class AcGroup(models.Model):
    id = models.AutoField(primary_key=True)
    acgroup_id = models.IntegerField(blank=True, null=True)
    acgroup_name = models.CharField(max_length=6, blank=True, null=True)
    acgroup_holidayvalid = models.IntegerField(blank=True, null=True)
    acgroup_verifystytle = models.IntegerField(blank=True, null=True)
    timezone1 = models.CharField(max_length=50, blank=True, null=True)
    timezone2 = models.CharField(max_length=50, blank=True, null=True)
    timezone3 = models.CharField(max_length=50, blank=True, null=True)
    terminal_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ac_group'

class AcHolidaysetting(models.Model):
    id = models.AutoField(primary_key=True)
    holiday_id = models.CharField(max_length=50, blank=True, null=True)
    holiday_name = models.CharField(max_length=100, blank=True, null=True)
    holiday_start = models.DateField(blank=True, null=True)
    holiday_end = models.DateField(blank=True, null=True)
    actimezoneid = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ac_holidaysetting'

class AcTimezone(models.Model):
    id = models.AutoField(primary_key=True)
    timezone_id = models.CharField(max_length=50, blank=True, null=True)
    timezone_name = models.CharField(max_length=255, blank=True, null=True)
    timezone_sunstart = models.CharField(max_length=50, blank=True, null=True)
    timezone_sunend = models.CharField(max_length=50, blank=True, null=True)
    timezone_monstart = models.CharField(max_length=50, blank=True, null=True)
    timezone_monend = models.CharField(max_length=50, blank=True, null=True)
    timezone_tuesstart = models.CharField(max_length=50, blank=True, null=True)
    timezone_tuesend = models.CharField(max_length=50, blank=True, null=True)
    timezone_wedstart = models.CharField(max_length=50, blank=True, null=True)
    timezone_wedend = models.CharField(max_length=50, blank=True, null=True)
    timezone_thursstart = models.CharField(max_length=50, blank=True, null=True)
    timezone_thursend = models.CharField(max_length=50, blank=True, null=True)
    timezone_fristart = models.CharField(max_length=50, blank=True, null=True)
    timezone_friend = models.CharField(max_length=50, blank=True, null=True)
    timezone_satstart = models.CharField(max_length=50, blank=True, null=True)
    timezone_satend = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ac_timezone'
        
        
# empleados


    
    
    
    

class HrDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    dept_code = models.IntegerField(blank=True, null=True)
    dept_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_department'

  # turnos class AttShift(models.Model):
 
class AttShift(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria autoincremental
    shift_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    max_entry_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    work_hours = models.IntegerField(null=True, blank=True)
    break_type = models.CharField(max_length=20, choices=[
        ('Sin descanso', 'Sin descanso'),
        ('Descanso libre', 'Descanso libre')
    ], default='Sin descanso')
    break_minutes = models.IntegerField(default=0, null=True, blank=True)
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ], default='Activo')

    def __str__(self):
        return f"{self.shift_name} ({self.start_time} - {self.end_time})"

    class Meta:
        db_table = "att_shift"
        managed = False  # Para evitar que Django modifique la tabla



#roles

class EmpRole(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'emp_role'
        managed = False

    def __str__(self):
        return self.nombre


#roles
class EmpJob(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'emp_job'
        managed = False

    def __str__(self):
        return self.nombre


#centros de costo
class EmpCostCenter(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'emp_cost_center'
        managed = False # por aca 
    def __str__(self):
        return self.nombre




    #grupos
class HrGroup(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    jefe_planta = models.ForeignKey('HrEmployee', on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos_como_jefe')

    
    

    class Meta:
        db_table = 'hr_group'  # 🔥 Asegura que se use la tabla correcta en la BD
        managed = False

    def __str__(self):
        return self.nombre  # ✅ Corregido
    
    
class GrupoSupervisor(models.Model):
    grupo = models.ForeignKey(HrGroup, on_delete=models.CASCADE, db_column='grupo_id')
    supervisor = models.ForeignKey('HrEmployee', on_delete=models.CASCADE, db_column='supervisor_id')

    class Meta:
        db_table = 'grupo_supervisor'
        managed = False  # porque ya la creaste manualmente
        unique_together = ('grupo', 'supervisor')

    
   
    
    
    #empleados
    
class HrEmployee(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_pin = models.BigIntegerField(unique=True, null=False, blank=False)  # Cedula
    emp_firstname = models.CharField(max_length=100, null=False, blank=False)  # Nombre
    emp_lastname = models.CharField(max_length=100, null=False, blank=False)  # Apellido
    emp_job = models.ForeignKey(EmpJob, on_delete=models.CASCADE, null=False, blank=False)  # Cargo
    #emp_emp_group = models.ForeignKey(HrGroup, on_delete=models.CASCADE, null=False, blank=False, db_column='emp_group')  # Grupo (¡este es el que te da error!)
    emp_group = models.ForeignKey(HrGroup, on_delete=models.CASCADE, db_column='emp_group')
    emp_role = models.ForeignKey(EmpRole, on_delete=models.CASCADE, null=False, blank=False)  # Rol
    emp_cost_center = models.ForeignKey(EmpCostCenter, on_delete=models.CASCADE, null=False, blank=False)  # Centro de Costo
    emp_email = models.CharField(max_length=150, unique=True, null=False, blank=False)  # Correo
    emp_photo = models.CharField(max_length=255, null=True, blank=True)  # Foto (opcional)
    emp_active = models.BooleanField(default=True, null=False, blank=False)  # Activo o Inactivo
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'hr_employee'   # 🔥 Aquí se lo dices a Django
        managed = False # 🔒 Importante: no la maneja Django
        
    def __str__(self):
        return f"{self.emp_firstname} {self.emp_lastname}"





#qué turno tiene asignado un empleado en una fecha específica

class EmpleadoTurno(models.Model):
    empleado = models.ForeignKey('HrEmployee', on_delete=models.CASCADE, db_column='empleado_id')
    turno = models.ForeignKey('AttShift', on_delete=models.CASCADE, db_column='turno_id')
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    festivo = models.BooleanField(default=False)  
    # Horas extras desglosadas
    horas_extras_diurnas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    horas_extras_nocturnas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    horas_extras_festivas_diurnas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    horas_extras_festivas_nocturnas = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Recargos
    recargo_nocturno = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    recargo_nocturno_festivo = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Aprobación y comentarios del líder/supervisor
    aprobado_por_lider = models.BooleanField(default=False)
    comentario = models.TextField(blank=True, null=True)

    # Control automático de registros
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'empleado_turno'
        unique_together = ('empleado', 'fecha')
        managed = True  # ✅ Esto es importante para que Django la cree y la administre

    def __str__(self):
        return f"{self.empleado} - {self.fecha} - Turno: {self.turno}"






# esta es la tabla de marcaciones
class AttPunch(models.Model):
    employee = models.ForeignKey('HrEmployee', on_delete=models.CASCADE, db_column='employee_id')
    punch_time = models.DateTimeField()
    terminal_id = models.CharField(max_length=50)
    punch_type = models.CharField(max_length=20)

    class Meta:
        db_table = 'att_punches'  # Para que la tabla tenga el mismo nombre
        verbose_name = 'Marcación'
        verbose_name_plural = 'Marcaciones'
        managed = False

    def __str__(self):
        return f"{self.employee.emp_firstname} - {self.punch_time}"

    
    
    
    