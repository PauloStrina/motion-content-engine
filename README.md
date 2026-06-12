# MOTION CONTENT ENGINE
Máquina de comunicación y marketing de Motion. Capa 1 (estrategia) + Capa 2 (fábrica) + Capa 3 (distribución) + Capa 4 (aprendizaje).
**Principio:** todo es un archivo versionado. Humano solo en: insumo (opcional) y aprobación (obligatoria).

## Estructura
- `strategy/` — el cerebro: tesis, buyer persona, voz, plan maestro. Los agentes leen SIEMPRE de acá.
- `skills/` — prompts de los 6 agentes.
- `design-system/` — identidad como código: tokens + plantillas HTML + render a PNG/PDF.
- `pipelines/video/` — corte de reels y motion graphics.
- `queue/` — pending (borradores) → approved (tu OK) → published.
- `automation/` — GitHub Actions: cascada semanal y publicación.
- `scripts/` — publicación vía Blotato API.
- `evidencias/` — Banco de Evidencias.

## Setup (una tarde técnica)
1. Crear repo privado en GitHub y pushear este contenido. Mover `automation/.github` a la raíz como `.github`.
2. Secrets del repo (Settings → Secrets → Actions): `ANTHROPIC_API_KEY`, `BLOTATO_API_KEY`, `NOTIFY_EMAIL`.
3. Copiar fuentes (.woff2) y logos (SVG) de Motion a `design-system/assets/` y completar los hex reales en `tokens.css` desde el manual de Oficina Robot (los actuales son APROXIMADOS — TODO marcado).
4. Render local de prueba: `cd design-system/render && npm i puppeteer && node render.js ../templates/carousel.html demo.json`
5. Crear cuenta Blotato, conectar canales, pegar API key. Completar endpoint real en `scripts/publish_blotato.py` según docs de Blotato (marcado TODO).
6. Probar el workflow manualmente: Actions → "cascada-semanal" → Run workflow.
7. Flujo diario: borradores aparecen en `queue/pending/` → revisás → movés a `queue/approved/` (commit) → el workflow de publicación los programa.

## Reglas duras
- `aprobacion.modo` jamás pasa a automático.
- Ningún agente inventa números: si no está en `evidencias/`, no se publica.
- Las API keys viven SOLO en GitHub Secrets, nunca en el código.
