# PROCESO DE CONOCIMIENTO Y PRODUCCIÓN DE CONTENIDOS

## 1. Dos flujos relacionados

El sistema separa:

1. **aprendizaje y conocimiento:** actualiza estrategia, situaciones, artefactos, conceptos, evidencias, hooks y auditoría;
2. **producción semanal:** convierte contenido aprobado en manifiestos, conceptos visuales, assets y programación.

La conversación con Paulo define criterio, correcciones y aprobación. GitHub es la memoria persistente y gobernada del sistema. No es necesario descargar y volver a cargar documentos para actualizar las reglas activas.

Los documentos adjuntos al proyecto o copias locales pueden servir como referencia histórica, pero no gobiernan cuando contradicen los archivos vigentes del repositorio.

## 2. Actualización de conocimiento desde el chat

Cuando Paulo aporta o corrige información:

1. identificar el aprendizaje;
2. formular la **conclusión estratégica del feedback**: qué principio mejora la calidad y qué cambia en futuras piezas;
3. clasificarlo como estrategia, situación, artefacto, concepto, evidencia, hook o corrección editorial;
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

### Paso 1 — Definir la secuencia

Para cada día se construye un esqueleto con:

- tres alternativas de hook;
- por qué importa;
- qué hace Motion;
- caso real;
- cómo hacerlo;
- CTA conectado con el Programa de Transformación Digital.

La semana debe mantener coherencia: el caso de Resultados demuestra el Método presentado y la pieza de Conexión amplía la capacidad necesaria para sostenerlo.

### Paso 2 — Aprobar el esqueleto

Paulo corrige o aprueba:

- tema;
- hooks;
- situación;
- concepto o artefacto;
- evidencia;
- CTA;
- secuencia semanal.

No se redacta ni produce una pieza sobre un caso que contradiga el método de la semana.

### Paso 3 — Redactar copys reales

Se escriben versiones separadas para:

- LinkedIn de Paulo;
- Instagram de Motion;
- carruseles;
- newsletter cuando corresponda;
- guion o copy de reel.

El copy publicable se lee como storytelling continuo. No muestra los rótulos `Hook`, `Bajada`, `Contenido` o `CTA`.

Cada párrafo debe justificar su presencia. Debe aportar al menos una de estas funciones:

- introducir la tensión;
- explicar un concepto;
- mostrar un mecanismo;
- aportar evidencia;
- volver la idea aplicable;
- conectar con el Programa.

Los detalles obvios o previsibles no se desarrollan si no agregan una distinción nueva.

### Paso 4 — Aprobar y aprender

Después de la aprobación:

- el copy queda congelado;
- los hooks se registran en el Banco de Hooks;
- los conceptos nuevos o adaptados se registran en el Banco de Conceptos;
- los hechos y cifras se registran en Evidencias;
- situaciones o artefactos nuevos se incorporan a sus bancos;
- las correcciones de voz relevantes se registran en la Auditoría Editorial;
- se explicita la conclusión estratégica del feedback y se actualiza el archivo de GitHub que corresponda.

## 4. Carga en GitHub

La producción se realiza en una rama temática del repositorio primario.

Ejemplo:

```text
content/2026-07-semana-2
```

### Archivos a modificar o crear

1. `manifiestos/mes_2026-07.json`: agregar la semana sin alterar el histórico.
2. `newsletters/`: guardar la newsletter aprobada.
3. `banco/reels/catalogo.json`: reconciliar publicados manualmente y reservar reels de la semana.
4. `design-system/concepts/<mes>/<piece_id>/concept.json`: guardar la hipótesis visual aprobada.
5. `design-system/slides/`: especificaciones visuales finales, generadas o revisadas por el flujo de assets.
6. Bancos y auditoría, únicamente si la semana produjo aprendizaje nuevo.

## 5. Aprobaciones separadas

Cada pieza necesita:

- copy aprobado;
- concepto visual aprobado;
- evidencia autorizada;
- estado editorial aprobado en el manifiesto.

El repositorio no puede corregir automáticamente el copy ni decidir una nueva dirección de arte.

## 6. Flujo técnico

### 6.1 PR de contenido

1. crear rama;
2. cargar manifiesto, newsletter, reservas de reels y contratos visuales;
3. validar JSON, referencias, fechas, estados y assets;
4. abrir PR;
5. revisar diff;
6. mergear a `main`.

### 6.2 Preparar assets

Ejecutar `1-preparar-assets` con:

```text
mes: 2026-07
semana: 2
```

El workflow valida el alcance, lee el copy aprobado, produce especificaciones visuales y no modifica el texto.

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
- reels;
- orden y legibilidad de carruseles;
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