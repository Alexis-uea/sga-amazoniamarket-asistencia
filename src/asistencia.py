"""
Módulo de Registro de Asistencia — SGA-AmazoniaMarket (Grupo 12).

Borrador del primer incremento (RF-01): cálculo de horas trabajadas
entre la hora de entrada y la hora de salida.
"""

from datetime import datetime

FORMATO_HORA = "%H:%M"


def calcular_horas_trabajadas(hora_entrada: str, hora_salida: str) -> float:
    """Calcula las horas trabajadas en una jornada.

    >>> calcular_horas_trabajadas("08:00", "17:00")
    9.0
    """
    entrada = datetime.strptime(hora_entrada, FORMATO_HORA)
    salida = datetime.strptime(hora_salida, FORMATO_HORA)
    return round((salida - entrada).total_seconds() / 3600, 2)