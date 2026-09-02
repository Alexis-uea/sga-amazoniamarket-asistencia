"""Módulo de Registro de Asistencia — SGA-AmazoniaMarket (RF-01, RF-02).

Semilla inicial; en próximas semanas se integrará a la app Django.
"""
from datetime import datetime


def registrar_entrada(empleado_id: int, momento: datetime) -> dict:
    """Registra la hora de entrada de un empleado (RF-01)."""
    if empleado_id <= 0:
        raise ValueError("empleado_id inválido")
    return {"empleado": empleado_id, "entrada": momento, "salida": None}


def validar_salida(registro: dict | None) -> bool:
    """Una salida solo es válida si existe entrada previa y no hay salida duplicada (AS-16)."""
    return registro is not None and registro.get("salida") is None