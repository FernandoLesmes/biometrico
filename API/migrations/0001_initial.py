# Generated by Django 5.1.6 on 2025-04-23 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('acgroup_id', models.IntegerField(blank=True, null=True)),
                ('acgroup_name', models.CharField(blank=True, max_length=6, null=True)),
                ('acgroup_holidayvalid', models.IntegerField(blank=True, null=True)),
                ('acgroup_verifystytle', models.IntegerField(blank=True, null=True)),
                ('timezone1', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone2', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone3', models.CharField(blank=True, max_length=50, null=True)),
                ('terminal_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ac_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AcHolidaysetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('holiday_id', models.CharField(blank=True, max_length=50, null=True)),
                ('holiday_name', models.CharField(blank=True, max_length=100, null=True)),
                ('holiday_start', models.DateField(blank=True, null=True)),
                ('holiday_end', models.DateField(blank=True, null=True)),
                ('actimezoneid', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ac_holidaysetting',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AcTimezone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timezone_id', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_name', models.CharField(blank=True, max_length=255, null=True)),
                ('timezone_sunstart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_sunend', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_monstart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_monend', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_tuesstart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_tuesend', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_wedstart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_wedend', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_thursstart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_thursend', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_fristart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_friend', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_satstart', models.CharField(blank=True, max_length=50, null=True)),
                ('timezone_satend', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ac_timezone',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AttPunch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punch_time', models.DateTimeField()),
                ('terminal_id', models.CharField(max_length=50)),
                ('punch_type', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Marcación',
                'verbose_name_plural': 'Marcaciones',
                'db_table': 'att_punches',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AttShift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shift_name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('max_entry_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('work_hours', models.IntegerField(blank=True, null=True)),
                ('break_type', models.CharField(choices=[('Sin descanso', 'Sin descanso'), ('Descanso libre', 'Descanso libre')], default='Sin descanso', max_length=20)),
                ('break_minutes', models.IntegerField(blank=True, default=0, null=True)),
                ('break_start', models.TimeField(blank=True, null=True)),
                ('break_end', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo', max_length=10)),
            ],
            options={
                'db_table': 'att_shift',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpCostCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'emp_cost_center',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'emp_job',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'emp_role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HrDepartment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dept_code', models.IntegerField(blank=True, null=True)),
                ('dept_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'hr_department',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HrEmployee',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('emp_pin', models.BigIntegerField(unique=True)),
                ('emp_firstname', models.CharField(max_length=100)),
                ('emp_lastname', models.CharField(max_length=100)),
                ('emp_email', models.CharField(max_length=150, unique=True)),
                ('emp_photo', models.CharField(blank=True, max_length=255, null=True)),
                ('emp_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'hr_employee',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HrGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'hr_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpleadoTurno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('festivo', models.BooleanField(default=False)),
                ('horas_extras_diurnas', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('horas_extras_nocturnas', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('horas_extras_festivas_diurnas', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('horas_extras_festivas_nocturnas', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('recargo_nocturno', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('recargo_nocturno_festivo', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('aprobado_por_lider', models.BooleanField(default=False)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('empleado', models.ForeignKey(db_column='empleado_id', on_delete=django.db.models.deletion.CASCADE, to='API.hremployee')),
                ('turno', models.ForeignKey(db_column='turno_id', on_delete=django.db.models.deletion.CASCADE, to='API.attshift')),
            ],
            options={
                'db_table': 'empleado_turno',
                'managed': True,
                'unique_together': {('empleado', 'fecha')},
            },
        ),
    ]
