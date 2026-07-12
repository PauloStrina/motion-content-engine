# OPERACIÓN DEL REPOSITORIO

## 1. Responsabilidad del sistema

El repositorio ejecuta un plan mensual ya definido y aprobado. No reemplaza la conversación estratégica ni editorial.

Entrada:

```text
manifiestos/mes_<YYYY-MM>.json
```

Salida:

- especificaciones visuales en `design-system/slides/`;
- PNG de carruseles;
- medios publicados en `motion-media`;
- publicaciones programadas en Blotato;
- newsletters listas para publicación manual.

## 2. Flujo

### Preparación

Ejecutar `1-preparar-assets-mensuales` con el mes correspondiente.

El workflow:

1. valida estructura y aprobación;
2. lee únicamente el manifiesto y el sistema visual;
3. genera las especificaciones visuales;
4. verifica que el copy no haya sido alterado;
5. commitea solo archivos de `design-system/slides/`.

### Prueba

Ejecutar `2-motor-mensual` en modo `dry`.

El workflow renderiza y simula la programación sin llamar a Blotato. Un manifiesto en borrador puede probarse, pero debe ser estructuralmente válido.

### Publicación

Ejecutar `2-motor-mensual` en modo `live`.

Requisitos:

- `estado: aprobado`;
- `aprobado_por` informado;
- `aprobado_en` en ISO 8601;
- assets visuales existentes;
- cuentas y secretos configurados.

## 3. Horarios

La zona horaria editorial es `America/Argentina/Buenos_Aires`. El sistema convierte los horarios locales a UTC antes de enviarlos a Blotato.

Valores actuales:

- LinkedIn de Paulo: 09:00.
- Instagram de Motion: 12:00.

## 4. Fuentes de verdad

- Estrategia: `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- Corpus y evidencia: `knowledge/MASTER_BASE_CONOCIMIENTO.md` en la base del proyecto; el repositorio conserva una referencia, no una copia operativa.
- Ejecución mensual: manifiesto aprobado.

Los archivos de `archive/` no se consultan en producción.

## 5. Subsistema de video

Los workflows, prompts y pipelines de creación y edición de reels se mantienen sin cambios y operan de forma independiente. Esta refactorización no modifica:

- workflows `3-*`, `4-*`, `5-*` ni `debug-frame`;
- `pipelines/video/`;
- `scripts/PROMPT_editor_video.md`;
- procesamiento, corte, subtitulado, render o catalogación de reels.

## 6. Recuperación

La rama `backup/pre-canonica-2026-07-13` conserva el estado completo anterior a esta reorganización. Los archivos retirados se documentan en `archive/2026-07-pre-canonica/README.md`.
