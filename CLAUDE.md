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

## Fuente persistente de verdad

- La conversación con Paulo es el canal de decisión, corrección y aprobación.
- GitHub es la memoria persistente y gobernada del sistema.
- Una decisión estratégica, editorial o metodológica confirmada por Paulo debe incorporarse al archivo canónico correspondiente en GitHub para que gobierne iteraciones futuras.
- Los documentos adjuntos al proyecto, copias descargadas o versiones históricas no gobiernan el flujo activo cuando contradicen los archivos vigentes de GitHub.
- No es necesario que Paulo descargue, edite y vuelva a cargar documentos para actualizar el sistema: la actualización se realiza en GitHub con trazabilidad.
- **Una conversación nueva no puede depender de recordar reglas de chats anteriores. Antes de producir contenido, se releen las fuentes vigentes del repositorio.**

## Modelo operativo vigente

- La estrategia y el plan editorial se definen mediante conversación estratégica y aprobación humana.
- Los bancos de situaciones, artefactos, conceptos, evidencias y hooks se actualizan de forma acumulativa desde las interacciones con Paulo.
- Antes de redactar se consulta: estrategia → situación → concepto o artefacto → evidencia → guía de storytelling → **contrato cognitivo de storytelling** → guía y banco de hooks → corpus de voz correspondiente → auditoría.
- La tesis gobierna la perspectiva semanal. Cada publicación debe funcionar de forma autónoma y no como un capítulo incompleto de una historia serial.
- Storytelling define cómo avanza la pieza. Problema, Método, Resultados o Conexión definen qué efecto debe producir.
- Antes de redactar se declaran `efecto_editorial`, `centro_narrativo`, `punto_de_llegada`, fuente y evidencia.
- **Antes de proponer hooks o copy final se resuelve obligatoriamente la arquitectura cognitiva definida en `knowledge/guides/CONTRATO_COGNITIVO_STORYTELLING.md`: conocimiento inicial, idea nueva dominante, puente cognitivo, jerarquía de ideas, secuencia conocido → nuevo, economía explicativa, estado mental del lector y comprensión final.**
- **Si el preflight cognitivo está incompleto, el agente no redacta el copy final.** Vuelve al diseño editorial.
- Para cada pieza se proponen tres hooks con mecanismos diferentes, salvo que el copy ya esté aprobado o bloqueado. Los hooks se diseñan después de resolver el puente cognitivo.
- Para contenido de Paulo y captions de Instagram se relee `strategy/VOZ_corpus.md` antes de escribir; el contrato cognitivo organiza la comprensión y el corpus gobierna la expresión.
- No toda pieza debe incluir por qué importa, qué hace Motion, caso real, cómo y oferta completos. El tipo editorial define qué bloques se utilizan y dónde termina la pieza.
- Todo CTA surge del argumento y se adapta al canal.
- LinkedIn e Instagram reciben textos propios y adaptados a sus audiencias antes del bloqueo del copy.
- Una pieza no pasa el gate si es una lista estilizada de frases o áreas, si acumula slogans sin progresión, si hay varias ideas dominantes, si aparecen conceptos sin puente o si el ritmo se fabrica mediante una oración por línea.
- Los marcos externos de storytelling pueden aportar criterios puntuales, pero no se usan como plantilla narrativa por defecto ni reemplazan la voz real de Motion.
- Cuando Paulo aprueba o pide mantener literalmente una versión, se registra `copy_locked: true` y la ruta de la fuente.
- Con copy bloqueado se puede segmentar y adaptar el CTA; no se puede regenerar, reordenar, cambiar la persona narrativa ni agregar conceptos.
- Después de una corrección relevante de Paulo, el agente debe explicitar la conclusión estratégica del aprendizaje, clasificar su alcance como local, recurrente o general y proponer o ejecutar la actualización del archivo correspondiente.
- El input de producción es `manifiestos/mes_<YYYY-MM>.json`.
- GitHub valida, diseña, renderiza y programa.
- Ningún workflow puede reescribir copies, tesis, buyer, oferta, contrato narrativo o estrategia.
- Nada se programa en `live` sin aprobación explícita.

## Archivos principales

- Estrategia: `strategy/ESTRATEGIA_MOTION_CANONICA.md`.
- Arquitectura y actualización del conocimiento: `knowledge/README.md`.
- Índice del Master: `knowledge/MASTER_BASE_CONOCIMIENTO.md`.
- Situaciones: `knowledge/banks/BANCO_SITUACIONES_MOTION.md`.
- Artefactos: `knowledge/banks/BANCO_ARTEFACTOS_MOTION.md`.
- Conceptos: `knowledge/banks/BANCO_CONCEPTOS_MOTION.md`.
- Evidencias: `knowledge/banks/BANCO_EVIDENCIAS_MOTION.md`.
- Hooks: `knowledge/banks/BANCO_HOOKS_MOTION.md`.
- Storytelling: `knowledge/guides/GUIA_OPERATIVA_STORYTELLING.md`.
- **Contrato cognitivo obligatorio:** `knowledge/guides/CONTRATO_COGNITIVO_STORYTELLING.md`.
- Guía de hooks: `knowledge/guides/GUIA_OPERATIVA_HOOKS.md`.
- Voz: `strategy/VOZ_corpus.md`.
- Agente redactor: `skills/02-redactor.md`.
- Auditoría editorial: `docs/AUDITORIA_EDITORIAL.md`.
- Proceso editorial: `docs/PROCESO_CONTENIDOS_Y_CONOCIMIENTO.md`.
- Contrato: `docs/CONTRATO_MANIFIESTO_MENSUAL.md`.
- Operación: `docs/OPERACION_REPOSITORIO.md`.
- Validador: `scripts/mes.py`.
- Preparación visual: `scripts/PROMPT_preparar_assets_mes.md`.
- Render: `scripts/generar_carrusel_mes.py`.
- Publicación: `scripts/publicador_mes.py`.

## Regla de entrada para una nueva conversación o agente

Antes de generar una pieza editorial nueva:

1. releer estrategia y las fuentes relevantes del tema;
2. releer `GUIA_OPERATIVA_STORYTELLING.md` y `CONTRATO_COGNITIVO_STORYTELLING.md`;
3. releer la guía de hooks;
4. releer `VOZ_corpus.md` cuando corresponda;
5. completar el preflight cognitivo;
6. recién entonces construir hooks y copy.

Una publicación anterior puede calibrar el sistema, pero nunca habilita a omitir estos pasos. La memoria conversacional es complementaria; **GitHub gobierna la ejecución futura**.

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
- No usar el formato como permiso para reescribir una fuente aprobada.
- No saltear la arquitectura cognitiva porque el tema parezca simple, exista un copy similar o haya poco tiempo.

## Compatibilidad temporal

Los archivos estratégicos anteriores que permanecen en `strategy/` se conservan únicamente cuando algún subsistema técnico todavía los consulta. No gobiernan el flujo editorial activo.
