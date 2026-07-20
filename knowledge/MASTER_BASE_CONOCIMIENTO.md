# MASTER BASE DE CONOCIMIENTO — ÍNDICE OPERATIVO

**Estado:** vigente como índice  
**Versión de referencia externa:** 2.2  
**Fecha:** 20 de julio de 2026

## 1. Función

El corpus completo de voz, publicaciones, transcripciones, materiales metodológicos y referencias visuales continúa en el Master del proyecto MOTION MKT Copilot.

Los activos que cambian durante la planificación editorial se gestionan desde GitHub para permitir trazabilidad y actualización continua:

- `banks/BANCO_SITUACIONES_MOTION.md`;
- `banks/BANCO_ARTEFACTOS_MOTION.md`;
- `banks/BANCO_EVIDENCIAS_MOTION.md`;
- `banks/BANCO_HOOKS_MOTION.md`;
- `guides/GUIA_OPERATIVA_HOOKS.md`;
- `../docs/AUDITORIA_EDITORIAL.md`.

## 2. Regla de no duplicación

- La estrategia se define únicamente en `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- El Master conserva corpus y material fuente.
- Los bancos conservan unidades operativas estructuradas.
- Las guías conservan criterios de creación.
- La auditoría conserva pares borrador → versión final y aprendizajes.
- Los manifiestos conservan únicamente contenido aprobado para producción.

## 3. Uso

Antes de crear contenido se consulta:

1. estrategia;
2. situación;
3. artefacto;
4. evidencia;
5. guía y banco de hooks;
6. corpus de voz cuando sea necesario;
7. auditoría editorial.

El repositorio no debe inventar contenido cuando una fuente necesaria no existe. Debe marcar el vacío o solicitar la información a Paulo.

## 4. Actualización

El procedimiento de actualización y sincronización entre los dos repositorios está definido en [`README.md`](README.md).

Los bancos se modifican de forma quirúrgica después de una confirmación, corrección o aprobación explícita. No se requiere volver a generar ni volver a cargar un Master completo por cada aprendizaje.