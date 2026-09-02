"""Servicios del módulo de Registro de Asistencia — RF-01 y RF-02."""
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from .models import RegistroAsistencia


class DuplicadoError(Exception):
    """Se intentó registrar una segunda entrada en la misma jornada (AS-16)."""


def registrar_entrada(empleado, momento):
    """Registra la hora de entrada de un empleado (RF-01)."""
    if empleado is None or empleado.pk is None:
        raise ValueError("empleado_id inválido")
    try:
        with transaction.atomic():  # aísla el fallo sin envenenar la transacción
            return RegistroAsistencia.objects.create(
                empleado=empleado,
                fecha=momento.date(),
                hora_entrada=momento,
            )
    except IntegrityError as exc:
        raise DuplicadoError(
            "Ya existe una entrada para este empleado en la jornada"
        ) from exc


def registrar_salida(empleado, momento):
    """Registra la salida. Regla AS-16: sin entrada previa no hay salida,
    y no se admite una segunda salida en la misma jornada."""
    if empleado is None or empleado.pk is None:
        raise ValueError("empleado_id inválido")
    registro = RegistroAsistencia.objects.filter(
        empleado=empleado, fecha=momento.date()
    ).first()
    if registro is None:
        raise ValidationError("No existe una entrada previa para esta jornada")
    if registro.hora_salida is not None:
        raise ValidationError("La salida de esta jornada ya fue registrada")
    registro.hora_salida = momento
    registro.estado = RegistroAsistencia.Estado.COMPLETADO
    registro.save()
    return registro
