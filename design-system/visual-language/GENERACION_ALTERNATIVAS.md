# GENERACIÓN DE ALTERNATIVAS VISUALES

**Estado:** regla permanente de producción visual
**Precedencia:** subordinado a `PRINCIPIOS.md` y a `FAMILIAS_VISUALES.md`
**Decisión:** Paulo, 2026-08-07

## 1. Regla

Toda pieza visual se produce en cuatro direcciones. Sin excepción y sin necesidad de pedirlo.

| | Origen | Qué es | Estado |
|---|---|---|---|
| **A** | gramática, código | composición canónica dentro del lenguaje vigente | publicable sin retrabajo |
| **B** | Claude Design | exploración con hipótesis conceptual declarada | requiere portado |
| **C** | Claude Design | exploración con hipótesis conceptual declarada | requiere portado |
| **D** | Claude Design | exploración con hipótesis conceptual declarada | requiere portado |

A existe siempre y se publica por defecto. Si Paulo no revisa las alternativas, la pieza sale igual: **la exploración nunca bloquea la producción.**

## 2. Por qué B, C y D salen de Claude Design y no de la gramática

La gramática compone dentro del lenguaje ya definido. Sirve para variar, no para inventar.

Claude Design puede proponer recursos formales que la gramática todavía no sabe dibujar. Ese es el punto de la regla: que cada semana entre una posibilidad de ampliar el lenguaje, no solo de recorrerlo.

Costo aceptado explícitamente: Claude Design no expone API ni MCP. El paso es manual en todas las piezas.

## 3. Las alternativas no son variaciones cosméticas

Cada alternativa se genera desde una **lectura conceptual distinta de la misma frase**, y esa lectura se declara por escrito antes de componer.

Ejemplo sobre `La dirección aprobó el rumbo. Pero cada área conserva sus presupuestos, prioridades e indicadores.`

- A — inercia: algo se mueve y vuelve al mismo punto.
- B — fragmentación: partes sin conexión entre sí.
- C — ausencia de centro: el vacío como sujeto de la composición.
- D — contraste entre acuerdo declarado y decisión real.

Una alternativa sin hipótesis escrita no es una alternativa. No se presenta.

## 4. Escala de la comparación

Las alternativas se juegan a nivel de **dirección visual de la pieza**, no placa por placa.

Cada dirección se muestra sobre tres placas representativas: portada, una placa de desarrollo y el cierre. La lámina comparativa tiene entonces doce recuadros y se decide de una mirada.

La dirección elegida se aplica después a todas las placas de la pieza.

Excepción: cuando una placa concentra el argumento, se generan alternativas solo para ella.

## 5. Promoción de una alternativa elegida

Cuando Paulo elige B, C o D, **no se guarda la forma**. Guardar formas reconstruye un catálogo cerrado y devuelve el problema de la repetición.

Se promueve el **principio compositivo**:

- qué relación conceptual resuelve;
- con qué recursos gráficos;
- qué debe preservarse siempre;
- qué queda libre para variar.

Se escribe como dirección del lenguaje en `design-system/visual-language/`, con la misma jerarquía que `line_system` y `conceptual_art`. A partir de ahí se compone *en* esa dirección, siempre distinto.

Crece el rango expresivo del sistema, nunca su inventario.

## 6. Registro de lo descartado

Las alternativas no elegidas se registran con su hipótesis y el motivo del descarte.

Sirven para no volver a proponer lo mismo, y para detectar patrones: si un mismo tipo de mensaje acumula rechazos, la conclusión se escribe en el lenguaje visual y cambia el default.

## 7. Cuándo el lenguaje no alcanza

Tres señales, ninguna basada en juicio estético del agente:

1. **Recurso prohibido.** El copy exige `forces`, `object_metaphor`, `photo_intervention`, `layers` o `generative`, que `FAMILIAS_VISUALES.json` excluye de `line_system`. Es el caso de cultura, fricción, resistencia y experiencia humana.
2. **Distancia geométrica mínima.** Las cuatro alternativas caen dentro del vecindario de lo ya publicado. Medición, no impresión: el lenguaje se agotó para esa idea.
3. **Rechazo acumulado.** Paulo descarta las cuatro. Si se repite para un tipo de mensaje, se registra como patrón.

Ninguna de las tres detecta "correcto pero aburrido". Esa evaluación es de Paulo y por eso la decisión final no se automatiza.

## 8. Contrato con Claude Design

El brief de cada pieza se genera desde el repo y se carga junto a `design-system/claude-design/CONTRATO_CLAUDE_DESIGN.md`, que traslada paleta, tipografías, reglas de no solapamiento, firma y formato de salida.

Con ese contrato, portar la salida de Claude Design a la gramática es traducción mecánica y no rediseño.
