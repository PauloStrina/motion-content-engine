# MOTION CONTENT ENGINE — Documento Maestro / CLAUDE.md
> Memoria única del proyecto. Lo leen: chats nuevos de Claude, Claude Code, y vos.
> Si una definición no está acá, no existe para el sistema. Mantener actualizado.
> Última actualización: junio 2026.

---

## 0. QUÉ ES ESTO
Máquina automatizada de comunicación y marketing para **Motion**, consultora de Transformación Digital (Argentina). Fundador: Paulo Strina (no técnico — hace clics, Claude escribe el código). Genera, diseña y programa contenido multicanal con aprobación humana antes de publicar.

Stack: GitHub Actions (orquestación) + Claude Code Action (agentes IA) + WeasyPrint (diseño en código) + Blotato (publicación). Dos repos: `motion-content-engine` (privado, el cerebro) y `motion-media` (público, solo imágenes para que Blotato las lea por URL).

---

## 1. ESTRATEGIA (el "porqué")

### Negocio
Motion acelera Transformación Digital. Diferenciador: integración **Negocio + Tecnología + Cultura**. Concepto propietario: **Transformación Continua®**. Lema: "Lo complejo, simple". Dos unidades: (1) Consultoría Estratégica (decisor: CEO/Dirección), (2) Talent Suite (SaaS RRHH). Newsletter LinkedIn "Lo complejo, simple": 399 subs (métrica base).

### Buyer Persona — "El Visionario de la Transformación"
CEO/Dirección de empresas 300-1000 empleados. YA sabe que necesita transformarse; le incomoda no haber empezado. NO le falta convicción: le falta el CÓMO (método, argumentos). Insight central: **el contenido EQUIPA, no persuade** — cada pieza es "munición" que el visionario reenvía a su directorio.

### Las 4 Tesis (hipótesis centrales)
1. **Cambio ≠ Transformación** (tesis madre): el cambio es transaccional (dolor→solución); la transformación nace de una visión y atraviesa procesos, liderazgo y cultura.
2. **La cultura es el sistema operativo**: no hay TD sin transformación cultural (absorbe "implementar IA ≠ adoptar IA").
3. **Modelos de gestión tradicionales obsoletos → nace Transformación Continua**.
4. **Tecnología es commodity; el valor está en la orquestación** (Service as a Software, "Orquestadores").

Premisa de contexto (encabeza todo, NO es tesis): "Salto Tecnológico" — entorno macro desafiante + disrupción IA + exceso de info/crisis de propósito.

### Los 4 Tipos de mensaje (método Rubilar) — ESQUEMA MENSUAL (vigente desde jul 2026)
Cada tesis se recorre desde 4 ángulos: **problema · método · resultados · conexión**.
→ **1 mes = 4 semanas = las 4 tesis** (una tesis por semana). Cada semana publica lun-jue, un tipo por día en orden FIJO (arco de persuasión): **lunes problema · martes método · miércoles resultados · jueves conexión**. Cada tesis reaparece mensualmente. Espiral: cada mes nuevo reusa la matriz con evidencia/analogías nuevas.
Formatos por semana (regla dura: **2 videos por semana**, los asigna la cascada según stock del banco de reels): 2 días video (mismo reel LinkedIn+IG, caption propio) · 1 día carousel+newsletter LinkedIn (mismo tema: newsletter se explaya, carrusel sintetiza; carrusel compartido con IG) · 1 día post largo LinkedIn + carousel IG. Newsletter se publica manual (Blotato no la soporta).
(El esquema semanal anterior de 8 semanas queda LEGACY: workflows 1-cascada-semanal y 2-motor-completo se conservan hasta validar el mensual.)

---

## 2. VOZ DE MARCA (Brand Voice Playbook — resumen)
- **Antítesis como figura madre**: cambio/transformación, SaaS/Service as a Software, implementar/adoptar IA.
- **Analogías culturales perspicaces** "ni básicas ni fantásticas": caso auto/tráfico ("comprar tecnología esperando transformarte es como cambiar el auto para escapar del tráfico — el problema no es el vehículo, es el sistema"), heladeros de Disney.
- "Metodología/método" = palabra martillo.
- Títulos de newsletter CLAROS, no de intriga.
- "La acción supera a la reflexión": los mejores posts nacen de actividad real, no de abstracción.
- El entusiasmo como motor de la transformación.
- **Prohibido**: clichés ("subite al tren de la IA"), terrorismo de obsolescencia, "en un mundo cada vez más digital...".

