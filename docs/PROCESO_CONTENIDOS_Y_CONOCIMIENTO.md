# PROCESO DE CONOCIMIENTO Y PRODUCCIÓN DE CONTENIDOS

## 1. Dos flujos relacionados

El sistema separa:

1. **aprendizaje y conocimiento:** actualiza estrategia, situaciones, artefactos, conceptos, evidencias, hooks, storytelling y auditoría;
2. **producción semanal:** convierte contenido aprobado en manifiestos, conceptos visuales, assets y programación.

La conversación con Paulo define criterio, correcciones y aprobación. GitHub es la memoria persistente y gobernada del sistema. No es necesario descargar y volver a cargar documentos para actualizar las reglas activas.

Los documentos adjuntos al proyecto o copias locales pueden servir como referencia histórica, pero no gobiernan cuando contradicen los archivos vigentes del repositorio.

## 2. Actualización de conocimiento desde el chat

Cuando Paulo aporta o corrige información:

1. identificar el aprendizaje;
2. formular la **conclusión estratégica del feedback**: qué principio mejora la calidad y qué cambia en futuras piezas;
3. clasificarlo como estrategia, situación, artefacto, concepto, evidencia, hook, storytelling o corrección editorial;
4. clasificar su alcance como `local`, `recurrente` o `general`;
5. verificar fuente, alcance, origen y autorización;
6. actualizar únicamente el archivo correspondiente;
7. mantener IDs estables y referencias cruzadas;
8. replicar la modificación en los dos repositorios;
9. abrir PRs equivalentes;
10. comparar los archivos relevantes;
11. mergear ambos PRs después de aprobación.

La conclusión estratégica debe explicitarse al usuario después de una corrección relevante, incluso cuando el cambio todavía no se haya incorporado al repositorio.

### Repositorios

- `PauloStrina/motion-content-engine`: operativo primario.
- `ops-motionco/motion-content-engine`: espejo de conocimiento y respaldo.

La arquitectura de conocimiento debe ser idéntica. La ejecución de publicación se realiza solo desde el repositorio primario para evitar programaciones duplicadas.

## 3. Diseño editorial de una semana

La tesis gobierna la perspectiva semanal. Cada publicación debe funcionar de forma autónoma: la semana no se redacta como una historia serial de cuatro capítulos.

### Paso 1 — Definir el contrato narrativo

Antes de proponer hooks o redactar, cada pieza debe declarar:

- tesis;
- tipo editorial: Problema, Método, Resultados o Conexión;
- efecto editorial buscado;
- centro narrativo;
- punto de llegada;
- canal y emisor;
- modo de fuente;
- referencias a situaciones, conceptos, artefactos o evidencias;
- estado inicial de `copy_locked`.

Estructura mínima:

```json
{
  "tipo": "problema",
  "efecto_editorial": "reconocimiento",
  "centro_narrativo": "tensión de autoridad transversal",
  "punto_de_llegada": "la legitimidad puede construirse produciendo evidencia",
  "source_mode": "situacion_potencial",
  "source_refs": [],
  "evidence_id": null,
  "copy_locked": false
}
```

La definición operativa se encuentra en `knowledge/guides/GUIA_OPERATIVA_STORYTELLING.md`.

### Paso 2 — Construir el esqueleto editorial

Para cada día se construye un esqueleto con:

- tres alternativas de hook;
- situación o escena;
- tensión o consecuencia;
- reencuadre de Motion;
- desarrollo compatible con el tipo editorial;
- conclusión;
- CTA.

Los bloques son un repertorio, no una lista obligatoria. El tipo define qué recibe mayor peso y dónde debe detenerse la pieza.

Controles por tipo:

- **Problema:** termina en una nueva comprensión y no explica el método completo.
- **Método:** utiliza el problema como contexto y concentra el desarrollo en decisiones y mecanismos.
- **Resultados:** parte de evidencia real y diferencia hecho, interpretación y aprendizaje.
- **Conexión:** genera afinidad desde una experiencia, postura, símbolo o decisión concreta.

La coherencia semanal surge de la tesis y de la relación entre método y evidencia. No se redacta una pieza sobre un caso que contradiga el método o la tesis de la semana.

### Paso 3 — Aprobar el diseño editorial

Paulo corrige o aprueba:

- tema;
- tipo y efecto editorial;
- centro narrativo;
- punto de llegada;
- hooks;
- situación;
- concepto o artefacto;
- evidencia;
- CTA;
- secuencia semanal.

No se redacta el copy final hasta que el diseño narrativo permite distinguir con claridad la función de la pieza.

### Paso 4 — Redactar copys reales

Se escriben versiones separadas para:

- LinkedIn de Paulo;
- Instagram de Motion;
- carruseles;
- newsletter cuando corresponda;
- guion o copy de reel.

