# PROMPT — CASCADA MENSUAL (Estratega + Redactor + Diseñador)
> Lo lee el agente del workflow `1-cascada-mensual`. Genera TODO el contenido de un mes en una corrida.
> Output principal: `manifiestos/mes_<YYYY-MM>.json` + slides de carruseles + 4 newsletters.

## MODELO MENSUAL
1 mes = 4 semanas = las 4 tesis (semana 1 → T1, semana 2 → T2, semana 3 → T3, semana 4 → T4).
Cada semana publica lunes a jueves, un tipo por día, orden FIJO:
**lunes problema · martes metodo · miércoles resultados · jueves conexion** (arco: tensión → solución → prueba → identificación).

Cada día tiene UNA pieza por canal (LinkedIn + Instagram). El formato del día lo decidís VOS
según el banco de reels, con esta regla dura:

### REGLA DE FORMATOS (no negociable)
- **Exactamente 2 días de la semana son VIDEO** (mismo reel en LinkedIn e Instagram, caption propio por canal).
- **1 día es CAROUSEL + NEWSLETTER**: carrusel de 8 slides (mismo asset LinkedIn+IG, copy propio por canal) + newsletter de LinkedIn del MISMO tema (el newsletter se explaya en profundidad, el carrusel sintetiza). El newsletter lo publica Paulo a mano.
- **1 día es POST LARGO (LinkedIn) + CAROUSEL (Instagram)**: mismo tema, formato distinto por canal.

### CÓMO ASIGNAR LOS VIDEOS (leé banco/reels/catalogo.json)
1. Para cada semana, mirá qué reels "disponible" hay con la tesis de esa semana.
2. Asignálos a los días cuyo tipo coincida (un reel tipo "metodo" va al martes, etc.).
3. Si hay más de 2 candidatos, elegí los 2 mejores para el arco de la semana (calidad del hook, variedad).
4. Si hay MENOS de 2 para esa tesis, asigná los que haya y marcá el resto como FALTANTE:
   `"formato": "faltante_video"` + campo `"grabar"` (texto: qué grabar — tesis, tipo, tema).
   NUNCA uses un reel de otra tesis ni inventes contenido para tapar el hueco. El día faltante
   lleva ADEMÁS todos los campos de un `post_carousel` (texto_linkedin largo + carrusel + slides
   + caption_instagram): ese es el fallback que el publicador usa si Paulo no llega a grabar.
   Si Paulo graba a tiempo, edita el manifiesto: cambia formato a "video" + reel_id.
5. Al reservar un reel: en catalogo.json cambiá su `estado` a "reservado" y `reservado_para`
   a la fecha del día (YYYY-MM-DD).
6. Los 2 días NO-video reciben los otros 2 formatos. Cuál recibe carousel+newsletter y cuál
   post largo+carousel: poné el **carousel+newsletter en el tipo con más profundidad conceptual**
   de esa semana (suele ser metodo o conexion) — el newsletter necesita sustancia para explayarse.

## PASO 0 — CONTEXTO (obligatorio, antes de escribir nada)
Leé COMPLETOS: strategy/VOZ_corpus.md (la voz — el más importante), strategy/tesis.md (matriz de
intención por tipo), strategy/voz-motion.md (formato por canal), strategy/buyer-persona.md,
evidencias/banco.md (datos/casos), CALENDARIO_EDITORIAL.md (la matriz de TEMAS del mes — los
temas salen de ahí, NO se inventan), banco/reels/catalogo.json (stock de videos).
Reglas de escritura, estructura #HistoriasEnMovimiento, y prohibiciones: scripts/PROMPT_redactor.md
(aplican TODAS las reglas de voz, formato y auto-crítica de ese documento a cada pieza).

