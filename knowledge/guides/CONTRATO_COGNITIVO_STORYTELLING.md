# CONTRATO COGNITIVO DE STORYTELLING — MOTION

**Estado:** vigente  
**Versión:** 1.0  
**Fecha:** 7 de agosto de 2026  
**Alcance:** regla operativa general para toda pieza editorial nueva de Motion.  
**Precedencia:** instrucción explícita más reciente de Paulo → `strategy/ESTRATEGIA_MOTION_CANONICA.md` → bancos activos → `GUIA_OPERATIVA_STORYTELLING.md` + este contrato → guía de hooks → auditoría editorial → documentación técnica.

## 1. Propósito

Este contrato agrega una capa obligatoria entre el diseño editorial y la redacción. Su función es asegurar que una pieza no sea solamente correcta en tesis, tipo y voz, sino que produzca una progresión de comprensión clara en la mente del lector.

No redefine estrategia, tesis, buyer, oferta, modelo editorial ni voz. Tampoco reemplaza `GUIA_OPERATIVA_STORYTELLING.md`: la complementa y vuelve explícita la arquitectura cognitiva que debe existir antes de redactar.

> **No se redacta el copy final hasta que la arquitectura cognitiva esté resuelta.**

## 2. Decisión editorial incorporada

La síntesis operativa surge de los principios de claridad y progresión cognitiva revisados en las lecturas de storytelling y estilo, combinados con el sistema narrativo propio de Motion.

Se incorporan como reglas permanentes:

- diseñar desde lo que el lector ya sabe hacia una única comprensión nueva;
- construir un puente cognitivo sin saltos argumentales;
- jerarquizar ideas principales, subordinadas y ejemplos;
- asegurar que cada párrafo derive del anterior y haga avanzar el pensamiento;
- explicar solamente lo necesario para producir la comprensión buscada;
- revisar la pieza desde el estado mental del lector, no desde la intención del redactor;
- conservar escena, tensión y movimiento cuando ayudan a comprender, sin convertirlos en una fórmula fija.

Los marcos externos revisados no se convierten en templates de escritura. En particular, estructuras reconocibles de data-storytelling o fórmulas muy estandarizadas pueden aportar criterios puntuales de jerarquía, pero **no gobiernan la gramática narrativa de Motion**. La pieza debe sonar a una persona pensando desde experiencia real, no a una IA aplicando un framework.

## 3. Arquitectura cognitiva obligatoria

Antes de proponer hooks o redactar, cada pieza debe resolver ocho campos.

### 3.1 Conocimiento inicial del lector

Definir qué puede darse por conocido para ese buyer y esa situación. No explicar nuevamente lo que el lector ya vive o comprende salvo que sea necesario para el reencuadre.

Pregunta de control:

> ¿Qué entiende ya el Visionario antes de empezar a leer?

### 3.2 Idea nueva dominante

Definir una sola comprensión nueva que la pieza busca instalar. Puede haber ideas subordinadas, pero no múltiples tesis compitiendo por el centro.

Pregunta de control:

> Si el lector recuerda una sola cosa mañana, ¿cuál debe ser?

### 3.3 Puente cognitivo

Describir el recorrido que conecta el conocimiento inicial con la idea nueva. Debe poder expresarse como una secuencia causal o lógica breve, no como una acumulación de frases correctas.

Ejemplo abstracto:

```text
situación conocida
→ tensión o contradicción
→ relación menos visible
→ nueva comprensión
```

### 3.4 Jerarquía de ideas

Separar:

- **idea principal:** la comprensión que gobierna la pieza;
- **ideas subordinadas:** las que la sostienen;
- **ejemplos o evidencia:** los que la vuelven visible o demostrable.

Un ejemplo no puede convertirse accidentalmente en la tesis. Una idea secundaria no debe recibir el mismo peso que la principal.

### 3.5 Secuencia conocido → nuevo

Cada idea nueva debe apoyarse en algo que ya quedó establecido. Si un párrafo introduce un concepto que no deriva de lo anterior, debe agregarse el puente necesario o eliminarse.

### 3.6 Economía explicativa

Definir explícitamente:

- qué necesita explicarse;
- qué puede omitirse;
- qué concepto, aunque sea correcto, desviaría la pieza.

La calidad no aumenta por cantidad de conceptos. Una explicación se conserva únicamente si hace avanzar la comprensión dominante.

### 3.7 Estado mental del lector

Antes de aprobar el esqueleto, describir qué debería estar pensando el lector en tres momentos:

1. **apertura:** qué reconoce o qué pregunta se activa;
2. **desarrollo:** qué relación empieza a ver;
3. **cierre:** qué comprensión nueva queda instalada.

