# MOTION CONTENT ENGINE — CONTEXTO OPERATIVO

Este archivo orienta a los agentes que trabajan dentro del repositorio. No contiene ni redefine estrategia.

## Precedencia

1. Instrucción explícita más reciente de Paulo.
2. `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
3. Bancos activos de `knowledge/banks/`.
4. Guías de `knowledge/guides/` y corpus referenciado por `knowledge/MASTER_BASE_CONOCIMIENTO.md`.
5. `docs/AUDITORIA_EDITORIAL.md`.
6. Documentación y código operativo.
7. `archive/**`, solo histórico.

Ante contradicciones se aplica la fuente de mayor jerarquía y se señala el archivo que debe corregirse.

## Modelo operativo vigente

- La estrategia y el plan editorial se definen mediante conversación estratégica y aprobación humana.
- Los bancos de situaciones, artefactos, evidencias y hooks se actualizan de forma acumulativa desde las interacciones con Paulo.
- Antes de redactar se consulta: estrategia → situación → artefacto → evidencia → guía y banco de hooks → auditoría.
- Para cada pieza se proponen tres hooks con mecanismos diferentes.
- El copy final integra por qué importa, qué hace Motion, caso real, cómo y CTA dentro de un storytelling continuo.
- Todo CTA conecta con el Programa de Transformación Digital.
- LinkedIn e Instagram reciben textos propios y adaptados a sus audiencias.
- El input de producción es `manifiestos/mes_<YYYY-MM>.json`.
- GitHub valida, diseña, renderiza y programa.
- Ningún workflow puede reescribir copies, tesis, buyer, oferta o estrategia.
- Nada se programa en `live` sin aprobación explícita.

## Archivos principales

- Estrategia: `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- Arquitectura y actualización del conocimiento: `knowledge/README.md`.
- Índice del Master: `knowledge/MASTER_BASE_CONOCIMIENTO.md`.
- Situaciones: `knowledge/banks/BANCO_SITUACIONES_MOTION.md`.
- Artefactos: `knowledge/banks/BANCO_ARTEFACTOS_MOTION.md`.
- Evidencias: `knowledge/banks/BANCO_EVIDENCIAS_MOTION.md`.
- Hooks: `knowledge/banks/BANCO_HOOKS_MOTION.md`.
- Guía de hooks: `knowledge/guides/GUIA_OPERATIVA_HOOKS.md`.
- Auditoría editorial: `docs/AUDITORIA_EDITORIAL.md`.
- Contrato: `docs/CONTRATO_MANIFIESTO_MENSUAL.md`.
- Operación: `docs/OPERACION_REPOSITORIO.md`.
- Validador: `scripts/mes.py`.
- Preparación visual: `scripts/PROMPT_preparar_assets_mes.md`.
- Render: `scripts/generar_carrusel_mes.py`.
- Publicación: `scripts/publicador_mes.py`.

## Sincronización entre repositorios

La arquitectura de conocimiento se mantiene de manera idéntica en:

- `PauloStrina/motion-content-engine` como repositorio operativo primario;
- `ops-motionco/motion-content-engine` como espejo sincronizado.

Una actualización no se considera terminada hasta que existen PRs equivalentes, se validaron los diffs y ambos cambios fueron mergeados.

## Límites

- No leer ni reutilizar `archive/**` para generar contenido.
- No modificar el subsistema de video salvo instrucción explícita.
- No inventar texto para completar campos faltantes.
- No inventar situaciones como evidencia ni cifras como resultados.
- No modificar el manifiesto durante diseño o render.
- No alterar secretos, cuentas o configuraciones sin instrucción explícita.
- No convertir una corrección aislada en regla general sin declaración explícita o evidencia recurrente.
- No cargar información confidencial o identificable sin autorización explícita.

## Compatibilidad temporal

Los archivos estratégicos anteriores que permanecen en `strategy/` se conservan únicamente cuando algún subsistema técnico todavía los consulta. No gobiernan el flujo editorial activo.