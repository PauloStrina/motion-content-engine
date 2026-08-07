# CONTRATO PARA CLAUDE DESIGN — SISTEMA VISUAL MOTION

Cargá este archivo en Claude Design junto al brief de la pieza. Define el sistema
visual de Motion y el formato de salida que consume el renderer del repositorio.

Su función es que lo que produzcas se pueda portar a producción sin rediseñar.

---

## 1. Qué se está diseñando

Placas de carrusel para LinkedIn e Instagram de **Motion**, consultora de
transformación digital. Formato **1080 x 1350**.

Cada placa desarrolla **una sola idea**, tomada literalmente de un copy ya
aprobado. El copy no se reescribe, no se resume y no se corrige, ni siquiera
sus erratas.

## 2. Familia visual

La familia vigente es `line_system`: **líneas, curvas, nodos circulares y arcos**.
Trazo vectorial preciso, mucho espacio negativo, pocos elementos.

Permitido: relaciones y topologías, trayectorias, contenedores, sistemas
modulares, repetición y variación, vacío y ausencia, escala, intersecciones,
timelines, tipografía conceptual, movimiento.

Excluido de esta familia: capas con profundidad ilusoria, fuerzas físicas,
metáfora objetual, fotografía intervenida, imagen generativa.

Si tu propuesta necesita alguno de los recursos excluidos, **decilo
explícitamente** en la hipótesis. Es información valiosa: significa que el
lenguaje actual no alcanza para esa idea.

## 3. Paleta

| Color | Hex | Uso |
|---|---|---|
| Naranja Motion | `#FF5000` | hitos clave y resultados puntuales |
| Violeta Motion | `#50235A` | estructura, tipografía, relaciones principales |
| Aqua Motion | `#9DEDE3` / `#2BAFA4` | método, acompañamiento, evolución |
| Negro | `#1A1A1A` | texto |
| Fondo | `#FAF8F5` | blanco hueso, nunca blanco puro |

Regla dura: **los hitos son naranja `#FF5000`.** Nunca amarillo, nunca lima,
nunca un sustituto.

Orientación por tipo de mensaje: Problema, violeta dominante con naranja para la
tensión. Método, aqua dominante con violeta estructural. Resultado, naranja para
cifras e hitos. Conexión, violeta y aqua.

## 4. Tipografías

- **Futura Std Condensed Extra Bold** — estructura, señal, dato, acción. La
  primera frase o headline de una portada va siempre en esta.
- **Lyon** — interpretación, tesis, reflexión, dimensión humana.
- **Gotham Narrow** — microtexto, rótulos, numeración. Los rótulos van en
  mayúsculas con letter-spacing.

## 5. Reglas duras

**Texto y gráfico nunca se solapan.** Cada placa define zona de texto, zona
visual y zona de firma. Ninguna línea, nodo, arco, rótulo o imagen entra en la
caja del texto ni en su margen de seguridad. Si el esquema no entra, se
simplifica. Una superposición invalida la pieza.

**Balance vertical.** El conjunto principal cerca del centro óptico. El espacio
vacío dominante va arriba, no abajo. La distancia entre texto y gráfico es menor
que la distancia de cualquiera de los dos a los bordes.

**Firma.** Logo `MOTION` más descriptor en dos líneas exactas:

```text
Lo complejo,
simple.
```

Nunca en una sola línea. El logo no se dibuja ni se recrea: se inserta como
asset.

**Paginación.** Círculo naranja pequeño arriba a la izquierda con el número de
placa en blanco.

**Patrón canónico.** Si el copy menciona integrar Negocio, Tecnología y Cultura,
la representación es un núcleo central con anillo exterior dividido en tres
sectores equivalentes rotulados `NEGOCIO`, `TECNOLOGÍA` y `CULTURA`. Integración
simultánea, no tres líneas que convergen.

## 6. Qué se espera de vos

Tres direcciones visuales — **B, C y D** — para la misma pieza.

Cada una parte de una **lectura conceptual distinta de la misma frase**, no de
una variación cosmética. Antes de componer, escribí en una frase qué está
probando esa dirección y por qué podría comunicar mejor que las otras.

Mostrá cada dirección sobre **tres placas**: portada, una placa de desarrollo y
el cierre.

No propongas una dirección que sea la misma composición con otro color.

## 7. Formato de salida

Entregá un ZIP con:

```text
B/  hipotesis.md      una frase: qué prueba esta dirección
    placa-01.svg      portada
    placa-XX.svg      desarrollo
    placa-YY.svg      cierre
C/  …
D/  …
```

Requisitos del SVG:

- `viewBox="0 0 1080 1350"`, sin dimensiones fijas en píxeles;
- geometría en elementos `<path>`, `<circle>`, `<line>` con coordenadas
  explícitas — nada de imágenes rasterizadas embebidas;
- colores en hex literal de la paleta, sin variables CSS;
- texto en `<text>` con la familia declarada por nombre, no convertido a curvas;
- sin `<foreignObject>`, sin scripts, sin dependencias externas.

Ese formato permite leer la geometría y portarla a la gramática del renderer.
Si algo no se puede expresar así, entregalo igual y anotá qué recurso necesitaste.

## 8. Lo que no hay que hacer

- reescribir, resumir o corregir el copy;
- letra manuscrita, estética de cuaderno, papel o post-it;
- layouts de presentación corporativa;
- iconografía decorativa sin función;
- una ilustración distinta y desconectada por placa;
- hitos en amarillo;
- logos generados o recreados;
- solapamientos entre texto, líneas, nodos o rótulos.