Este control obliga a evaluar la pieza desde la mente del lector y no desde lo que el redactor quiso decir.

### 3.8 Comprensión final

Debe existir una frase de control que responda:

> ¿Qué entiende ahora el lector que no entendía —o no había formulado— al comenzar?

La comprensión final debe ser coherente con `efecto_editorial`, `centro_narrativo` y `punto_de_llegada`.

## 4. Contrato mínimo previo a redacción

Toda pieza nueva debe poder declarar, al menos internamente o en su fuente editorial, este bloque antes del copy:

```json
{
  "tipo": "problema",
  "efecto_editorial": "reconocimiento",
  "centro_narrativo": "...",
  "punto_de_llegada": "...",
  "source_mode": "situacion_potencial",
  "source_refs": [],
  "evidence_id": null,
  "arquitectura_cognitiva": {
    "conocimiento_inicial": "...",
    "idea_nueva_dominante": "...",
    "puente_cognitivo": ["...", "...", "..."],
    "idea_principal": "...",
    "ideas_subordinadas": ["..."],
    "ejemplos_evidencia": ["..."],
    "omitir": ["..."],
    "lector_apertura": "...",
    "lector_desarrollo": "...",
    "lector_cierre": "...",
    "comprension_final": "..."
  },
  "copy_locked": false
}
```

No es obligatorio incorporar este objeto al manifiesto técnico si el schema vigente no lo soporta. Sí es obligatorio resolverlo antes de la redacción y conservarlo en el diseño o fuente editorial cuando se materialice una pieza en GitHub.

## 5. Orden operativo obligatorio

```text
Estrategia y tesis
→ Tipo + efecto + centro + punto de llegada
→ Fuente y evidencia
→ Arquitectura cognitiva
→ Esqueleto narrativo
→ Hooks
→ Redacción continua desde la voz real
→ Adaptación por canal
→ Gate cognitivo + storytelling + voz + evidencia
→ Aprobación humana
→ copy_locked
```

Los hooks se diseñan después del puente cognitivo. No se optimiza una apertura aislada antes de saber qué recorrido de comprensión debe abrir.

## 6. Gate cognitivo de rechazo

Una pieza **no está lista** si ocurre cualquiera de estas condiciones:

1. no puede identificarse una única idea nueva dominante;
2. el cuerpo es una lista estilizada de afirmaciones, áreas o slogans sin relación causal o progresiva;
3. dos o más ideas compiten por ser la conclusión;
4. un párrafo podría moverse a cualquier lugar sin alterar el razonamiento;
5. aparece información nueva sin puente desde lo ya establecido;
6. se explica algo obvio para el lector sin que esa explicación produzca un reencuadre;
7. el texto acumula conceptos correctos que no hacen avanzar la pieza;
8. el ritmo depende de una oración por línea o de cortes artificiales en lugar de la progresión del pensamiento;
9. el cierre repite el hook, pero no instala una comprensión nueva;
10. no puede describirse qué piensa el lector al abrir, durante el desarrollo y al cerrar;
11. la pieza suena a una plantilla reconocible antes que a la voz real de Paulo o Motion.

Si falla cualquiera de estos controles, se vuelve a la arquitectura cognitiva. No se corrige cosméticamente el copy.

## 7. Relación con la voz

Para `linkedin_paulo`, `x_paulo` y captions de Instagram se debe leer `strategy/VOZ_corpus.md` antes de redactar. El contrato cognitivo organiza la comprensión; el corpus gobierna cómo esa comprensión se expresa.

No usar este contrato para volver la escritura académica, explicativa o rígida. La voz de Paulo sigue priorizando escenas concretas, experiencia, antítesis, preguntas genuinas, párrafos conectados y lenguaje de conversación real.

## 8. Persistencia entre conversaciones

GitHub es la memoria gobernada del sistema. Por lo tanto:

- una conversación nueva no debe depender de recordar acuerdos de chats anteriores;
- antes de generar contenido nuevo, el agente debe releer la versión vigente de este contrato y de las guías que lo acompañan;
- no se puede omitir el preflight cognitivo porque el tema parezca simple o porque exista un copy parecido previo;
- una pieza aprobada sirve como calibración, no como plantilla para saltear el razonamiento;
- si una futura instrucción de Paulo cambia esta regla, primero se actualiza la fuente correspondiente en GitHub y luego se aplica el nuevo criterio.

## 9. Alcance del aprendizaje

Paulo confirmó esta arquitectura como **regla general**, no como corrección local de una publicación. Debe gobernar todas las piezas editoriales nuevas hasta que una instrucción posterior la modifique.
