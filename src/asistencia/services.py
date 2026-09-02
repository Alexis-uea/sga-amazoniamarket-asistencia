from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone  # <-- Agregar esta importación
from .models import RegistroAsistencia

class DuplicadoError(Exception):
    """Se intentó registrar una segunda entrada en la misma jornada (AS-16)."""

def registrar_entrada(empleado, momento):
    if empleado is None or empleado.pk is None:
        raise ValueError("empleado_id inválido")
    
    # Extraemos la fecha local basada en la zona horaria de Django
    fecha_local = timezone.localdate(momento) 
    
    try:
        with transaction.atomic():
            return RegistroAsistencia.objects.create(
                empleado=empleado,
                fecha=fecha_local,  # <-- Usar fecha alineada
                hora_entrada=momento,
            )
    except IntegrityError as exc:
        raise DuplicadoError("Ya existe una entrada para este empleado en la jornada") from exc

def registrar_salida(empleado, momento):
    if empleado is None or empleado.pk is None:
        raise ValueError("empleado_id inválido")
    
    fecha_local = timezone.localdate(momento)
    registro = RegistroAsistencia.objects.filter(empleado=empleado, fecha=fecha_local).first()
    
    if registro is None:
        raise ValidationError("No existe una entrada previa para esta jornada")
    if registro.hora_salida is not None:
        raise ValidationError("La salida de esta jornada ya fue registrada")
    
    registro.hora_salida = momento
    registro.estado = RegistroAsistencia.Estado.COMPLETADO
    registro.save()
    return registro