---

## 3. SISTEMA DE DISEÑO VISUAL (kit fijo, codificado)
Carrusel 1080×1350 (4:5). Fuentes ORIGINALES (en repo): Futura Std Condensed ExtraBold (display), Gotham Narrow Medium (metadata), Lyon Display + Lyon Text (serif editorial).
Colores: naranja #FF5000 · violeta #50235A · aqua #9DEDE3 · negro #1A1A1A.

### Kit de 3 tratamientos (roles fijos, el Diseñador NO improvisa)
1. **Eco vertical**: palabra repetida 3× con opacidad decreciente (DOLOR/EL CÓMO). Para palabra héroe sola.
2. **Degradé laminado 10px MONOCOLOR**: resalta palabras. Sombra ÚNICA elegida por render.py según fondo (violeta sobre fondos claros, aqua sobre oscuros). NUNCA más de un color de sombra. (Se descartaron: glitch/mitades, sombra dura tricolor, extrusión 3D.)
3. **Contraste serif Lyon**: para analogías y momentos editoriales.

### Narrativa cromática por tipo de mensaje
La portada lleva el color del tipo: **problema=negro · método=violeta · resultados=naranja · conexión=aqua**. El interior gira de fondo cuando el argumento gira.

### Plantilla estructural por tipo (arquitectura, no solo color)
Cada tipo hereda un tratamiento dominante del kit + arquitectura de slides propia:
- problema → eco vertical · contraste binario dolor↔visión · cierre = pregunta sola.
- metodo → laminado + lista numerada · pasos 1→2→3 · cierre = principio.
- resultados → plantilla dato · una métrica/slide antes→después · cierre = transformación.
- conexion → serif Lyon editorial · analogía cultural · cierre = creencia anclada.
Recombina lo existente: cero código nuevo. El detalle operativo vive en PROMPT_disenador.md.

### Plantillas estáticas (render_static.py, 1080×1080)
quote card · dato (número con sombra laminada) · lista numerada. (Quote card: calidad pendiente de pulir.)

---

## 4. ARQUITECTURA TÉCNICA

### El contrato: MANIFIESTO SEMANAL (nombrado por fecha, organizado por BLOQUES)
Fuente ÚNICA de verdad. UN JSON por semana, `manifiestos/manifiesto_<fecha>.json` (`<fecha>` = lunes, YYYY-MM-DD). Organizado por BLOQUES de contenido: cada bloque agrupa su cabecera (post/caption/hilo) + sus 8 slides JUNTAS, para revisarlo en conjunto. El newsletter (artículo) va aparte (`newsletters/newsletter_<fecha>.md`, manual). Estructura:
```
{ "fecha_inicio":"<fecha>","semana":N,"tesis","estado",
  "carousel": {tipo:"problema|resultados", tema, carrusel:"<fecha>", carrusel_slides:8,
               post_linkedin, caption_instagram, hilo_twitter:[...], slides:[{lineas:[...]} x8]},   // martes
  "institucional": {post_linkedin_motion},                                                          // miércoles
  "newsletter": {tipo:"metodo|conexion", tema, carrusel:"<fecha>-news", carrusel_slides:8,
                 caption_instagram, hilo_twitter:[...], slides:[{lineas:[...]} x8]} }               // jueves
```
El copy de las slides lo escribe el Redactor (voz) y se inyecta en el render (Paulo lo edita acá). `manifiesto.pieza()` arma la pieza por canal desde estos bloques. Carousel y newsletter comparten tesis, NUNCA ángulo. Día/hora fijos por canal (CANAL_SCHEDULE en publicador.py); la programación se ancla a `fecha_inicio`.

### Render (no usa Chrome — no disponible en sandbox)
WeasyPrint (HTML/CSS→PDF) + pdftoppm (PDF→PNG). `render.py` paramétrico lee JSON de slides (`--png` exporta imágenes). `generar_carrusel.py` deriva nombre y cantidad de slides DEL MANIFIESTO (garantiza congruencia de nombres con el publicador).

