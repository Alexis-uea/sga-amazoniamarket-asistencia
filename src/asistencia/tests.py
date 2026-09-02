"""Pruebas automatizadas del módulo de Registro de Asistencia.

Ejecutar: python src/manage.py test -v 2
Automatiza CP-U01..U04 (unitarias) y CP-I01..I03 (integración) del Avance 3.
"""

from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Empleado, RegistroAsistencia
from .services import DuplicadoError, registrar_entrada, registrar_salida


def momento(hora, minuto):
    """Crea un datetime con zona horaria."""
    return timezone.make_aware(datetime(2026, 9, 2, hora, minuto))


JORNADA = momento(8, 2)


class PruebasUnitarias(TestCase):
    """CP-U01 a CP-U04: comportamiento de cada función de servicio."""

    def setUp(self):
        self.empleado = Empleado.objects.create(
            cedula="0102030405",
            nombres="Luis",
            apellidos="Quishpe",
            cargo="Cajero",
        )

    def test_cp_u01_empleado_inexistente(self):
        """CP-U01: se rechaza registrar entrada de un empleado inexistente."""
        with self.assertRaises(ValueError):
            registrar_entrada(None, JORNADA)

    def test_cp_u02_salida_sin_entrada_previa(self):
        """CP-U02: no se permite salida sin entrada previa (AS-16)."""
        with self.assertRaises(ValidationError):
            registrar_salida(self.empleado, momento(17, 10))

    def test_cp_u03_salida_duplicada(self):
        """CP-U03: no se permite una segunda salida en la misma jornada."""
        registrar_entrada(self.empleado, JORNADA)
        registrar_salida(self.empleado, momento(17, 0))

        with self.assertRaises(ValidationError):
            registrar_salida(self.empleado, momento(18, 0))

    def test_cp_u04_registro_valido(self):
        """CP-U04: entrada y salida válidas completan la jornada."""
        registro = registrar_entrada(self.empleado, JORNADA)

        self.assertEqual(registro.estado, "EN_JORNADA")

        registro = registrar_salida(self.empleado, momento(17, 10))

        self.assertEqual(registro.estado, "COMPLETADO")
        self.assertIsNotNone(registro.hora_salida)


class PruebasIntegracion(TestCase):
    """CP-I01 a CP-I03: módulo + base de datos (SQLite en memoria)."""

    def setUp(self):
        self.empleado = Empleado.objects.create(
            cedula="0607080910",
            nombres="María",
            apellidos="Grefa",
            cargo="Bodeguera",
        )

    def test_cp_i01_persistencia_de_entrada(self):
        """CP-I01 · CASO MÁS CRÍTICO: la entrada queda guardada en la BD."""
        registrar_entrada(self.empleado, JORNADA)

        guardado = RegistroAsistencia.objects.get(
            empleado=self.empleado,
            fecha=JORNADA.date(),
        )

        self.assertEqual(guardado.hora_entrada, JORNADA)
        self.assertIsNone(guardado.hora_salida)

    def test_cp_i02_actualizacion_con_salida(self):
        """CP-I02: registrar la salida actualiza el registro persistido."""
        registrar_entrada(self.empleado, JORNADA)

        salida = momento(17, 10)
        registrar_salida(self.empleado, salida)

        guardado = RegistroAsistencia.objects.get(
            empleado=self.empleado
        )

        self.assertEqual(guardado.hora_salida, salida)
        self.assertEqual(guardado.estado, "COMPLETADO")
        self.assertEqual(guardado.horas_trabajadas, 9.13)

    def test_cp_i03_entrada_duplicada_rechazada(self):
        """CP-I03: la BD conserva una sola entrada por jornada (RF-02)."""
        registrar_entrada(self.empleado, JORNADA)

        with self.assertRaises(DuplicadoError):
            registrar_entrada(
                self.empleado,
                momento(9, 0),
            )

        self.assertEqual(
            RegistroAsistencia.objects.filter(
                empleado=self.empleado,
                fecha=JORNADA.date(),
            ).count(),
            1,
        )