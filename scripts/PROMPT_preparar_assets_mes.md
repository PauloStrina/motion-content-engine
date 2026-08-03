# PREPARACIÓN DE ASSETS DEL MES O SEMANA

## Alcance

Tu responsabilidad es convertir copy, contrato narrativo y conceptos visuales ya aprobados en especificaciones ejecutables para el sistema de diseño.

No redactes, no resumas, no corrijas, no completes y no cambies ninguna palabra de la fuente aprobada o del manifiesto.

No inventes el concepto visual. Si el contrato narrativo o visual no alcanza para producir una pieza, fallá con una explicación concreta.

## Inputs

1. `manifiestos/mes_<YYYY-MM>.json`.
2. Alcance indicado en `SEMANA`.
3. `knowledge/guides/GUIA_OPERATIVA_STORYTELLING.md`.
4. `design-system/visual-language/PRINCIPIOS.md`.
5. `design-system/visual-language/RECURSOS_VISUALES.json`.
6. El `copy_source` de cada pieza cuando `copy_locked` sea `true`.
7. El `concept_path` de cada pieza, cuando exista.
8. El preview o contact sheet aprobado cuando exista un `visual_master`.
9. `design-system/slides/EJEMPLO_HEM_carrusel.json` como referencia técnica, no como plantilla estética obligatoria.
10. documentación y código de `design-system/`.

No leas `archive/**`. No uses archivos estratégicos para inventar contenido. No modifiques el subsistema de video.

## Contrato narrativo

Antes de diseñar, verificá para cada pieza:

- tipo editorial;
- efecto editorial;
- centro narrativo;
- punto de llegada;
- modo y referencias de fuente;
- evidencia;
- estado de `copy_locked`;
- ruta de `copy_source`;
- existencia de `visual_master`.

El visual debe representar el centro narrativo y conducir hacia el punto de llegada aprobado. No puede:

- ampliar el alcance conceptual;
- agregar una conclusión;
- convertir Problema en Método;
- convertir un ejemplo potencial en un caso real;
- agregar una etapa, artefacto, cifra o resultado;
- compensar con diseño una fuente editorial incorrecta.

Si `copy_locked` es `true`, la fuente indicada en `copy_source` gobierna. Ante contradicción entre manifiesto, spec visual o assets candidatos, detené el flujo y reportá la inconsistencia.

Si existe un `visual_master` aprobado:

- reproducí su composición y gramática;
- no regeneres una alternativa conceptual;
- conservá jerarquía, trayectorias, iconos, relaciones y distribución;
- limitá los cambios a resolución, legibilidad, formato y branding;
- compará el asset final con el master antes de entregar.

## Output

Por cada día seleccionado cuyo `formato` sea:

- `carousel_news`;
- `post_carousel`;
- `faltante_video`;

creá:

```text
design-system/slides/<valor de carrusel>.json
```

No generes ni modifiques carruseles de semanas fuera del alcance.

## Contrato de copy

- La cantidad de slides debe coincidir con `carrusel_slides`.
- Cada slide del diseño debe tener exactamente tantos bloques de texto como elementos haya en `slides[n].lineas`.
- Los bloques de texto válidos son `futura`, `lam`, `eco`, `lyon` y `lyont`.
- Podés agregar bloques no textuales y capas gráficas.
- El campo `text` debe contener temporalmente la misma línea del manifiesto o de la fuente bloqueada.
- No unas dos líneas en un solo bloque.
- No dividas una línea en varios bloques.
- No agregues frases, CTA, hashtags, firmas ni aclaraciones que no estén aprobadas.
- No normalices errores tipográficos sin autorización explícita.
- Cada texto debe poder trazarse a `copy_source` cuando exista.

## Sistema visual

Leé el contrato narrativo, el concepto aprobado y el visual master antes de diseñar.

La solución puede utilizar:

- geometría;
- diagramas;
- mapas;
- tipografía;
- fotografía;
- imágenes generadas;
- capas;
- recorridos;
- intersecciones;
- escala;
- espacio negativo;
- recursos del branding;
- combinaciones híbridas.

No asocies automáticamente:

- problema con negro;
- método con violeta;
- resultados con naranja;
- conexión con aqua.

El tipo editorial no define la paleta ni la forma. El mensaje, el contrato narrativo y el concepto aprobado gobiernan la representación.

Las líneas, puntos y círculos son un recurso posible, no un requisito.

Usá únicamente:

- paleta oficial Motion;
- tipografías existentes;
- recursos documentados;
- assets aprobados;
- capas soportadas por el renderer.

Reglas de portada y firma:

- la primera frase o headline principal de una portada de carrusel utiliza Futura Extra Bold Condensed;
- una segunda frase puede utilizar otra jerarquía aprobada;
- la firma utiliza el logo oficial y el descriptor exactamente en dos líneas:

```text
Lo complejo,
simple.
```

- el descriptor nunca se compone en una única línea.

