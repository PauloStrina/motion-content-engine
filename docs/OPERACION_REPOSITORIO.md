# OPERACIÓN DEL REPOSITORIO

## 1. Responsabilidad del sistema

El repositorio ejecuta un plan mensual ya definido. No reemplaza la conversación estratégica ni editorial.

La estrategia se organiza por mes. La producción, aprobación y programación pueden realizarse por semana para conservar flexibilidad operativa.

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

## 2. Alcances de ejecución

### Semana específica

Seleccionar `semana: 1`, `2`, `3` o `4`.

El sistema valida, diseña, renderiza y programa únicamente esa semana. La semana debe estar aprobada en su propio nodo. El manifiesto raíz y las semanas futuras pueden permanecer en borrador.

### Ciclo completo

Seleccionar `semana: todas`.

El sistema exige las cuatro semanas, secuencia completa y aprobación raíz del manifiesto.

## 3. Flujo

### Preparación

Ejecutar `1-preparar-assets` con:

- `mes`: ciclo editorial `YYYY-MM`;
- `semana`: número de semana o `todas`.

El workflow:

1. valida estructura y aprobación del alcance;
2. lee únicamente el manifiesto y el sistema visual;
3. genera las especificaciones visuales necesarias;
4. verifica que el copy no haya sido alterado;
5. commitea solo archivos de `design-system/slides/`.

Cuando las especificaciones visuales ya existen y pasan validación, este paso puede omitirse.

### Prueba

Ejecutar `2-motor` en modo `dry` para la misma semana.

El workflow renderiza y simula la programación sin llamar a Blotato ni publicar los medios. Permite detectar errores estructurales, de assets, cuentas y fechas antes de programar.

### Publicación

Ejecutar `2-motor` en modo `live` únicamente después de revisar el `dry`.

Requisitos para una semana:

- `estado: aprobado` en la semana;
- `aprobado_por` informado;
- `aprobado_en` en ISO 8601;
- assets visuales existentes;
- cuentas y secretos configurados.

Requisitos para `todas`:

- las cuatro semanas completas;
- aprobación raíz del manifiesto;
- assets de todo el ciclo.

## 4. Horarios

La zona horaria editorial es `America/Argentina/Buenos_Aires`. El sistema convierte los horarios locales a UTC antes de enviarlos a Blotato.

Valores actuales:

- LinkedIn de Paulo: 09:00.
- Instagram de Motion: 12:00.

## 5. Fuentes de verdad

- Estrategia: `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- Corpus y evidencia: `knowledge/MASTER_BASE_CONOCIMIENTO.md` en la base del proyecto; el repositorio conserva una referencia, no una copia operativa.
- Ejecución: manifiesto y semana aprobados.
- Aprendizaje editorial operativo: `docs/AUDITORIA_EDITORIAL.md`.

`docs/AUDITORIA_EDITORIAL.md` conserva correcciones estructurales, pares borrador → versión final y controles de voz. No redefine estrategia ni reemplaza el corpus.

Los archivos de `archive/` no se consultan en producción.

## 6. Control editorial

Antes de aprobar una pieza:

1. consultar `docs/AUDITORIA_EDITORIAL.md`;
2. revisar los controles editoriales activos;
3. incorporar las correcciones del usuario como una entrada nueva cuando tengan valor estructural;
4. clasificar el alcance como `local`, `recurrente` o `general`;
5. cerrar la entrada únicamente cuando exista una versión final aprobada para comparar contra el borrador.

La auditoría es acumulativa. No se usa para convertir cada corrección aislada en una regla permanente.

## 7. Subsistema de video

Los workflows, prompts y pipelines de creación y edición de reels se mantienen sin cambios y operan de forma independiente. Esta operación no modifica:

- workflows `3-*`, `4-*`, `5-*` ni `debug-frame`;
- `pipelines/video/`;
- `scripts/PROMPT_editor_video.md`;
- procesamiento, corte, subtitulado, render o catalogación de reels.

## 8. Recuperación

La rama `backup/pre-canonica-2026-07-13` conserva el estado completo anterior a esta reorganización. Los archivos retirados se documentan en `archive/2026-07-pre-canonica/README.md`.
