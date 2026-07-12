# CONTRATO DEL MANIFIESTO MENSUAL

## Archivo

```text
manifiestos/mes_<YYYY-MM>.json
```

El manifiesto es el input operativo aprobado. Contiene el plan y el copy final de las 16 publicaciones.

## Estructura raíz

```json
{
  "mes": "2026-08",
  "primer_lunes": "2026-08-03",
  "estado": "aprobado",
  "aprobado_por": "Paulo",
  "aprobado_en": "2026-07-30T18:00:00-03:00",
  "semanas": []
}
```

## Reglas

- Debe haber exactamente 4 semanas.
- Cada semana contiene `lun`, `mar`, `mie` y `jue`.
- El orden de tipos es problema, método, resultados y conexión.
- Cada semana suma exactamente 2 piezas `video` o `faltante_video`.
- Cada día incluye `texto_linkedin` y `caption_instagram`.
- Los carruseles incluyen `carrusel`, `carrusel_slides` y `slides`.
- `slides` contiene el copy final. Diseño y render no pueden modificarlo.
- `carousel_news` incluye la ruta del newsletter aprobado.
- `live` exige aprobación completa.

## Formatos permitidos

- `video`.
- `carousel_news`.
- `post_carousel`.
- `faltante_video` con fallback de carrusel.

## Ejemplo de día con carrusel

```json
{
  "tipo": "metodo",
  "tema": "Cómo convertir una visión en programa",
  "lente_buyer": "innovacion",
  "objetivo": "mostrar el método",
  "formato": "carousel_news",
  "carrusel": "2026-08-03-mar",
  "carrusel_slides": 8,
  "slides": [
    {"lineas": ["Copy aprobado de la portada"]},
    {"lineas": ["Copy aprobado de la slide 2"]}
  ],
  "texto_linkedin": "Texto final aprobado.",
  "caption_instagram": "Caption final aprobado.",
  "newsletter": "newsletters/newsletter_2026-08-03.md"
}
```
