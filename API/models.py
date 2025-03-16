from django.db import models

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

class HrEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    emp_pin = models.BigIntegerField(unique=True)
    emp_ssn = models.CharField(max_length=50, blank=True, null=True)
    emp_role = models.CharField(max_length=50, blank=True, null=True)
    emp_firstname = models.CharField(max_length=50, blank=True, null=True)
    emp_lastname = models.CharField(max_length=50, blank=True, null=True)
    emp_username = models.CharField(max_length=50, blank=True, null=True)
    emp_pwd = models.CharField(max_length=100, blank=True, null=True)
    emp_phone = models.CharField(max_length=20, blank=True, null=True)
    emp_email = models.EmailField(max_length=255, blank=True, null=True)
    emp_privilege = models.IntegerField(blank=True, null=True)
    emp_hiredate = models.DateField(blank=True, null=True)
    emp_firedate = models.DateField(blank=True, null=True)
    emp_birthday = models.DateField(blank=True, null=True)
    emp_active = models.BooleanField(default=True)
    emp_address = models.CharField(max_length=255, blank=True, null=True)
    emp_operationmode = models.IntegerField(blank=True, null=True)
    emp_gender = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey('HrDepartment', on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = False
        db_table = 'hr_employee'

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