### Publicación (Blotato)
`publicador.py` lee el manifiesto, cada canal SU pieza. Resiliente: captura error por canal y sigue. Reintentos automáticos (429/500), pausa entre canales.
- Imágenes: URLs públicas de `motion-media` vía GitHub Pages (https://ops-motionco.github.io/motion-media/carruseles/). NO base64 (Blotato lo rechaza).
- LinkedIn Motion = cuenta de Paulo (25264) + **pageId 105691334** dentro de `target` (NO es un accountId).
- Modo: la programación se ancla a `fecha_inicio` (martes/miércoles/jueves de esa semana) → editable en calendario Blotato. NADA se publica sin OK final de Paulo.

### accountIds Blotato (verificados)
- linkedin_paulo: 25264 · x_paulo_hem y x_paulo_news: 20492 (misma cuenta Twitter, distinto día) · instagram e instagram_newsletter: 53650 · linkedin_motion: usa 25264 + pageId 105691334.

### Secrets en GitHub (repo motion-content-engine)
ANTHROPIC_API_KEY · BLOTATO_API_KEY · MEDIA_REPO_TOKEN (fine-grained, Contents:write solo sobre motion-media).

---

## 5. FLUJO DE TRABAJO MENSUAL
**Alimentar el banco** (cuando Paulo graba, las veces que haga falta):
1. Grabar sesión larga → Actions `3-reels-guion` (link Drive + slug) → revisar manifiesto de reels → `4-reels-render` → revisar los MP4 del artifact.
2. Actions → `5-banco-reels` → indicar slug + qué reels aprobás ("todos" o "1,3,5"). Sube los MP4 a motion-media/reels/ y los registra en banco/reels/catalogo.json con tesis+tipo. El catálogo muestra el stock por tesis/tipo (qué falta grabar).

**Generar y publicar el mes**:
**Paso 1** (Paulo, 1 clic): Actions → `1-cascada-mensual` → mes (YYYY-MM) + primer lunes (YYYY-MM-DD).
**Paso 2** (máquina): lee CALENDARIO (matriz de temas) + banco + voz → escribe manifiestos/mes_<YYYY-MM>.json (4 semanas × 4 días, 2 videos/semana reservados del banco o FALTANTES marcados con qué grabar) + JSONs de slides de todos los carruseles + 4 newsletters .md. Commit.
**Paso 3** (Paulo): revisar el manifiesto mensual + newsletters. Si hay faltantes de video: grabar y pasar por el banco, después editar el manifiesto (formato→video + reel_id). ← momento de criterio.
**Paso 4** (Paulo, 1 clic): Actions → `2-motor-mensual` → mismo mes + modo (dry/live).
**Paso 5** (máquina): render de todos los carruseles → push a motion-media → programa el MES completo en Blotato (16 días × LinkedIn 09:00 + Instagram 12:00; videos vía presigned upload al CDN de Blotato) → marca reels como publicados en el catálogo.
**Paso 6** (Paulo): OK final en calendario Blotato + publicar las 4 newsletters a mano en su día.

Cadencia: 1 mes = 1 manifiesto mensual = 1 corrida de cada workflow. Combustible: sesiones de grabación (el banco avisa qué tesis/tipo escasean) + evidencias.

### LEGACY (esquema semanal viejo, hasta validar el mensual)
`1-cascada-semanal` + `2-motor-completo` + manifiesto_<fecha>.json semanal (6 canales con X/Twitter e institucional). El esquema mensual NO incluye X ni linkedin_motion por ahora (decisión pendiente de Paulo).

---

## 6. ESTADO ACTUAL
✅ Cascada de texto · ✅ Carruseles · ✅ Quote/dato/lista · ✅ Publicación 4 canales (ep1-2 programado en Blotato, modo revisión) · ✅ Calendario editorial · ✅ Manifiesto dinámico punta a punta.
✅ **Motor de reels** (pipelines/video/): grabación larga → whisper con timestamps por palabra → Editor de Video IA elige reels según estrategia (manifiesto_reels.json, Paulo revisa) → corte ffmpeg sin silencios → branding con **Remotion** (subtítulos karaoke animados con pop por palabra, título en caja del color del tipo, logo; fuentes como fuentes de sistema en CI, NUNCA FontFace/loadFont — congela el renderer) → artifacts para revisión (incluye `_control.png` de validación visual). Workflows `3-reels-guion` y `4-reels-render` (inputs: link Drive + slug; opcional video de pantalla → modo split). Modos de encuadre: crop (cámara sola) · split (2 archivos: pantalla+cámara) · zonas (stream compuesto, coordenadas en el manifiesto; calibrar con workflow `debug-frame`). Validado end-to-end con 2 sesiones reales (conceptos + charla CAEII). Modo split sin probar con material real.
🚧 **Esquema mensual** (jul 2026): banco de reels (`banco/reels/catalogo.json` + workflow `5-banco-reels`, MP4s en motion-media/reels/) + cascada mensual (`1-cascada-mensual`, PROMPT_mes.md, manifiestos/mes_<YYYY-MM>.json) + motor mensual (`2-motor-mensual`, publicador_mes.py con video vía presigned upload a Blotato). Construido, SIN correr aún — falta poblar el banco y probar el primer mes en dry.
⏸️ Standby: motion graphics conceptuales (svganim.py validado técnicamente, falta pulido de composición — espera modelo de mayor capacidad).

---

## 7. PENDIENTES
**Inmediato**: subir sistema-final + calendario al repo; borrar obsoletos (ver §8); probar flujo en dry; OK final ep1-2 en Blotato.
**Corto**: crear Banco de Evidencias (evidencias/banco.md); validar dato "x4 ROI" antes de uso público; generar ep siguiente de punta a punta; pulir quote card; alinear 8→7 slides del ejemplo; limpieza de PNG huérfanos al regenerar.
**Mediano**: motion graphics conceptuales (líneas+pelotitas, estilo referencias del usuario); reels v2 (tracking de cara, modo marco automático, publicación de video vía Blotato); newsletter LinkedIn (verificar si Blotato lo soporta — probable que quede manual).
**Estratégico**: Capa 4 — métricas y aprendizaje; salto a Claude Code con este CLAUDE.md; Armar el embudo de low to high ticket.

---

## 8. LIMPIEZA DEL REPO (borrar — son del diseño viejo)
- scripts/publish_blotato.py (→ publicador.py)
- .github/workflows/: publicar-blotato.yml, publicar-instagram.yml, motor-completo.yml (viejo sin número), render-visuales.yml (viejo), cascada-semanal.yml (viejo)
- carpeta queue/ entera (reemplazada por manifiestos/)
Activos correctos: 1-cascada-semanal.yml, 2-motor-completo.yml, scripts/{manifiesto,publicador,generar_carrusel}.py, scripts/PROMPT_*.md, CALENDARIO_EDITORIAL.md, config.yaml, manifiestos/, design-system/.

---

## 9. BANCO DE EVIDENCIAS (a crear: evidencias/banco.md)
Formato por entrada: Caso/cliente · Sector · Qué hicimos · Resultado (número) · Uso público (SÍ anonimizado / SÍ con nombre / NO) · Fuente del dato.
Regla: el banco es fuente útil de datos/casos, NO un candado. El Redactor puede usar números/casos cuando aporten. Paulo revisa y aprueba TODO antes de publicar (modo revisión en Blotato) y se hace cargo de la veracidad.

---

## 10. REGLAS DE ORO (para cualquier Claude que retome esto)
1. El cerebro está en los DOCUMENTOS (estrategia), no en el código. Cambiar comportamiento = editar documento, no código.
2. Cada canal su pieza propia. Nunca cruzar contenido entre canales.
3. Usar números/casos cuando aporten. Paulo revisa y aprueba TODO antes de publicar y se hace cargo (el banco es fuente, no candado).
4. Nada se publica sin OK humano de Paulo (modo revisión en Blotato).
5. El manifiesto es la fuente de verdad. Nombres y cantidades salen de ahí.
6. Paulo no es técnico: explicar como a alguien que hace clics, guías paso a paso, sin jerga.
7. Honestidad sobre límites: no prometer lo que el sistema no hace.
