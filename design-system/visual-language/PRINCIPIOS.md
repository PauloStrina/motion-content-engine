# LENGUAJE VISUAL OPERATIVO DE MOTION

**Estado:** vigente para ejecución visual  
**Precedencia:** subordinado a `strategy/ESTRATEGIA_MOTION_CANONICA.md`, a `FAMILIAS_VISUALES.md` y al concepto visual aprobado de cada pieza  
**Función:** traducir mensajes aprobados a recursos gráficos sin definir la narrativa editorial.

## 1. Principio central

Motion no utiliza una plantilla visual única, pero tampoco mezcla lenguajes incompatibles dentro de una misma pieza.

Cada pieza debe encontrar la representación más simple y potente para hacer visible su idea y elegir una sola familia visual:

- `line_system`;
- `conceptual_art`.

La consistencia surge de la calidad de conceptualización, la elección correcta de familia, la paleta, la tipografía, el uso del espacio, la precisión del sistema y el repertorio de marca.

Pregunta de trabajo:

> ¿Cuál es la forma visual más simple de hacer visible esta idea y qué familia puede expresarla sin contaminación?

## 2. Regla de familia única

- una pieza utiliza una sola familia;
- todas las placas de un carrusel utilizan la misma familia;
- los recursos de la otra familia quedan explícitamente excluidos;
- tipografía, paleta y logotipo son capas de identidad comunes;
- una pieza no se aprueba porque “se vea Motion”: debe tener claridad conceptual y calidad comparable con sus referencias.

La definición completa vive en `design-system/visual-language/FAMILIAS_VISUALES.md`.

## 3. Formato dominante para carruseles largos

El formato dominante de Motion para carruseles largos es `narrative_schematic_carousel`.

Este formato:

- cuenta una historia completa a lo largo de 8 a 12 placas;
- mantiene lectura fácil y rápida;
- utiliza un esquema simple por placa para reforzar la idea principal;
- respeta literalmente el copy aprobado;
- evita estética handwritten, de cuaderno o presentación corporativa;
- utiliza principalmente la familia `line_system`;
- permite variar la distribución de colores según Problema, Método, Resultado o Conexión;
- utiliza naranja Motion `#FF5000` para hitos clave y resultados puntuales;
- no utiliza amarillo o lima como sustituto del naranja de marca.

La gramática completa vive en `design-system/visual-language/CARRUSEL_NARRATIVO_ESQUEMATICO.md`.

## 4. Criterios obligatorios

- limpieza y legibilidad móvil;
- una idea visual dominante;
- síntesis sin vaciar la relación conceptual;
- uso intencional del espacio;
- branding Motion como sistema, no como decoración;
- movimiento con significado;
- correspondencia entre forma y mensaje;
- variedad suficiente para no quemar un recurso;
- trazabilidad entre concepto aprobado y asset final;
- fidelidad a una única familia;
- calidad de ejecución equivalente a la referencia seleccionada.

## 4.1 Regla dura de no solapamiento

> **El texto y los elementos gráficos no se solapan.**

Esta regla aplica a:

- títulos y subtítulos;
- texto principal y microtexto;
- líneas y trayectorias;
- nodos, círculos y contenedores;
- rótulos internos;
- fotografías, formas y texturas;
- logos, firma y paginación.

Controles obligatorios:

- cada placa define una zona de texto, una zona visual y una zona de firma;
- ninguna línea, nodo, círculo, rótulo o imagen puede ingresar al bounding box del texto ni a su margen de seguridad;
- los rótulos del gráfico deben ubicarse dentro de espacios limpios o en una leyenda externa;
- si la relación conceptual no cabe sin superposición, se redistribuye o simplifica el gráfico;
- nunca se reduce la legibilidad para conservar una composición;
- es preferible conservar espacio vacío antes que llenar la placa con elementos sin función.

Una pieza con texto y elementos gráficos solapados no puede pasar a estado aprobado.

## 4.2 Balance vertical

- texto y gráfico deben sentirse parte de una misma composición, no dos bloques desconectados;
- en carruseles, el conjunto principal debe ubicarse cerca del centro óptico de la placa;
- cuando exista espacio vacío dominante, se prioriza la parte superior antes que comprimir texto, gráfico y firma en el pie;
- la distancia entre texto y gráfico debe ser menor que la distancia entre cualquiera de ellos y los bordes exteriores, salvo decisión conceptual explícita.

## 4.3 Preview aprobado como master

Cuando Paulo identifica expresamente un preview, contact sheet o composición de revisión como la solución correcta, ese preview pasa a ser **master visual de producción**.

A partir de esa decisión:

- no se vuelve a interpretar el concepto desde cero;
- se conserva la composición, jerarquía, gramática de líneas, iconografía, relaciones y distribución aprobadas;
- se adapta únicamente lo necesario para producir cada formato con calidad final;
- no se reemplaza por una solución “equivalente” o por una nueva versión más genérica;
- los assets finales deben poder compararse directamente con el master y explicar cualquier diferencia;
- si el master proviene de una vista conjunta, se reconstruyen las piezas individuales manteniendo el mismo lenguaje y las mismas relaciones.

