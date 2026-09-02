from django.db import models


class Empleado(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=80, default="")

    class Meta:
        db_table = "empleado"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class RegistroAsistencia(models.Model):
    """Entidad Asistencia del diagrama de clases (Unidad 2)."""

    class Estado(models.TextChoices):
        EN_JORNADA = "EN_JORNADA"
        COMPLETADO = "COMPLETADO"
        TARDANZA = "TARDANZA"  # se usará al automatizar CP-U05

    empleado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, related_name="asistencias"
    )
    fecha = models.DateField()
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.EN_JORNADA
    )

    class Meta:
        db_table = "registro_asistencia"
        constraints = [
            # Regla AS-16: una sola entrada por empleado y jornada
            models.UniqueConstraint(
                fields=["empleado", "fecha"], name="una_entrada_por_jornada"
            ),
        ]

    @property
    def horas_trabajadas(self):
        """Método calcularHorasTrabajadas() del diagrama de clases."""
        if self.hora_salida is None:
            return None
        return round(
            (self.hora_salida - self.hora_entrada).total_seconds() / 3600, 2
        )
