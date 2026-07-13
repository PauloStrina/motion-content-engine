# AUDITORÍA EDITORIAL Y APRENDIZAJE DE VOZ

## 1. Propósito

Este documento registra correcciones editoriales estructurales y aprendizajes de voz surgidos del trabajo entre Paulo y MOTION MKT Copilot.

No reemplaza ni redefine:

- la estrategia vigente de `strategy/ESTRATEGIA_MOTION_CANONICA.md`;
- el corpus, la evidencia ni la voz contenidos en la base `MASTER_BASE_CONOCIMIENTO.md`;
- la aprobación humana de cada pieza.

Su función es operativa: conservar trazabilidad sobre qué patrones se corrigieron, por qué, con qué alcance y cómo deben auditarse en piezas futuras.

## 2. Reglas de uso

1. Se consulta antes de redactar y antes de aprobar una pieza.
2. Cada entrada conserva el par borrador → versión final aprobada.
3. Si la versión final aún no existe, la entrada queda `abierta`.
4. Las entradas se agregan; no se eliminan por conveniencia editorial.
5. Una corrección aislada no se convierte automáticamente en regla general.
6. El alcance debe clasificarse como:
   - `local`: aplica solo a una pieza;
   - `recurrente`: patrón a observar en futuras piezas;
   - `general`: regla estructural explícitamente aprobada.
7. Las reglas activas deben expresarse como criterios de auditoría, no como fórmulas obligatorias de redacción.
8. Este documento no debe copiar definiciones estratégicas ya contenidas en la estrategia canónica.

## 3. Flujo de aprendizaje

```text
borrador
→ devolución del usuario
→ versión final aprobada
→ análisis de cambios
→ clasificación del alcance
→ incorporación como control editorial
```

## 4. Plantilla de entrada

```markdown
### AE-AAAA-MM-DD-NNN — Título breve

- Fecha:
- Pieza:
- Canal:
- Estado: abierta | cerrada
- Alcance: local | recurrente | general
- Disparador:

#### Borrador observado

> Fragmento o patrón relevante.

#### Devolución del usuario

- Corrección 1.
- Corrección 2.

#### Versión final aprobada

> Pendiente o texto final.

#### Análisis del cambio

- Qué cambió.
- Por qué cambió.
- Qué no debe generalizarse.

#### Control editorial derivado

- Criterio verificable antes de aprobar futuras piezas.
```

## 5. Controles editoriales activos

### CE-001 — Evitar la forma estandarizada de “post de LinkedIn generado por IA”

- Estado: activo.
- Alcance: general.
- Origen: instrucción explícita de Paulo del 12 de julio de 2026.

Antes de aprobar una pieza, verificar:

- que la apertura no dependa automáticamente de fórmulas como `El problema no es X, es Y`;
- que el ritmo no se construya mediante una sucesión de frases cortas separadas por saltos dobles;
- que no exista una oración individual por párrafo como patrón dominante;
- que los saltos de línea respondan al argumento y no a una dramatización prefabricada;
- que la pieza pueda leerse como prosa natural, aun antes de adaptarla al canal;
- que exista una escena, observación, experiencia o razonamiento concreto de Motion;
- que la estructura no pueda reutilizarse casi sin cambios para cualquier otro tema.

Este control no prohíbe los contrastes, las frases breves ni los párrafos de una sola oración. Exige que su uso sea deliberado y excepcional, no el molde predeterminado.

## 6. Entradas de auditoría

### AE-2026-07-12-001 — Lanzamiento de la serie Transformación Continua

- Fecha: 2026-07-12.
- Pieza: publicación inicial de la semana de Transformación Continua.
- Canal: LinkedIn.
- Estado: abierta.
- Alcance: general.
- Disparador: el borrador fue identificado por Paulo como una redacción estandarizada y fácilmente reconocible como generada por IA.

#### Borrador observado

> El problema no es que los proyectos terminen. Es creer que la transformación también termina.

El resto de la pieza utilizaba frases breves, párrafos de una sola oración y saltos dobles de línea como recurso principal de ritmo.

#### Devolución del usuario

- La apertura `El problema no es X, es Y` está saturada en LinkedIn.
- Las frases cortas con puntos y saltos de línea reproducen un patrón reconocible de contenido generado por IA.
- Las oraciones individuales separadas por dos saltos de línea vuelven artificial la voz.

#### Versión final aprobada

> Pendiente.

#### Análisis del cambio

La falla no estuvo en el concepto estratégico, sino en haberlo convertido demasiado pronto en una plantilla de canal. El contenido debe reconstruirse desde una situación, observación o razonamiento concreto y redactarse primero como prosa natural. Solo después corresponde adaptarlo al formato de LinkedIn.

#### Control editorial derivado

Aplicar `CE-001` a todas las piezas futuras y cerrar esta entrada únicamente cuando exista una versión final aprobada para comparar contra el borrador.