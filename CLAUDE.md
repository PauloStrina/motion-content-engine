# MOTION CONTENT ENGINE — CONTEXTO OPERATIVO

Este archivo orienta a los agentes que trabajan dentro del repositorio. No contiene ni redefine estrategia.

## Precedencia

1. Instrucción explícita del operador.
2. `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
3. La base `MASTER_BASE_CONOCIMIENTO.md` del proyecto MOTION MKT Copilot.
4. Documentación y código operativo.
5. `archive/**`, solo histórico.

## Modelo operativo vigente

- La estrategia, la matriz mensual y los textos se definen con aprobación humana fuera del repositorio.
- El input activo es `manifiestos/mes_<YYYY-MM>.json`.
- GitHub valida, diseña, renderiza y programa.
- Ningún agente puede cambiar copies, tesis, buyer, oferta ni estrategia.
- Cada canal usa el texto aprobado que figura en el manifiesto.
- Nada se programa en `live` sin `estado: aprobado`.

## Archivos principales

- Estrategia: `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- Referencia a conocimiento: `knowledge/MASTER_BASE_CONOCIMIENTO.md`.
- Contrato: `docs/CONTRATO_MANIFIESTO_MENSUAL.md`.
- Operación: `docs/OPERACION_REPOSITORIO.md`.
- Validador: `scripts/mes.py`.
- Preparación visual: `scripts/PROMPT_preparar_assets_mes.md`.
- Render: `scripts/generar_carrusel_mes.py`.
- Publicación: `scripts/publicador_mes.py`.

## Límites

- No leer ni reutilizar `archive/**` para generar contenido.
- No modificar el subsistema de video salvo instrucción explícita.
- No inventar texto para completar campos faltantes: el validador debe fallar.
- No modificar el manifiesto durante diseño o render.
- No alterar secretos, cuentas o configuraciones sin instrucción explícita.

## Compatibilidad temporal

Los archivos estratégicos anteriores que permanecen en `strategy/` se conservan únicamente porque el subsistema de video todavía los consulta. No gobiernan el flujo mensual y no deben ser leídos por los workflows de assets o publicación.
