# PROCESO DE CONOCIMIENTO Y PRODUCCIÓN DE CONTENIDOS

## 1. Dos flujos relacionados

El sistema separa:

1. **aprendizaje y conocimiento:** actualiza estrategia, situaciones, artefactos, conceptos, evidencias, hooks, storytelling, arquitectura de comprensión y auditoría;
2. **producción semanal:** convierte contenido aprobado en manifiestos, conceptos visuales, assets y programación.

La conversación con Paulo define criterio, correcciones y aprobación. GitHub es la memoria persistente y gobernada del sistema. No es necesario descargar y volver a cargar documentos para actualizar las reglas activas.

Los documentos adjuntos al proyecto o copias locales pueden servir como referencia histórica, pero no gobiernan cuando contradicen los archivos vigentes del repositorio.

## 2. Actualización de conocimiento desde el chat

Cuando Paulo aporta o corrige información:

1. identificar el aprendizaje;
2. formular la **conclusión estratégica del feedback**: qué principio mejora la calidad y qué cambia en futuras piezas;
3. clasificarlo como estrategia, situación, artefacto, concepto, evidencia, hook, storytelling, arquitectura de comprensión o corrección editorial;
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

### Paso 2 — Diseñar la arquitectura de comprensión

Antes del esqueleto narrativo se declara cómo el lector podrá reconstruir la idea:

- `conocimiento_inicial`: qué situación, problema o lenguaje ya reconoce;
- `idea_nueva`: qué distinción debe comprender;
- `puente`: qué situación, contraste, ejemplo, pregunta o mecanismo conecta ambos;
- `arco_principal`: qué relaciones lógicas hacen avanzar la pieza.

Estructura mínima:

```json
{
  "arquitectura_cognitiva": {
    "conocimiento_inicial": "la visión está aprobada, pero las áreas siguen decidiendo por separado",
    "idea_nueva": "la legitimidad puede construirse produciendo evidencia",
    "puente": "un comité transversal que no modifica decisiones cotidianas",
    "arco_principal": [
      "situacion",
      "intento",
      "contraste",
      "explicacion",
      "nueva_comprension"
    ]
  }
}
```

Controles:

- cada pieza trabaja una idea nueva principal;
- la idea nueva se apoya en algo que el lector ya conoce;
- cada bloque tiene una relación reconocible con el anterior;
- claridad no significa explicar más;
- si una explicación no cambia la comprensión, se elimina;
- los conceptos estratégicos centrales no se diluyen en paráfrasis ni enumeraciones secundarias.

### Paso 3 — Construir el esqueleto editorial

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

### Paso 4 — Aprobar el diseño editorial y cognitivo

Paulo corrige o aprueba:

- tema;
- tipo y efecto editorial;
- centro narrativo;
- punto de llegada;
- conocimiento inicial del lector;
- idea nueva;
- puente cognitivo;
- arco principal;
- hooks;
- situación;
- concepto o artefacto;
- evidencia;
- CTA;
- secuencia semanal.

No se redacta el copy final hasta que el diseño permite distinguir con claridad la función de la pieza y el recorrido mental del lector.

### Paso 5 — Redactar copys reales

Se escriben versiones separadas para:

- LinkedIn de Paulo;
- Instagram de Motion;
- carruseles;
- newsletter cuando corresponda;
- guion o copy de reel.

El copy publicable se lee como storytelling continuo. No muestra los rótulos `Hook`, `Situación`, `Fricción`, `Reencuadre`, `Conclusión` o `CTA`.

Storytelling define cómo avanza la pieza. El tipo editorial define qué cambio debe producir en el lector. La arquitectura de comprensión define cómo pasa de lo que reconoce a la idea nueva.

Cada párrafo o placa debe justificar su presencia. Debe aportar al menos una de estas funciones:

