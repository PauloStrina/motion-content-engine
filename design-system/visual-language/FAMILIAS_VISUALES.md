# FAMILIAS VISUALES MOTION

## 1. Regla central

Motion trabaja con dos familias visuales principales. Cada pieza debe elegir **una sola**.

No se pueden mezclar dentro del mismo asset ni dentro de un mismo carrusel. La tipografía, la paleta y el logotipo son capas comunes de identidad; no constituyen una tercera familia.

## 2. Familia A — `line_system`

Sistema diagramático bidimensional inspirado en esquemas de líneas y nodos.

### Recursos dominantes

- líneas simples, continuas o quebradas;
- nodos, puntos, círculos y órbitas;
- ejes, curvas, trayectorias y conexiones;
- módulos planos;
- alto uso de espacio negativo;
- pocos elementos y relaciones legibles;
- geometría precisa y deliberada.

### Qué debe expresar

La idea se comunica mediante relaciones: conexión, secuencia, tensión, bloqueo, desvío, convergencia, expansión o cambio de dirección.

### Ejecución recomendada

- `code` para diagramas exactos;
- `hybrid` solo cuando una textura o imperfección manual sea necesaria, manteniendo la estructura vectorial dominante.

### Prohibido

- sombras volumétricas;
- cintas 3D;
- objetos escultóricos;
- profundidad fotorealista;
- texturas materiales dominantes;
- mezclar líneas y nodos con una metáfora artística volumétrica.

## 3. Familia B — `conceptual_art`

Sistema conceptual, esquemático o artístico basado en una metáfora visual dominante.

### Recursos dominantes

- pliegues, cintas, capas, volúmenes y sombras;
- objetos conceptuales o composiciones escultóricas;
- profundidad, materia, luz y espacio negativo;
- diagramas con cualidad editorial o artística;
- una metáfora central que sintetiza el argumento.

### Qué debe expresar

La pieza debe convertir la tesis en una imagen: integrar, desarmar, atravesar, sostener, conectar, liberar, comprimir, expandir o transformar.

### Ejecución recomendada

- `openai` para generar el recurso visual central;
- `hybrid` para combinar ese recurso con tipografía, logo y composición exacta;
- `code` solo cuando el renderer pueda reproducir la calidad material requerida.

### Prohibido

- redes de puntos como recurso principal;
- curvas de trayectoria tipo infografía;
- múltiples pequeños diagramas compitiendo con la metáfora;
- apariencia de dashboard o esquema técnico plano;
- mezclar una cinta o volumen con el lenguaje Matt Gray dentro de la misma pieza.

## 4. Selección de familia

Elegir `line_system` cuando la idea depende principalmente de una relación entre partes:

- antes y después;
- causa y consecuencia;
- trayectorias;
- silos y conexiones;
- secuencias;
- redes;
- evolución de un sistema.

Elegir `conceptual_art` cuando la idea depende principalmente de una metáfora o una transformación visual:

- integración de Negocio, Tecnología y Cultura;
- tensión entre fuerzas;
- cambio de forma;
- peso, fricción, ruptura, movimiento o equilibrio;
- una idea que necesita impacto editorial y no solo explicación.

## 5. Regla para carruseles

Todas las placas de un carrusel usan la misma familia. Puede variar la composición, pero no el lenguaje.

Un carrusel `line_system` puede cambiar nodos, trayectorias y relaciones. No puede introducir cintas volumétricas o sombras artísticas.

Un carrusel `conceptual_art` puede mostrar distintas vistas o transformaciones de una metáfora. No puede alternar con placas de líneas y pelotitas.

## 6. Calidad conceptual

Antes de ejecutar, el contrato debe responder:

1. ¿Qué idea única hace visible la pieza?
2. ¿Por qué esta familia es la adecuada?
3. ¿Cuál es la metáfora o relación dominante?
4. ¿Qué recursos están prohibidos para evitar contaminación?
5. ¿Qué referencia de la misma familia orienta la calidad?

La pieza no se aprueba solo porque usa la paleta y el logo. Debe alcanzar calidad conceptual, claridad y oficio visual comparables con las referencias aprobadas.

## 7. Flujo obligatorio

```text
contenido aprobado
→ tres hipótesis visuales
→ elección de una familia
→ selección de una hipótesis
→ contrato draft
→ preview de calidad
→ aprobación de Paulo
→ ejecución final
→ validación visual
```

No se marca un contrato como `approved` antes de mostrar y aprobar el preview.
