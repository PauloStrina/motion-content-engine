# PLAN MAESTRO — Sistema de Comunicación y Marketing MOTION
**Versión 1.0 — junio 2026** · Documento vivo: se actualiza con cada decisión del proyecto.

---

## 1. Visión del sistema

Una máquina de generación de demanda B2B que va de la estrategia a la ejecución con mínima intervención humana: construye autoridad alrededor de las tesis de Motion, **equipa** al Visionario de la Transformación con municiones, lo hace avanzar por un flow-map de conversión hacia las dos unidades de negocio (Consultoría y Talent Suite), y aprende de sus propias métricas. Humano solo en dos puntos: insumo pilar y aprobación.

```
CAPA 1 · ESTRATEGIA  →  CAPA 2 · FÁBRICA  →  CAPA 3 · DISTRIBUCIÓN  →  CAPA 4 · APRENDIZAJE
(tesis, persona,         (agentes Claude:       (aprobación humana →      (MCP métricas →
 strategy packs)          redacción, diseño,     Blotato → canales +       Agente Analista →
        ↑                 video, render)         flow-map de conversión)   retro mensual)
        └──────────────────────── el loop cierra acá ←──────────────────────────┘
```

---

## 2. Registro de decisiones (cerradas — no se reabren salvo pedido explícito o razón fuerte)

| # | Decisión | Fecha |
|---|---|---|
| D1 | Embudos Consultoría y Talent Suite en paralelo: una máquina, un mensaje madre, dos lentes (negocio / talento). Regla 70% autoridad / 30% producto | jun 2026 |
| D2 | Esquema editorial: **Motor de Tesis** (reemplaza Content Waterfall). 4-5 tesis → series argumentales → episodios multiformato | jun 2026 |
| D3 | Pieza pilar: **Sesión Pilar semanal** (25-30 min de grabación del fundador). Podcast = pilar bonus, no estructural | jun 2026 |
| D4 | Capa 1 **switchable** vía Strategy Packs (`/strategies/` + config). Capa de identidad (tesis, voz, persona) constante; metodología intercambiable, revisión trimestral | jun 2026 |
| D5 | Orquestación: **Claude Code headless + GitHub Actions (cron)**. Sin n8n (reconsiderar solo si el operador deja de ser técnico) | jun 2026 |
| D6 | Visual estático: **sistema de diseño como código** (HTML/CSS con tokens Motion) renderizado a PNG/PDF por el Agente Diseñador. Sin Canva | jun 2026 |
| D7 | Video: pipeline propio (Whisper + selección por Claude + ffmpeg con subtítulos brandeados). Sin Opus Clip | jun 2026 |
| D8 | Publicación: **Blotato vía API** — solo como tubería de distribución; el cerebro de contenido es propio | jun 2026 |
| D9 | Métricas: **MCP server propio** (Meta Graph API + LinkedIn org API + Metricool API). Perfil personal de LinkedIn: export mensual (límite de LinkedIn, no de la arquitectura) | jun 2026 |
| D10 | Canales: LinkedIn fundador (voz de tesis) · Newsletter LinkedIn (capítulo profundo) · LinkedIn Motion (método y prueba) · **Showcase Page Talent Suite** (producto) · Instagram (cultura) · **+X/Twitter**. Expansión: retro mes 2 | jun 2026 |
| D11 | **Flow-map (Vender Sin Perseguir)** = capa de conversión permanente del Motor de Tesis. Principios adaptados a B2B; nunca copia literal del material de Rubilar | jun 2026 |
| D12 | Escalera de ofertas: Lead magnets gratis → low ticket (masterclass ejecutiva / kit de argumentos) → mid (Sprint 1,2,3-Boom, Diagnóstico) → high (Programa TD / Talent Suite) | jun 2026 |
| D13 | Lead magnet #1: **Chequeo de Madurez Digital** autoadministrado (informe-munición para el directorio) | jun 2026 |
| D14 | Lead magnet #2: **Experiencia IA de 5 minutos** ("tu informe para el directorio"): demo precargado, máx. 3 prompts copiar-pegar, primer resultado < 2 min; documento propio y playground = Nivel 2 post-wow. CTA → Chequeo | jun 2026 |
| D15 | Reglas editoriales: contenido que **equipa** (test de la munición) · regla de evidencia (artefacto/número/caso) · sustantivos propios · lenguaje de negocio · anti-persecución | jun 2026 |

---

## 3. Las 4 capas, instrumentadas y evolucionables

> Principio rector: **todo es un archivo versionado en el repo `motion-content-engine`**. Modificar el sistema = editar un archivo. Ampliarlo = agregar uno. Nada vive en la cabeza de nadie ni en una herramienta cerrada.