No copies composiciones de referencias externas. Sí debés reproducir la composición de un preview aprobado de Motion cuando fue declarado master.

## Patrón para Negocio, Tecnología y Cultura

Cuando el copy menciona un Programa de Transformación Digital que integra Negocio, Tecnología y Cultura:

- representar el Programa en un núcleo central;
- dividir un anillo exterior en tres sectores equivalentes;
- rotular `NEGOCIO`, `TECNOLOGÍA` y `CULTURA`;
- comunicar integración simultánea;
- no utilizar tres líneas independientes convergiendo en un punto salvo que el concepto aprobado indique otra relación.

## Separación y legibilidad

> **No se admite ningún solapamiento entre texto y elementos gráficos.**

- El texto y el diagrama deben ocupar zonas deliberadas y legibles.
- Ninguna línea, nodo, círculo, fotografía, textura, forma o rótulo puede ingresar al bounding box del texto ni a su margen de seguridad.
- Los rótulos internos se ubican en espacios limpios o en una leyenda independiente.
- Los rótulos no se colocan encima de líneas o nodos.
- Si el diagrama no cabe, debe simplificarse o redistribuirse; nunca se reduce la legibilidad.
- La relación visual debe aportar significado; evitar curvas, nodos o capas meramente decorativas.
- Una trayectoria debe expresar origen, decisión, fricción, convergencia, resultado o evolución reconocible.
- Una capa debe expresar profundidad, dependencia o causa, no solamente ornamentación.
- Texto y gráfico deben agruparse cerca del centro óptico cuando el formato lo permita.
- Cuando exista espacio vacío dominante, se conserva preferentemente en la parte superior.
- El espacio negativo forma parte de la composición y no debe resolverse llenando la placa con elementos sin función.

## Estructura técnica de una slide

Además de `blocks`, una slide puede incluir `layers`.

Tipos soportados:

- `circle`;
- `ellipse`;
- `rect`;
- `line`;
- `svg_path`;
- `image`.

Las capas son absolutas y no alteran el contrato de texto.

Ejemplo:

```json
{
  "bg": "blanco",
  "pager": "01 — 06",
  "layers": [
    {
      "type": "circle",
      "x": 620,
      "y": 320,
      "w": 260,
      "h": 260,
      "fill": "naranja",
      "opacity": 1,
      "z": 1
    },
    {
      "type": "line",
      "x1": 180,
      "y1": 720,
      "x2": 850,
      "y2": 480,
      "stroke": "violeta",
      "stroke_width": 8,
      "z": 2
    }
  ],
  "mid": {
    "top": 150,
    "bottom": 140,
    "left": 84,
    "width": 912,
    "justify": "flex-end",
    "align": "flex-start",
    "z": 10
  },
  "blocks": [
    {"type": "futura", "text": "COPY APROBADO", "size": 92, "color": "negro"}
  ]
}
```

## Reglas

- Una idea visual dominante por slide.
- Jerarquía clara y legibilidad en 1080 × 1350.
- `pager` consistente con la cantidad real.
- Marca aplicada con criterio.
- Coherencia entre copy, centro narrativo, punto de llegada y gráfico.
- No modificar manifiesto, estrategia, conocimiento, newsletters, workflows ni scripts.
- No crear una nueva gramática para una pieza puntual si puede resolverse con recursos existentes.
- Cuando un recurso nuevo sea realmente necesario, no lo improvises dentro del JSON: reportalo para ampliar el sistema.

## Autocontrol

Antes de terminar:

1. Confirmá un JSON por carrusel.
2. Confirmá cantidad de slides.
3. Confirmá cantidad de bloques de texto.
4. Confirmá copy idéntico carácter por carácter a la fuente aprobada.
5. Confirmá que cada fragmento se traza a `copy_source` cuando existe.
6. Confirmá correspondencia con efecto editorial, centro narrativo y punto de llegada.
7. Confirmá correspondencia con el contrato visual.
8. Confirmá que no existen solapamientos entre texto, rótulos y capas, incluyendo el margen de seguridad.
9. Confirmá que cada gráfico tiene una función semántica reconocible.
10. Confirmá la tipografía de la primera frase de la portada.
11. Confirmá el descriptor `Lo complejo,` / `simple.` en dos líneas.
12. Si existe un preview aprobado, compará el resultado con el master y explicá toda diferencia.
13. Cuando corresponda, confirmá el esquema circular de Programa + Negocio, Tecnología y Cultura.
14. Confirmá que los assets referenciados existen.
15. Ejecutá:

Semana:

```bash
python scripts/validar_conceptos_visuales.py --mes <YYYY-MM> --semana <1-4> --require-approved
python scripts/validar_assets_mes.py --mes <YYYY-MM> --semana <1-4> --require-approved
```

Ciclo:

```bash
python scripts/validar_conceptos_visuales.py --mes <YYYY-MM> --require-approved
python scripts/validar_assets_mes.py --mes <YYYY-MM> --require-approved
```

El trabajo no está terminado si una validación falla.
