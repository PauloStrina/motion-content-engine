# PREPARACIÓN DE ASSETS DEL MES O SEMANA

## Alcance

Tu responsabilidad es convertir copy y conceptos visuales ya aprobados en especificaciones ejecutables para el sistema de diseño.

No redactes, no resumas, no corrijas, no completes y no cambies ninguna palabra del manifiesto.

No inventes el concepto visual. Si el contrato no alcanza para producir una pieza, fallá con una explicación concreta.

## Inputs

1. `manifiestos/mes_<YYYY-MM>.json`.
2. Alcance indicado en `SEMANA`.
3. `design-system/visual-language/PRINCIPIOS.md`.
4. `design-system/visual-language/RECURSOS_VISUALES.json`.
5. El `concept_path` de cada pieza, cuando exista.
6. `design-system/slides/EJEMPLO_HEM_carrusel.json` como referencia técnica, no como plantilla estética obligatoria.
7. documentación y código de `design-system/`.

No leas `archive/**`. No uses archivos estratégicos para inventar contenido. No modifiques el subsistema de video.

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
- El campo `text` debe contener temporalmente la misma línea del manifiesto.
- No unas dos líneas en un solo bloque.
- No dividas una línea en varios bloques.
- No agregues frases, CTA, hashtags, firmas ni aclaraciones.

## Sistema visual

Leé el concepto aprobado antes de diseñar.

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

El tipo editorial no define la paleta ni la forma. El mensaje y el concepto aprobado gobiernan la representación.

Las líneas, puntos y círculos son un recurso posible, no un requisito.

Usá únicamente:

- paleta oficial Motion;
- tipografías existentes;
- recursos documentados;
- assets aprobados;
- capas soportadas por el renderer.

No copies composiciones de las referencias.

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
- No modificar manifiesto, estrategia, conocimiento, newsletters, workflows ni scripts.
- No crear una nueva gramática para una pieza puntual si puede resolverse con recursos existentes.
- Cuando un recurso nuevo sea realmente necesario, no lo improvises dentro del JSON: reportalo para ampliar el sistema.

## Autocontrol

Antes de terminar:

1. Confirmá un JSON por carrusel.
2. Confirmá cantidad de slides.
3. Confirmá cantidad de bloques de texto.
4. Confirmá copy idéntico carácter por carácter.
5. Confirmá correspondencia con el contrato visual.
6. Confirmá que los assets referenciados existen.
7. Ejecutá:

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
