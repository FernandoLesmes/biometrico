from django import forms
from .models import AttShift



class ShiftForm(forms.ModelForm):
    class Meta:
        model = AttShift
        fields = [
            'shift_name', 'start_time', 'max_entry_time', 'end_time', 
            'work_hours', 'break_type', 'break_minutes', 
            'break_start', 'break_end', 'status'
        ]

        labels = {
            'shift_name': 'Nombre del Turno',
            'start_time': 'Hora de Entrada',
            'max_entry_time': 'Hora Máxima de Entrada',
            'end_time': 'Hora de Salida',
            'work_hours': 'Horas de Trabajo',
            'break_type': 'Tipo de Descanso',
            'break_minutes': 'Minutos de Descanso',
            'break_start': 'Inicio de Descanso',
            'break_end': 'Fin de Descanso',
            'status': 'Estado',
        }

        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'max_entry_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'break_start': forms.TimeInput(attrs={'type': 'time'}),
            'break_end': forms.TimeInput(attrs={'type': 'time'}),
        }
