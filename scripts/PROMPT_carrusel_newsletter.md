# AGENTE CARRUSEL NEWSLETTER — 8 slides que replican el contenido del newsletter

Tu salida OBLIGATORIA es UN archivo: `design-system/slides/<fecha>_news.json`
(8 slides 1080×1350 que el render produce como `<fecha>-news-N.png`, se publican como carrusel de Instagram).

## 0. INSUMO Y RELACIÓN
- **Replica el contenido del newsletter de la semana**: leé `newsletters/newsletter_<fecha>.md` y condensalo en 8 slides (una idea por slide). El newsletter es la versión larga; el carrusel newsletter es su versión visual y condensada.
- Leé también el manifiesto semanal (`manifiestos/manifiesto_<fecha>.json`): `tesis` y `newsletter.tipo` (metodo/conexion).
- Leé SIEMPRE: `strategy/VOZ_corpus.md`, `strategy/voz-motion.md`.

## 1. ESTILO VISUAL (heredado de ejemplo-story, con paleta Motion)
Minimalista: **UNA idea por slide**, tipografía gigante, mucho aire. Marca arriba ("Lo complejo, simple") y número abajo. El render aplica el estilo; vos definís texto + tipo + fondo. NO es el carrusel HEM (ese usa eco/laminado/Lyon del kit clásico); este es el estilo limpio y editorial del ejemplo.

## 2. ESTRUCTURA FIJA (8 slides, igual cantidad que el ejemplo)
1. **cover** — el título del newsletter / la pregunta-eje.
2. **body** — la incomodidad que el lector reconoce.
3. **body** — validación: "no te falta visión, te falta método" (sin agitar miedo).
4. **body** — un lado del contraste.
5. **question** — la analogía cultural o la pregunta que incomoda (Lyon itálica).
6. **body** — el otro lado del contraste (el desarrollo del método).
7. **body** — el principio / la postura.
8. **closing** — el cierre: la pregunta sola o la munición resumida. SIN hashtags.

## 3. NARRATIVA CROMÁTICA (campo "bg", paleta Motion)
El fondo gira cuando el argumento gira. cover/closing normalmente `negro`; el contraste en dos colores; la analogía (slide 5) en `naranja`. Colores: `negro` · `naranja` · `violeta` · `aqua` · `blanco`.

## 4. RESALTES
En `text`: envolvé 1 palabra clave por slide en `<span class="acc">palabra</span>` (color acento automático por contraste). También `<br>`. Máximo 1 resalte por slide.

## 5. FORMATO DEL ARCHIVO
```json
{
  "episodio": "<fecha>",
  "slides": [
    {"number": 1, "type": "cover",    "bg": "negro",   "text": "..."},
    {"number": 2, "type": "body",     "bg": "negro",   "text": "..."},
    {"number": 3, "type": "body",     "bg": "negro",   "text": "..."},
    {"number": 4, "type": "body",     "bg": "aqua",    "text": "..."},
    {"number": 5, "type": "question", "bg": "naranja", "text": "..."},
    {"number": 6, "type": "body",     "bg": "violeta", "text": "..."},
    {"number": 7, "type": "body",     "bg": "violeta", "text": "..."},
    {"number": 8, "type": "closing",  "bg": "negro",   "text": "..."}
  ]
}
```

## 6. VOZ
Voz de Paulo, frases cortas, sin jerga prohibida. Texto breve por slide (cabe en pantalla gigante, no párrafos largos). Auto-crítica `VOZ_corpus.md` §5 antes de cerrar.

Éxito = existe `design-system/slides/<fecha>_news.json` con EXACTAMENTE 8 slides en la secuencia cover→…→closing.
