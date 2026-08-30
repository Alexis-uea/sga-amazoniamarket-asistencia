# SGA-AmazoniaMarket · Módulo de Registro de Asistencia

Sistema de Gestión de Asistencia y Nómina Automatizada para el supermercado
**AmazoniaMarket**. Este repositorio aloja el **módulo de Registro de Asistencia**
(primer incremento del sistema), que atiende los requerimientos **RF-01** y **RF-02**
del SRS.

**Stack:** Python 3.12 + Django 5 — seleccionado mediante matriz de decisión (Avance 1, U3).

## Integrantes — Grupo 12
| Integrante | Rol |
|---|---|
| Merino Moya Alexis Efraín | Líder de desarrollo · mantenedor de `main` |
| Calva Abad Cristian Paul | Desarrollo · revisión de PR |
| Maya Enríquez Lilia Lucely | Desarrollo · revisión de PR |

## Estructura del repositorio
- `src/` → código fuente del módulo.
- `.github/workflows/ci.yml` → pipeline de integración continua.
- `.gitignore` → archivos que Git nunca sube (secretos, BD local, caché).

## Flujo de trabajo con ramas (GitHub Flow)
`main` es la rama **estable**: siempre debe compilar y pasar el CI. Nadie hace commits
directamente sobre ella.

1. Crear una rama desde `main` con nombre descriptivo:
   `feature/...` para funcionalidades (ej. `feature/registrar-asistencia`),
   `fix/...` para correcciones (ej. `fix/validar-hora-salida`).
2. Hacer **commits pequeños** con mensajes claros (ver convención abajo).
3. Subir la rama (`git push origin <rama>`) y abrir un **Pull Request** hacia `main`.
4. Otro integrante revisa el PR y el pipeline de CI debe quedar **en verde ✔**.
5. Fusionar el PR y eliminar la rama.

## Convención de mensajes de commit
Formato `tipo: descripción en presente`:
- `feat: agrega cálculo de horas trabajadas (RF-01)`
- `fix: corrige cálculo en turnos nocturnos`
- `docs: actualiza flujo de ramas en el README`
- `test: agrega prueba unitaria de horas trabajadas`

## Integración continua
El pipeline se ejecuta en cada push y pull request (pestaña **Actions**).
Hoy verifica la sintaxis del código; en la Semana 12 ejecutará también las pruebas.