- presentar una situación;
- hacer avanzar la escena;
- mostrar un intento;
- establecer una relación causal;
- explicar una distinción;
- mostrar un mecanismo;
- aportar evidencia;
- instalar una consecuencia;
- conectar naturalmente con el siguiente paso.

Los detalles obvios o previsibles no se desarrollan si no agregan una distinción nueva.

Aplicar el siguiente orden cuando corresponda:

- conocido antes que nuevo;
- tema antes que comentario;
- situación concreta antes que concepto denso;
- actores y acciones antes que abstracciones;
- conclusión importante en una posición fuerte.

No usar como fórmula obligatoria:

- estructuras numéricas de párrafos;
- sucesiones permanentes de frases de una línea;
- listas diseñadas solo para facilitar escaneo;
- opiniones artificialmente contundentes;
- estilos reconocibles de escritura algorítmica o genérica de LinkedIn.

### Paso 6 — Revisar desde la mente del lector

Antes de aprobar el copy:

1. reconstruir la idea central en una frase;
2. verificar que se entienda de qué habla, qué sostiene Motion y por qué;
3. revisar que cada pronombre o referencia tenga un antecedente claro;
4. identificar puntos donde el lector deba retroceder;
5. eliminar explicaciones que no produzcan una comprensión nueva;
6. leer en voz alta para detectar sintaxis laberíntica o pérdida de ritmo;
7. confirmar que el punto de llegada no fue ampliado durante la redacción.

### Paso 7 — Aprobar, bloquear y aprender

Después de la aprobación:

- el copy queda congelado con `copy_locked: true`;
- se conserva la fuente exacta aprobada;
- se conserva también la arquitectura de comprensión aprobada;
- los hooks se registran en el Banco de Hooks;
- los conceptos nuevos o adaptados se registran en el Banco de Conceptos;
- los hechos y cifras se registran en Evidencias;
- situaciones o artefactos nuevos se incorporan a sus bancos;
- las correcciones de voz, storytelling o comprensión relevantes se registran en la Auditoría Editorial;
- se explicita la conclusión estratégica del feedback y se actualiza el archivo de GitHub que corresponda.

Con `copy_locked: true`, una adaptación puede segmentar, jerarquizar y crear variantes de CTA por canal. No puede regenerar el contenido desde un resumen, alterar el orden argumental, modificar la persona narrativa, cambiar el arco de coherencia ni agregar conceptos no aprobados.

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
- arquitectura de comprensión aprobada;
- copy aprobado y bloqueado;
- concepto visual aprobado;
- evidencia autorizada;
- estado editorial aprobado en el manifiesto.

El repositorio no puede corregir automáticamente el copy, cambiar su tipo editorial, ampliar el punto de llegada, modificar la idea nueva ni decidir una nueva dirección de arte.

## 6. Flujo técnico

### 6.1 PR de contenido

1. crear rama;
2. cargar manifiesto, fuentes editoriales, newsletter, reservas de reels y contratos visuales;
3. validar JSON, referencias, fechas, estados, contrato narrativo, arquitectura cognitiva y assets;
4. abrir PR;
5. revisar diff;
6. mergear a `main`.

### 6.2 Preparar assets

Ejecutar `1-preparar-assets` con:

```text
mes: 2026-07
semana: 2
```

El workflow valida el alcance, lee el copy aprobado, produce especificaciones visuales y no modifica el texto, el contrato narrativo ni la arquitectura de comprensión.

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
- arquitectura de comprensión y arco aprobado;
- reels;
- orden y legibilidad de carruseles;
- coherencia entre tipo, narrativa, comprensión y visual;
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

Los bancos y documentos de gobernanza se sincronizan en ambos repositorios. Los manifiestos, fuentes editoriales semanales, specs y assets operativos permanecen únicamente en `PauloStrina/motion-content-engine`.

Los workflows de publicación se ejecutan únicamente desde `PauloStrina/motion-content-engine`.

Nunca ejecutar el mismo `live` en los dos repositorios.
