# BACKUP PRE-CANÓNICA — JULIO 2026

## Punto de recuperación

- Rama completa: `backup/pre-canonica-2026-07-13`.
- Commit de origen: `edf06143967b49958f04fd490a0ea151e238711e`.

La rama es el backup completo e inmutable. No se copiaron archivos legacy dentro de `main` para evitar que agentes, búsquedas o scripts vuelvan a utilizarlos accidentalmente.

## Motivo

Se discontinuó el modelo donde GitHub definía estrategia, temas y copies. El sistema vigente recibe un manifiesto mensual aprobado y se limita a validar, diseñar, renderizar y programar.

## Archivos retirados del flujo activo

### Workflows

- `.github/workflows/1-cascada-mensual.yml`.
- `.github/workflows/1-cascada-semanal.yml`.
- `.github/workflows/2-motor-completo.yml`.

### Prompts

- `scripts/PROMPT_mes.md`.
- `scripts/PROMPT_redactor.md`.
- `scripts/PROMPT_newsletter.md`.
- `scripts/PROMPT_disenador.md`.
- `scripts/PROMPT_carrusel_newsletter.md`.

### Contratos y scripts semanales

- `scripts/manifiesto.py`.
- `scripts/publicador.py`.
- `scripts/generar_carrusel.py`.

### Planificación legacy

- `CALENDARIO_EDITORIAL.md`.

## Documentación reemplazada

- `README.md`.
- `CLAUDE.md`.

Las versiones anteriores también están en la rama de backup.

## Exclusión

El subsistema de creación y edición de video no fue modificado ni archivado. Los archivos estratégicos antiguos que todavía utiliza permanecen temporalmente en `strategy/` como compatibilidad y no gobiernan el flujo mensual.
