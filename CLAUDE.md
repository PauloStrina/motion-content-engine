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

### Los 4 Tipos de mensaje (método Rubilar)
Cada tesis se recorre desde 4 ángulos: **problema · método · resultados · conexión**.
→ 4 tesis × 4 tipos = **16 episodios base** (~4 meses a ritmo semanal). Al terminar, se reinicia con evidencia/analogías nuevas (espiral, no círculo: la tesis se repite, la munición rota).

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

### Plantillas estáticas (render_static.py, 1080×1080)
quote card · dato (número con sombra laminada) · lista numerada. (Quote card: calidad pendiente de pulir.)

---

## 4. ARQUITECTURA TÉCNICA

### El contrato: MANIFIESTO por episodio
Fuente ÚNICA de verdad. Un JSON `manifiestos/manifiesto_<ep>.json` que conecta Redactor→Diseñador→Publicador. Nadie adivina ni hardcodea. Estructura:
```
{ "episodio","serie","tesis","tipo","estado",
  "canales": {
    "linkedin_paulo":  {activo, formato:"post", texto},        // post largo, tesis, 1ra persona
    "linkedin_motion": {activo, formato:"post", texto},        // institucional, método (DISTINTO)
    "x_paulo":         {activo, formato:"hilo", hilo:[...]},
    "instagram":       {activo, formato:"carrusel", caption (CORTO), carrusel:"<ep>", carrusel_slides:N}
  }}
```
REGLA DURA: cada canal su pieza propia. JAMÁS repetir el post de LinkedIn como caption de Instagram.

### Render (no usa Chrome — no disponible en sandbox)
WeasyPrint (HTML/CSS→PDF) + pdftoppm (PDF→PNG). `render.py` paramétrico lee JSON de slides (`--png` exporta imágenes). `generar_carrusel.py` deriva nombre y cantidad de slides DEL MANIFIESTO (garantiza congruencia de nombres con el publicador).

### Publicación (Blotato)
`publicador.py` lee el manifiesto, cada canal SU pieza. Resiliente: captura error por canal y sigue. Reintentos automáticos (429/500), pausa entre canales.
- Imágenes: URLs públicas de `motion-media` vía GitHub Pages (https://ops-motionco.github.io/motion-media/carruseles/). NO base64 (Blotato lo rechaza).
- LinkedIn Motion = cuenta de Paulo (25264) + **pageId 105691334** dentro de `target` (NO es un accountId).
- Modo: programar con fecha futura (48hs buffer) → editable en calendario Blotato. NADA se publica sin OK final de Paulo.

### accountIds Blotato (verificados)
- linkedin_paulo: 25264 · x_paulo: 20492 · instagram: 53650 · linkedin_motion: usa 25264 + pageId 105691334.

### Secrets en GitHub (repo motion-content-engine)
ANTHROPIC_API_KEY · BLOTATO_API_KEY · MEDIA_REPO_TOKEN (fine-grained, Contents:write solo sobre motion-media).

---

## 5. FLUJO DE TRABAJO SEMANAL
**Paso 1** (Paulo, 1 clic): Actions → `1-cascada-semanal` → Run → escribir episodio (ej. ep2-1) o vacío.
**Paso 2** (máquina): Estratega lee CALENDARIO_EDITORIAL.md, Redactor escribe el manifiesto (4 piezas), Diseñador genera JSON de slides. Commit al repo.
**Paso 3** (Paulo): revisar el manifiesto en el repo. Aprobar o pedir cambios. ← momento de criterio.
**Paso 4** (Paulo, 1 clic): Actions → `2-motor-completo` → Run → indicar episodio + modo (dry/live). SIEMPRE indicar episodio explícito (no confiar en "más reciente").
**Paso 5** (máquina): render carrusel → push PNG a motion-media → espera Pages → programa en Blotato.
**Paso 6** (Paulo): OK final en calendario Blotato. Recién ahí se publica.

Cadencia recomendada: 1 episodio/semana. Combustible: Paulo alimenta Banco de Evidencias + Playbook (1×/mes mínimo) o la rueda se seca en ~4 meses.

### Selección de episodio
- Salto puntual: escribir el código (ej. ep3-1) al disparar. Override manual.
- Cambio de plan: editar CALENDARIO_EDITORIAL.md (reordenar filas/estados).
- Nomenclatura: ep<TESIS>-<TIPO>. Ej: ep3-1 = tesis 3, tipo problema. (-1 problema, -2 método, -3 resultados, -4 conexión.)

---

## 6. ESTADO ACTUAL
✅ Cascada de texto · ✅ Carruseles · ✅ Quote/dato/lista · ✅ Publicación 4 canales (ep1-2 programado en Blotato, modo revisión) · ✅ Calendario editorial · ✅ Manifiesto dinámico punta a punta.
⏸️ Standby: motion graphics conceptuales (svganim.py validado técnicamente, falta pulido de composición — espera modelo de mayor capacidad).

---

## 7. PENDIENTES
**Inmediato**: subir sistema-final + calendario al repo; borrar obsoletos (ver §8); probar flujo en dry; OK final ep1-2 en Blotato.
**Corto**: crear Banco de Evidencias (evidencias/banco.md); validar dato "x4 ROI" antes de uso público; generar ep siguiente de punta a punta; pulir quote card; alinear 8→7 slides del ejemplo; limpieza de PNG huérfanos al regenerar.
**Mediano**: motion graphics conceptuales (líneas+pelotitas, estilo referencias del usuario); editor de reels desde grabación; plantilla estructural por tipo de mensaje (hoy solo varía el color, no el layout); newsletter LinkedIn (verificar si Blotato lo soporta — probable que quede manual).
**Estratégico**: Capa 4 — métricas y aprendizaje; salto a Claude Code con este CLAUDE.md.

---

## 8. LIMPIEZA DEL REPO (borrar — son del diseño viejo)
- scripts/publish_blotato.py (→ publicador.py)
- .github/workflows/: publicar-blotato.yml, publicar-instagram.yml, motor-completo.yml (viejo sin número), render-visuales.yml (viejo), cascada-semanal.yml (viejo)
- carpeta queue/ entera (reemplazada por manifiestos/)
Activos correctos: 1-cascada-semanal.yml, 2-motor-completo.yml, scripts/{manifiesto,publicador,generar_carrusel}.py, scripts/PROMPT_*.md, CALENDARIO_EDITORIAL.md, config.yaml, manifiestos/, design-system/.

---

## 9. BANCO DE EVIDENCIAS (a crear: evidencias/banco.md)
Formato por entrada: Caso/cliente · Sector · Qué hicimos · Resultado (número) · Uso público (SÍ anonimizado / SÍ con nombre / NO) · Fuente del dato.
Regla: el Redactor SOLO usa datos del banco con "Uso público: SÍ". Si un número no está, no se puede usar. Protege de publicar lo insostenible. (El "x4 ROI" NO está validado aún.)

---

## 10. REGLAS DE ORO (para cualquier Claude que retome esto)
1. El cerebro está en los DOCUMENTOS (estrategia), no en el código. Cambiar comportamiento = editar documento, no código.
2. Cada canal su pieza propia. Nunca cruzar contenido entre canales.
3. Nunca inventar datos/números/casos. Solo Banco de Evidencias.
4. Nada se publica sin OK humano de Paulo (modo revisión en Blotato).
5. El manifiesto es la fuente de verdad. Nombres y cantidades salen de ahí.
6. Paulo no es técnico: explicar como a alguien que hace clics, guías paso a paso, sin jerga.
7. Honestidad sobre límites: no prometer lo que el sistema no hace.