## OUTPUT — manifiesto mensual: manifiestos/mes_<YYYY-MM>.json
```json
{
  "mes": "2026-08",
  "primer_lunes": "2026-08-03",
  "estado": "borrador_para_aprobacion",
  "semanas": [
    {
      "fecha_inicio": "2026-08-03",
      "tesis": 1,
      "tesis_nombre": "Cambio ≠ Transformación",
      "dias": {
        "lun": {
          "tipo": "problema", "tema": "el de la matriz del calendario",
          "formato": "video",
          "reel_id": "2026-07-03-conceptos_3",
          "texto_linkedin": "post que presenta el video (reglas HEM de PROMPT_redactor.md)",
          "caption_instagram": "caption corto propio + 2-3 hashtags"
        },
        "mar": {
          "tipo": "metodo", "tema": "...",
          "formato": "carousel_news",
          "carrusel": "2026-08-03-mar", "carrusel_slides": 8,
          "slides": [ {"lineas": ["..."]}, "... 8 slides ..." ],
          "texto_linkedin": "cabecera del carrusel en LinkedIn",
          "caption_instagram": "caption corto propio",
          "newsletter": "newsletters/newsletter_2026-08-03.md"
        },
        "mie": {
          "tipo": "resultados", "tema": "...",
          "formato": "post_carousel",
          "texto_linkedin": "POST LARGO (1200-2000 caracteres, desarrollo completo del tema con la voz de Paulo — este formato NO lleva carrusel en LinkedIn)",
          "carrusel": "2026-08-03-mie", "carrusel_slides": 8,
          "slides": [ "... 8 slides para el carrusel de Instagram ..." ],
          "caption_instagram": "caption corto propio"
        },
        "jue": {
          "tipo": "conexion", "tema": "...",
          "formato": "video",
          "reel_id": "...",
          "texto_linkedin": "...", "caption_instagram": "..."
        }
      }
    }
    // ... x4 semanas
  ]
}
```
- `formato` ∈ `video` · `carousel_news` · `post_carousel` · `faltante_video` (con campo `grabar` y
  fallback de carousel o post en el mismo día).
- `carrusel` se nombra `<fecha_inicio>-<dia>` y `carrusel_slides` = cantidad real de slides.
- Los días video NO llevan slides. Los días carousel llevan las 8 slides en el manifiesto
  (el copy es del Redactor; el Diseñador solo asigna diseño).

## ARCHIVOS ADICIONALES (misma corrida)
1. Por cada día con carrusel: `design-system/slides/<carrusel>.json` — el Diseñador toma el copy
   de `slides` VERBATIM y asigna tratamiento/color imitando el exemplar
   (`design-system/slides/EJEMPLO_HEM_carrusel.json`). Paleta por tipo:
   problema=negro · metodo=violeta · resultados=naranja · conexion=aqua.
2. Por cada semana: `newsletters/newsletter_<fecha_inicio>.md` — artículo completo del tema del
   día carousel_news (seguí scripts/PROMPT_newsletter.md). 4 newsletters por mes.
3. Actualizá banco/reels/catalogo.json (reservas) y la tabla MESES de CALENDARIO_EDITORIAL.md
   (estado "generado").

## REGLAS DE CALIDAD (no negociables)
- El arco semanal se tiene que SENTIR: el lunes abre una tensión que el martes responde, el
  miércoles prueba y el jueves ancla en una creencia. Leé la semana completa antes de entregarla.
- Cada canal contenido PROPIO: jamás repetir el texto de LinkedIn como caption de Instagram.
- Test de diferenciación carousel/newsletter (mismo día, mismo tema): si el newsletter se puede
  resumir en las slides, falló — el newsletter profundiza donde el carrusel no llega.
- Voz de Paulo SIEMPRE: auto-crítica de VOZ_corpus.md §5 en cada pieza. Si suena a IA, reescribí.
- Los captions de los días video: NO repitas el caption_sugerido del banco tal cual — es una
  referencia; reescribilo para el arco de la semana y el canal.

## AUTOCONTROL antes de terminar
- ¿Cada semana tiene exactamente 2 videos (o faltantes marcados con `grabar` + fallback)?
- ¿Los 4 tipos aparecen en orden lun→jue en las 4 semanas?
- ¿Reservaste en catalogo.json TODOS los reels usados?
- ¿4 newsletters generadas, una por semana, del tema del día carousel_news?
- ¿Cada carrusel del manifiesto tiene su JSON de slides en design-system/slides/?
- ¿Las piezas suenan a Paulo?
