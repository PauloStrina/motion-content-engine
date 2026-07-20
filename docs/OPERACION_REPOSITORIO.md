# OPERACIÓN DEL REPOSITORIO

## 1. Responsabilidad del sistema

El repositorio ejecuta un plan mensual y conceptos visuales ya definidos. No reemplaza la conversación estratégica, editorial ni de dirección de arte.

La estrategia se organiza por mes. La producción, aprobación y programación pueden realizarse por semana para conservar flexibilidad operativa.

Entradas:

```text
manifiestos/mes_<YYYY-MM>.json
design-system/concepts/<YYYY-MM>/<piece_id>/concept.json
```

Salidas:

- recursos conceptuales en `design-system/generated/`;
- especificaciones visuales en `design-system/slides/`;
- PNG de carruseles;
- medios publicados en `motion-media`;
- publicaciones programadas en Blotato;
- newsletters listas para publicación manual.

## 2. Aprobaciones separadas

El copy y el concepto visual se aprueban de forma independiente.

Una pieza puede tener:

- contenido aprobado y visual pendiente;
- visual aprobado y contenido pendiente;
- ambos aprobados y listos para producción.

El repositorio no corrige ninguna de las dos capas.

## 3. Alcances de ejecución

### Semana específica

Seleccionar `semana: 1`, `2`, `3` o `4`.

El sistema valida, diseña, renderiza y programa únicamente esa semana. La semana debe estar aprobada en su propio nodo. El manifiesto raíz y las semanas futuras pueden permanecer en borrador.

### Ciclo completo

Seleccionar `semana: todas`.

El sistema exige las cuatro semanas, secuencia completa y aprobación raíz del manifiesto.

## 4. Flujo

### Conceptualización

Se realiza fuera del repositorio:

1. definir contenido;
2. proponer una hipótesis visual;
3. generar un preview;
4. aprobar el concepto;
5. guardar el contrato en `design-system/concepts/`.

### Generación conceptual opcional

Ejecutar `1a-generar-imagen-conceptual` únicamente para contratos con modo `openai` o `hybrid`.

El workflow:

1. valida el contrato;
2. reutiliza el preview aprobado cuando el modo exige fidelidad exacta;
3. genera o edita el recurso con OpenAI cuando corresponde;
4. guarda el asset y sus metadatos;
5. no publica.

### Preparación

Ejecutar `1-preparar-assets` con:

- `mes`: ciclo editorial `YYYY-MM`;
- `semana`: número de semana o `todas`.

El workflow:

1. valida estructura y aprobación del alcance;
2. valida los contratos visuales cuando están habilitados;
3. lee únicamente el manifiesto, el contrato visual y el sistema de diseño;
4. genera las especificaciones visuales necesarias;
5. verifica que el copy no haya sido alterado;
6. commitea solo archivos de `design-system/slides/`.

Cuando las especificaciones visuales ya existen y pasan validación, este paso puede omitirse.

### Prueba

Ejecutar `2-motor` en modo `dry` para la misma semana.

El workflow valida contratos, renderiza y simula la programación sin llamar a Blotato ni publicar medios.

### Publicación

Ejecutar `2-motor` en modo `live` únicamente después de revisar el `dry`.

Requisitos:

- alcance editorial aprobado;
- contratos visuales aprobados cuando `contrato_visual_version: 1`;
- assets visuales existentes;
- cuentas y secretos configurados.

## 5. Modos de ejecución visual

- `code`: render determinístico.
- `openai`: generación o edición de recurso.
- `hybrid`: recurso generativo más composición en código.
- `reuse`: uso directo del asset aprobado.

La composición final, los textos, los logos y los diagramas exactos permanecen determinísticos.

## 6. Horarios

La zona horaria editorial es `America/Argentina/Buenos_Aires`. El sistema convierte los horarios locales a UTC antes de enviarlos a Blotato.

Valores actuales:

- LinkedIn de Paulo: 09:00.
- Instagram de Motion: 12:00.

## 7. Fuentes de verdad

- Estrategia: `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- Corpus y evidencia: Master activo del proyecto, referenciado en `knowledge/MASTER_BASE_CONOCIMIENTO.md`.
- Lenguaje visual: `design-system/visual-language/`.
- Concepto por pieza: `design-system/concepts/`.
- Ejecución: manifiesto y alcance aprobados.
- Aprendizaje editorial operativo: `docs/AUDITORIA_EDITORIAL.md`.

Las referencias de `design-system/references/` no gobiernan una pieza y no pueden copiarse.

## 8. Control editorial

Antes de aprobar una pieza:

1. consultar `docs/AUDITORIA_EDITORIAL.md`;
2. revisar controles editoriales;
3. validar copy;
4. validar hipótesis visual;
5. guardar cada aprobación;
6. cerrar únicamente cuando exista una versión final.

## 9. Subsistema de video

Los workflows, prompts y pipelines de creación y edición de reels se mantienen sin cambios.

Los futuros motion graphics conceptuales deberán leer el mismo contrato visual, pero no sustituirán el pipeline actual.

## 10. Configuración sensible

Las credenciales necesarias para generación, publicación y acceso a medios se configuran exclusivamente en los secretos del repositorio. Nunca se guardan en manifiestos, contratos, prompts o commits.

## 11. Recuperación

La rama `backup/pre-canonica-2026-07-13` conserva el estado completo anterior a la reorganización canónica.
