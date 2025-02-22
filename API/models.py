#from django.db import models
from django.db import models

class Empleado(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    puesto = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.nombre} {self.apellido}"

class RegistroAsistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')])

    def __str__(self):
        return f"{self.empleado.user_id} - {self.tipo} - {self.timestamp}"

