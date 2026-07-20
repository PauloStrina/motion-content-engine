# MOTION CONTENT ENGINE

Repositorio operativo para producir y programar contenido de Motion a partir de un **manifiesto mensual aprobado**.

## Fuentes activas

- `strategy/ESTRATEGIA_MOTION_CANONICA.md`: única fuente de verdad estratégica.
- `knowledge/MASTER_BASE_CONOCIMIENTO.md`: referencia a la base de conocimiento activa del proyecto.
- `manifiestos/mes_<YYYY-MM>.json`: contrato operativo aprobado para cada mes.
- `design-system/visual-language/`: principios y repertorio visual operativo.
- `design-system/concepts/`: contratos visuales aprobados por pieza.

La estrategia, los textos y la conceptualización visual se definen fuera del repositorio. GitHub no decide qué comunicar ni inventa el concepto: valida el manifiesto y el contrato visual, genera o compone recursos aprobados, renderiza assets y programa las publicaciones.

## Flujo mensual

1. Definir y aprobar el plan editorial.
2. Validar copy e hipótesis visual en la conversación estratégica.
3. Cargar `manifiestos/mes_<YYYY-MM>.json`.
4. Guardar el contrato visual aprobado en `design-system/concepts/`.
5. Cuando corresponda, ejecutar `1a-generar-imagen-conceptual`.
6. Ejecutar `1-preparar-assets`.
7. Revisar las especificaciones y previews.
8. Ejecutar `2-motor` en modo `dry`.
9. Revisar el resultado.
10. Ejecutar `2-motor` en modo `live`.

El modo `live` se bloquea si el alcance no está aprobado. Los manifiestos anteriores siguen siendo compatibles; el contrato visual se exige cuando el manifiesto declara `contrato_visual_version: 1`.

## Alcance activo

- LinkedIn de Paulo.
- Instagram de Motion.
- Carruseles, posts largos, captions, newsletters manuales y programación por Blotato.
- Sistema de diseño en código.
- Recursos conceptuales generados con OpenAI cuando el contrato visual aprobado lo indica.

## Video

El subsistema de creación y edición de video se conserva sin cambios. Sus workflows, prompts, pipelines y banco de reels siguen operando de forma independiente. Los motion graphics conceptuales se incorporarán sobre el contrato visual común, sin reemplazar el pipeline actual de reels.

## Estructura

- `.github/workflows/`: preparación de assets, generación conceptual, publicación mensual y subsistema de video.
- `strategy/`: estrategia canónica y archivos de compatibilidad del subsistema de video.
- `knowledge/`: referencia a la base de conocimiento fuente.
- `manifiestos/`: inputs mensuales aprobados.
- `design-system/visual-language/`: principios, recursos y criterios de uso.
- `design-system/concepts/`: especificaciones visuales aprobadas.
- `design-system/generated/`: recursos generativos trazables.
- `design-system/references/`: referencias visuales, solo para inspiración.
- `design-system/slides/`: especificaciones de render por carrusel.
- `scripts/`: validación, generación, render y publicación.
- `pipelines/video/`: creación y edición de reels.
- `archive/`: documentación y automatizaciones discontinuadas.

## Reglas operativas

- Nada se publica sin aprobación humana.
- El copy y el concepto visual se aprueban por separado.
- Una referencia inspira; no se copia ni se usa como asset final sin licencia.
- Una imagen aprobada se reutiliza o se edita; no se regenera desde cero si se necesita fidelidad.
- `dry` no toca Blotato ni hace push a `motion-media`.
- `live` exige `estado: aprobado`, `aprobado_por` y `aprobado_en`.
- Los copies viven en el manifiesto. Diseño y render no pueden reescribirlos.
- Las API keys viven únicamente en GitHub Secrets.
- `archive/**` nunca se usa como fuente activa.

Ver:

- `docs/OPERACION_REPOSITORIO.md`
- `docs/CONTRATO_MANIFIESTO_MENSUAL.md`
- `docs/CONTRATO_CONCEPTO_VISUAL.md`
