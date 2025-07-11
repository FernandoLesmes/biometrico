# Generated by Django 5.1.6 on 2025-06-19 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_permisorol'),
    ]

    operations = [
        migrations.CreateModel(
            name='AprobacionHorasExtras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprobado_supervisor', models.BooleanField(default=False)),
                ('aprobado_jefe_area', models.BooleanField(default=False)),
                ('fecha_aprobacion_supervisor', models.DateTimeField(blank=True, null=True)),
                ('fecha_aprobacion_jefe', models.DateTimeField(blank=True, null=True)),
                ('bloqueado_para_pago', models.BooleanField(default=False)),
                ('jefe_aprobo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jefe_aprobaciones', to='API.hremployee')),
                ('supervisor_aprobo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisor_aprobaciones', to='API.hremployee')),
                ('turno', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='API.empleadoturno')),
            ],
            options={
                'verbose_name': 'Historial Aprobación de Horas Extras',
                'verbose_name_plural': 'Historial Aprobación de Horas Extras',
            },
        ),
    ]
