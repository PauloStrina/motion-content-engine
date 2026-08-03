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
8. `design-system/slides/EJEMPLO_HEM_carrusel.json` como referencia técnica, no como plantilla estética obligatoria.
9. documentación y código de `design-system/`.

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
- ruta de `copy_source`.

El visual debe representar el centro narrativo y conducir hacia el punto de llegada aprobado. No puede:

- ampliar el alcance conceptual;
- agregar una conclusión;
- convertir Problema en Método;
- convertir un ejemplo potencial en un caso real;
- agregar una etapa, artefacto, cifra o resultado;
- compensar con diseño una fuente editorial incorrecta.

Si `copy_locked` es `true`, la fuente indicada en `copy_source` gobierna. Ante contradicción entre manifiesto, spec visual o assets candidatos, detené el flujo y reportá la inconsistencia.

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

Leé el contrato narrativo y el concepto aprobado antes de diseñar.

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

No copies composiciones de las referencias.

## Separación y legibilidad

- El texto y el diagrama deben ocupar zonas deliberadas y legibles.
- Ninguna línea, nodo, círculo, fotografía o rótulo puede solapar el texto principal.
- Los rótulos internos se ubican en espacios limpios o en una leyenda independiente.
- La relación visual debe aportar significado; evitar curvas, nodos o capas meramente decorativas.
- Una trayectoria debe expresar origen, decisión, fricción, convergencia, resultado o evolución reconocible.
- Una capa debe expresar profundidad, dependencia o causa, no solamente ornamentación.
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
8. Confirmá que no existen solapamientos entre texto, rótulos y capas.
9. Confirmá que cada gráfico tiene una función semántica reconocible.
10. Confirmá que los assets referenciados existen.
11. Ejecutá:

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