### CAPA 1 — Estrategia (el cerebro)
**Componentes:** `/strategy/tesis.md` · `/strategy/buyer-persona.md` (v2 ✓) · `/strategy/voz-motion.md` (pendiente) · `/strategy/banco-evidencias.md` (pendiente) · `/strategies/<pack>/` + `config.yaml` · `/strategy/flow-map.md`
**Cómo se modifica:** edición directa + commit. Cambios de tesis o pack: decisión humana en revisión trimestral. Cambios menores (frases nuevas del banco, evidencias): continuo.
**Cómo se amplía:** nuevos packs en `/strategies/`, nuevas tesis como archivos, nuevos personas por rol.

### CAPA 2 — Fábrica (los agentes)
**Componentes:** Skills versionadas (`/skills/redactor`, `/skills/disenador`, `/skills/video`, `/skills/estratega`) · plantillas visuales (`/design-system/`: tokens + templates HTML/CSS) · pipeline de video (`/video-pipeline/`).
**Cómo se modifica:** cada corrección tuya en la aprobación se traduce a un ajuste de skill (la máquina aprende una vez, no repite). Plantillas nuevas = nuevos archivos HTML.
**Cómo se amplía:** nuevos agentes como nuevos archivos de skill + entrada en el workflow (ej. futuro Agente de Newsletter externo, Agente de Webinars).

### CAPA 3 — Distribución y conversión
**Componentes:** workflow GitHub Actions (cron) · cola de aprobación (`/pending` → `/approved` + notificación) · publicación vía API Blotato · flow-map assets (Experiencia 5min, Chequeo de Madurez, escalera de ofertas) · mapeo canal-rol (D10).
**Cómo se modifica:** horarios y cadencias en un archivo de configuración; canales se agregan/quitan en la config de Blotato.
**Cómo se amplía:** nuevos canales (TikTok/YouTube) = una línea de config cuando el pipeline de video madure; nuevos lead magnets = nuevos assets con el molde de la Experiencia #1.

### CAPA 4 — Aprendizaje
**Componentes:** MCP server `motion-metrics` · Agente Analista (informe semanal automático) · retro mensual (humano + Claude) · revisión trimestral de estrategia.
**Cómo se modifica:** los KPIs por canal y por pack viven en `/strategy/metricas-norte.md`.
**Cómo se amplía:** nuevas fuentes de datos = nuevos endpoints del MCP (ej. analytics de la Experiencia, CRM, Chequeo completions → lead scoring).

---

## 4. Roadmap de construcción

**Principio: la máquina publica desde la semana 1.** No esperamos la automatización completa: las primeras semanas la fábrica opera en modo asistido (este proyecto de Claude produce, vos aprobás, se programa a mano) mientras se construye la versión autónoma por detrás. Contenido desde el día uno, automatización incremental.

| Fase | Qué se construye | Entregables | Esfuerzo tuyo |
|---|---|---|---|
| **F0 · Fundaciones** (sem 1-2) | Cierre de capa 1 | Brand Voice Playbook · Mapa de Tesis y series · Banco de Evidencias v1 · flow-map documentado | 2 sesiones de trabajo + grabación 1ª Sesión Pilar |
| **F1 · Fábrica asistida** (sem 1-3, en paralelo) | Producción real desde este proyecto | 1ª cascada semanal publicada · skills v1 calibradas con tus correcciones | Aprobación semanal (30-45 min) |
| **F2 · Automatización** (sem 3-6) | Repo + agentes headless + Blotato + cola de aprobación + design system en código + pipeline de video | Máquina autónoma con gate humano | Setup técnico del equipo (guiado) + aprobaciones |
| **F3 · Flow-map assets** (sem 5-8) | Experiencia IA 5min · Chequeo de Madurez Digital · Showcase Page · cadencia de newsletter | Escalera de conversión activa e instrumentada | Validación de specs + test con círculo de networking |
| **F4 · Loop de aprendizaje** (sem 7-9) | MCP métricas + Agente Analista + tablero | Retro mensual con datos; el sistema empieza a auto-mejorar | Retro mensual (60 min) |

### Rutinas permanentes (desde F1)
- **Lunes (30-40 min):** Sesión Pilar — el fundador graba el tema de la semana.
- **Martes (30-45 min):** aprobación de la cascada de la semana.
- **Diario (15 min):** engagement humano del fundador (lo único jamás automatizado).
- **Viernes (15 min):** pulso de métricas.
- **Mensual (60 min):** retro con datos → ajustes a skills y calendario.
- **Trimestral (90 min):** revisión de estrategia — tesis, packs, canales, escalera.

---

## 5. Insumos pendientes (bloqueantes suaves)
1. **Métricas actuales** de los 3 canales (línea base — aún no recibidas).
2. Sesión de trabajo para el **Brand Voice Playbook** (próximo entregable).
3. Insumos del **Banco de Evidencias**: 3-5 mini-casos con números, hallazgos recurrentes de diagnósticos.
4. Acceso/decisiones técnicas para F2: cuenta GitHub, alta en Blotato, API key de Anthropic.
