# CALENDARIO EDITORIAL MOTION — Modelo de 8 semanas (1 manifiesto por semana)
# Esta tabla la controla Paulo. La cascada lee la primera semana "pendiente" (o la que Paulo indique).
# UNA SEMANA = 1 tesis + 2 contenidos (carousel + newsletter), todo en UN manifiesto nombrado por la fecha del lunes:
#   Carousel  → problema (semana A) / resultados (semana B)   (idea fuerte, visual; sale martes)
#   Newsletter→ metodo   (semana A) / conexion   (semana B)   (profundidad; sale jueves)
# Misma tesis toda la semana; carousel y newsletter NUNCA comparten ángulo.
# La columna TEMA fija de qué habla cada pieza: NO inventar un tema nuevo, usar ESTE (se puede afinar la redacción, no el tema).
# Estados: pendiente · generado · publicado

| Semana | Tesis | Carousel (tipo) | Tema carousel | Newsletter (tipo) | Tema newsletter | Estado |
|--------|-------|-----------------|---------------|-------------------|-----------------|--------|
| 1 | T1 Cambio ≠ Transformación | Problema   | ¿Cambio o Transformación? (la pregunta que casi nadie se hace a tiempo) | Método    | Cómo saber si tu organización busca un cambio o una transformación (antes de invertir) | generado |
| 2 | T1 Cambio ≠ Transformación | Resultados | Pidió un tablero, encontró una transformación (efecto cebolla) | Conexión  | Por qué elegimos trabajar con quien se siente incómodo | generado |
| 3 | T2 Cultura = sistema operativo | Problema   | La brecha Copilot: quedarse en la herramienta (Power BI sobre stack Google) | Método    | Implementar ≠ adoptar IA · el Laboratorio de IA | pendiente |
| 4 | T2 Cultura = sistema operativo | Resultados | Adopción real de IA + evidencia | Conexión  | Organizaciones más conscientes · los Heladeros de Disney | pendiente |
| 5 | T3 Transformación Continua®    | Problema   | Obituarios de los modelos de gestión tradicionales | Método    | Los 6 principios de Transformación Continua® | pendiente |
| 6 | T3 Transformación Continua®    | Resultados | Los 3 rieles del Programa (proyectos en marcha) | Conexión  | No se gestiona el cambio: se diseña la organización para vivir en cambio | pendiente |
| 7 | T4 Tecnología commodity        | Problema   | La trampa del enlatado | Método    | Service as a Software | pendiente |
| 8 | T4 Tecnología commodity        | Resultados | El ROI de orquestar a medida (caso) | Conexión  | Orquestadores: el perfil profesional emergente | pendiente |

# REGLA PARA LA CASCADA:
# 1. Paulo indica la FECHA (lunes de la semana) y, opcional, la semana (1-8).
# 2. Si no indica semana, tomá la PRIMERA "pendiente" de arriba hacia abajo.
# 3. El TEMA de cada pieza SALE de la columna Tema. NO inventes un tema nuevo. Podés afinar el título, no el tema.
# 4. Generá UN manifiesto semanal (manifiestos/manifiesto_<fecha>.json) con los 6 canales:
#    - Carousel (martes): linkedin_paulo (PDF) + instagram (HEM) + x_paulo_hem (hilo)
#    - Institucional (miércoles): linkedin_motion
#    - Newsletter (jueves): instagram_newsletter (carrusel news) + x_paulo_news (hilo) + newsletter_<fecha>.md (manual)
# 5. Paleta del carrusel HEM por tipo: problema=negro · resultados=naranja.
# 6. Tras generar, cambiá el estado de esa fila a "generado".