El copy publicable se lee como storytelling continuo. No muestra los rótulos `Hook`, `Situación`, `Fricción`, `Reencuadre`, `Conclusión` o `CTA`.

Storytelling define cómo avanza la pieza. El tipo editorial define qué cambio debe producir en el lector. Por eso, una pieza no debe recorrer automáticamente problema, método, evidencia y oferta completos.

Cada párrafo debe justificar su presencia. Debe aportar al menos una de estas funciones:

- introducir la tensión;
- hacer avanzar la escena;
- explicar una distinción;
- mostrar un mecanismo;
- aportar evidencia;
- volver la idea aplicable;
- instalar una consecuencia;
- conectar naturalmente con el siguiente paso.

Los detalles obvios o previsibles no se desarrollan si no agregan una distinción nueva.

### Paso 5 — Aprobar, bloquear y aprender

Después de la aprobación:

- el copy queda congelado con `copy_locked: true`;
- se conserva la fuente exacta aprobada;
- los hooks se registran en el Banco de Hooks;
- los conceptos nuevos o adaptados se registran en el Banco de Conceptos;
- los hechos y cifras se registran en Evidencias;
- situaciones o artefactos nuevos se incorporan a sus bancos;
- las correcciones de voz y storytelling relevantes se registran en la Auditoría Editorial;
- se explicita la conclusión estratégica del feedback y se actualiza el archivo de GitHub que corresponda.

Con `copy_locked: true`, una adaptación puede segmentar, jerarquizar y crear variantes de CTA por canal. No puede regenerar el contenido desde un resumen, alterar el orden argumental, modificar la persona narrativa ni agregar conceptos no aprobados.

## 4. Carga en GitHub

La producción se realiza en una rama temática del repositorio primario.

Ejemplo:

```text
content/2026-07-semana-2
```

### Archivos a modificar o crear

1. `manifiestos/mes_2026-07.json`: agregar la semana sin alterar el histórico.
2. `editorial/`: conservar las fuentes aprobadas y bloqueadas cuando corresponda.
3. `newsletters/`: guardar la newsletter aprobada.
4. `banco/reels/catalogo.json`: reconciliar publicados manualmente y reservar reels de la semana.
5. `design-system/concepts/<mes>/<piece_id>/concept.json`: guardar la hipótesis visual aprobada.
6. `design-system/slides/`: especificaciones visuales finales, generadas o revisadas por el flujo de assets.
7. Bancos, guías y auditoría, únicamente si la semana produjo aprendizaje nuevo.

El manifiesto referencia la fuente aprobada; no debe convertirse en el único lugar donde exista el copy cuando la pieza se desarrolló y aprobó fuera de él.

## 5. Aprobaciones separadas

Cada pieza necesita:

- diseño narrativo aprobado;
- copy aprobado y bloqueado;
- concepto visual aprobado;
- evidencia autorizada;
- estado editorial aprobado en el manifiesto.

El repositorio no puede corregir automáticamente el copy, cambiar su tipo editorial, ampliar el punto de llegada ni decidir una nueva dirección de arte.

## 6. Flujo técnico

### 6.1 PR de contenido

1. crear rama;
2. cargar manifiesto, fuentes editoriales, newsletter, reservas de reels y contratos visuales;
3. validar JSON, referencias, fechas, estados, contrato narrativo y assets;
4. abrir PR;
5. revisar diff;
6. mergear a `main`.

### 6.2 Preparar assets

Ejecutar `1-preparar-assets` con:

```text
mes: 2026-07
semana: 2
```

El workflow valida el alcance, lee el copy aprobado, produce especificaciones visuales y no modifica el texto ni el contrato narrativo.

### 6.3 Dry run

Ejecutar `2-motor` con:

```text
mes: 2026-07
semana: 2
modo: dry
```

Revisar:

- fechas y horarios;
- canales;
- textos;
- copy bloqueado y fuente correcta;
- reels;
- orden y legibilidad de carruseles;
- coherencia entre tipo, narrativa y visual;
- URLs de medios;
- cantidad de publicaciones;
- fallback de piezas sin video.

### 6.4 Live

Solo después de aprobar el dry:

```text
mes: 2026-07
semana: 2
modo: live
```

La newsletter de LinkedIn permanece manual salvo que el flujo técnico incorpore una integración específica.

## 7. Reconciliación de publicaciones manuales

Antes de producir una nueva semana:

1. identificar qué piezas anteriores se publicaron manualmente;
2. marcar sus reels como `publicado`;
3. evitar volver a programarlas;
4. registrar cualquier cambio de copy final que haya ocurrido fuera del manifiesto;
5. conservar el histórico sin reprogramar semanas cerradas.

## 8. Regla de ejecución única

Los bancos se sincronizan en ambos repositorios. Los workflows de publicación se ejecutan únicamente desde `PauloStrina/motion-content-engine`.

Nunca ejecutar el mismo `live` en los dos repositorios.
