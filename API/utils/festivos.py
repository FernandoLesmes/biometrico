from datetime import date

# Festivos oficiales de Colombia para 2025
FESTIVOS_FIJOS = [
    date(2025, 1, 1),   # Año Nuevo
    date(2025, 1, 6),   # Reyes Magos (trasladado)
    date(2025, 3, 24),  # San José (trasladado)
    date(2025, 4, 10),  # Jueves Santo
    date(2025, 4, 11),  # Viernes Santo
    date(2025, 5, 1),   # Día del Trabajo
    date(2025, 5, 26),  # Ascensión (trasladado)
    date(2025, 6, 16),  # Corpus Christi (trasladado)
    date(2025, 6, 23),  # Sagrado Corazón (trasladado)
    date(2025, 7, 20),  # Independencia
    date(2025, 8, 7),   # Batalla de Boyacá
    date(2025, 8, 18),  # La Asunción (trasladado)
    date(2025, 10, 13), # Día de la Raza (trasladado)
    date(2025, 11, 3),  # Todos los Santos (trasladado)
    date(2025, 11, 17), # Independencia de Cartagena (trasladado)
    date(2025, 12, 8),  # Inmaculada Concepción
    date(2025, 12, 25), # Navidad
]

def es_festivo(fecha):
    """
    Retorna True si la fecha es un festivo o domingo.
    """
    return fecha in FESTIVOS_FIJOS or fecha.weekday() == 6  # domingo = 6
