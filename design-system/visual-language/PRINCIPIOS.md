# LENGUAJE VISUAL OPERATIVO DE MOTION

**Estado:** vigente para ejecución visual  
**Precedencia:** subordinado a `strategy/ESTRATEGIA_MOTION_CANONICA.md` y al concepto visual aprobado de cada pieza  
**Función:** traducir mensajes aprobados a recursos gráficos sin definir la narrativa editorial.

## 1. Principio central

Motion no utiliza una plantilla visual única.

Cada pieza debe encontrar la representación más simple y potente para hacer visible su idea. La consistencia surge de la calidad de conceptualización, la paleta, la tipografía, el uso del espacio, la precisión del sistema y el repertorio de marca; no de repetir líneas, puntos o una composición fija.

Pregunta de trabajo:

> ¿Cuál es la forma visual más simple de hacer visible esta idea?

## 2. Criterios obligatorios

- limpieza y legibilidad móvil;
- una idea visual dominante;
- síntesis sin vaciar la relación conceptual;
- uso intencional del espacio;
- branding Motion como sistema, no como decoración;
- movimiento con significado;
- correspondencia entre forma y mensaje;
- variedad suficiente para no quemar un recurso;
- trazabilidad entre concepto aprobado y asset final.

## 3. Repertorio abierto

Las familias visuales son recursos, no categorías rígidas:

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

Líneas, nodos y círculos se utilizan cuando explican conexiones, actores, silos, flujos, trayectorias u orquestación. No constituyen la firma obligatoria de Motion.

## 4. Branding

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

Recursos prioritarios del branding:

- formas continuas y plegadas;
- deformación y cambio de plano;
- estrías, ecos y huellas;
- superposición y gradiente;
- bloques cromáticos intensos;
- serialidad y repetición;
- fotografía editorial intervenida;
- ondas y campos concéntricos.

No es obligatorio utilizar todos los colores ni todos los recursos en una pieza.

## 5. Modos de ejecución

### `code`

Para diagramas, mapas, tipografía, relaciones exactas, datos y geometrías controladas.

### `openai`

Para escenas, objetos, texturas, formas orgánicas o recursos que no conviene construir manualmente.

### `hybrid`

Modo recomendado cuando una imagen generativa se combina con tipografía, diagramas, branding y composición determinística.

### `reuse`

La imagen aprobada se utiliza sin regeneración.

## 6. Reglas de fidelidad

- Una imagen validada no se vuelve a generar desde texto si se requiere el mismo resultado.
- El preview aprobado se conserva como asset o como referencia de edición.
- Logos, copy, diagramas exactos y composición final se resuelven en código.
- El modelo generativo no debe incluir texto final de publicación salvo una decisión explícita.
- Los prompts y parámetros quedan versionados.
- Los recursos de terceros son referencia, no material final, salvo licencia verificada.

## 7. Fuentes principales de inspiración

1. Branding original de Motion.
2. Referencias esquemáticas minimalistas compartidas por Paulo.
3. Colección `Concepto 2`, documentada en `design-system/references/concepto-2/README.md`.

La jerarquía es siempre:

1. mensaje aprobado;
2. estrategia y branding Motion;
3. concepto visual aprobado;
4. referencias;
5. capacidad técnica de ejecución.