Un preview aprobado no es solo una referencia de inspiración: gobierna la ejecución hasta que Paulo apruebe otra dirección.

## 5. Repertorio de recursos

Los recursos se organizan bajo las dos familias visuales. No son intercambiables libremente.

Recursos disponibles:

- relaciones y topologías;
- trayectorias y evolución;
- capas y profundidad;
- contenedores y límites;
- fuerzas y tensiones;
- sistemas modulares;
- repetición y variación;
- vacío y ausencia;
- contraste visual;
- metáforas objetuales;
- escalas y proporciones;
- intersecciones y superposiciones;
- timelines y mapas;
- fotografía editorial intervenida;
- tipografía conceptual;
- formas tridimensionales;
- imágenes generativas;
- diagramas animados.

`FAMILIAS_VISUALES.json` define qué recursos puede utilizar cada familia y cuáles están prohibidos.

## 5.1 Patrón canónico — Programa que integra Negocio, Tecnología y Cultura

Cuando una pieza menciona un **Programa de Transformación Digital que integra Negocio, Tecnología y Cultura**, la representación preferente es un sistema circular:

- el Programa ocupa el núcleo central;
- el anillo exterior se divide en tres sectores equivalentes;
- los sectores se rotulan `NEGOCIO`, `TECNOLOGÍA` y `CULTURA`;
- el esquema comunica integración simultánea, no una secuencia ni tres inputs desconectados;
- las divisiones deben ser claras y los rótulos legibles;
- evitar tres líneas independientes que convergen en un punto si la idea central es integración sistémica;
- los colores se adaptan al branding Motion sin alterar la equivalencia entre los tres componentes.

Este patrón puede simplificarse para tamaños pequeños, pero debe conservar siempre la relación **núcleo común + tres dimensiones integradas**.

## 6. Branding

Paleta oficial:

- naranja `#FF5000`;
- violeta `#50235A`;
- aqua `#9DEDE3`;
- negro `#1A1A1A`;
- blanco `#FFFFFF`.

Tipografías:

- Futura Extra Bold Condensed: estructura, sistema, señal, dato, acción;
- Lyon: interpretación, tesis, reflexión, dimensión humana;
- Gotham Narrow: información secundaria, numeración y microtexto.

Reglas de aplicación:

- la primera frase o headline principal de una portada de carrusel se compone en **Futura Extra Bold Condensed**;
- una segunda frase puede utilizar Lyon, Gotham Narrow u otra jerarquía aprobada cuando cumple una función distinta;
- la firma utiliza el logo oficial `MOTION` y el descriptor en dos líneas exactamente así:

```text
Lo complejo,
simple.
```

- el descriptor no se presenta en una única línea;
- logo y descriptor mantienen una separación clara y no compiten con el contenido.

No es obligatorio utilizar todos los colores ni todos los recursos en una pieza.

Los hitos clave utilizan naranja Motion. No se sustituyen por amarillo, lima ni colores no pertenecientes al branding.

## 7. Modos de ejecución

### `code`

Para diagramas, mapas, tipografía, relaciones exactas, datos y geometrías controladas. Es el modo principal de `line_system`.

### `openai`

Para objetos, escenas, texturas, volumen, formas orgánicas y recursos de `conceptual_art` que requieren alta calidad material.

### `hybrid`

Recurso generativo más tipografía, logo y composición determinística. Es el modo principal cuando `conceptual_art` necesita precisión de marca.

### `reuse`

La imagen aprobada se utiliza sin regeneración.

Los modos permitidos se validan por familia.

## 8. Reglas de fidelidad

- una imagen validada no se vuelve a generar desde texto si se requiere el mismo resultado;
- el preview aprobado se conserva como asset o como referencia de edición;
- si Paulo aprueba la composición del preview, se aplica la regla de master visual de la sección 4.3;
- logos, copy y composición final se resuelven con precisión determinística;
- el modelo generativo no incluye texto final de publicación ni logo;
- los prompts y parámetros quedan versionados;
- las referencias de terceros no se publican salvo licencia verificada;
- no se marca un contrato como `approved` antes de mostrar y aprobar el preview;
- el diseño no puede reescribir ni resumir el copy aprobado sin una nueva validación editorial.

## 9. Fuentes principales de inspiración

1. Branding original de Motion.
2. Referencias `line_system` compartidas por Paulo.
3. Referencias `conceptual_art` compartidas y aprobadas por Paulo.
4. Carruseles narrativos esquemáticos aprobados para Curva del Cambio y Comunidad Digital.
5. Colección `Concepto 2` cuando sea coherente con la familia seleccionada.

La jerarquía es siempre:

1. mensaje aprobado;
2. estrategia y branding Motion;
3. familia visual seleccionada;
4. formato dominante cuando corresponda;
5. concepto visual aprobado;
6. preview aprobado como master, cuando exista;
7. referencias de la misma familia;
8. capacidad técnica de ejecución.
