# MOTION CONTENT ENGINE

Repositorio operativo para producir y programar contenido de Motion a partir de un **manifiesto mensual aprobado**.

## Fuentes activas

- `strategy/ESTRATEGIA_MOTION_CANONICA.md`: única fuente de verdad estratégica.
- `knowledge/MASTER_BASE_CONOCIMIENTO.md`: referencia a la base de conocimiento activa del proyecto.
- `manifiestos/mes_<YYYY-MM>.json`: contrato operativo aprobado para cada mes.

La estrategia y los textos se definen fuera del repositorio. GitHub no decide qué comunicar ni redacta el mes: valida el manifiesto, genera especificaciones visuales, renderiza assets y programa las publicaciones.

## Flujo mensual

1. Definir y aprobar el plan de 16 publicaciones.
2. Cargar `manifiestos/mes_<YYYY-MM>.json` con `estado: aprobado`.
3. Ejecutar `1-preparar-assets-mensuales`.
4. Revisar los archivos de diseño generados.
5. Ejecutar `2-motor-mensual` en modo `dry`.
6. Revisar el resultado.
7. Ejecutar `2-motor-mensual` en modo `live`.

El modo `live` se bloquea si el manifiesto no está aprobado.

## Alcance activo

- LinkedIn de Paulo.
- Instagram de Motion.
- Carruseles, posts largos, captions, newsletters manuales y programación por Blotato.
- Sistema de diseño en código.

## Video

El subsistema de creación y edición de video se conserva sin cambios. Sus workflows, prompts, pipelines y banco de reels siguen operando de forma independiente.

## Estructura

- `.github/workflows/`: preparación de assets, publicación mensual y subsistema de video.
- `strategy/`: estrategia canónica y archivos de compatibilidad del subsistema de video.
- `knowledge/`: referencia a la base de conocimiento fuente.
- `manifiestos/`: inputs mensuales aprobados.
- `design-system/`: identidad visual, especificaciones y render.
- `scripts/`: validación, render y publicación.
- `pipelines/video/`: creación y edición de reels; fuera del alcance de esta refactorización.
- `archive/`: manifiesto de documentación y automatizaciones discontinuadas.

## Reglas operativas

- Nada se publica sin aprobación humana.
- `dry` no toca Blotato ni hace push a `motion-media`.
- `live` exige `estado: aprobado`, `aprobado_por` y `aprobado_en`.
- Los copies viven en el manifiesto. El diseñador no puede reescribirlos.
- Las API keys viven únicamente en GitHub Secrets.
- `archive/**` nunca se usa como fuente activa.

Ver `docs/OPERACION_REPOSITORIO.md` y `docs/CONTRATO_MANIFIESTO_MENSUAL.md`.
