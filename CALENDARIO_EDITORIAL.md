# CALENDARIO EDITORIAL MOTION — Modelo de 8 semanas (1 manifiesto por semana)
# Esta tabla la controla Paulo. La cascada lee la primera semana "pendiente" (o la que Paulo indique).
# UNA SEMANA = 1 tesis + 2 contenidos, todo en UN manifiesto nombrado por la fecha del lunes:
#   Carousel  → problema (semana A) / resultados (semana B)   (idea fuerte, visual; sale martes)
#   Newsletter→ metodo   (semana A) / conexion   (semana B)   (profundidad; sale jueves)
# Misma tesis toda la semana; carousel y newsletter NUNCA comparten ángulo.
# Estados: pendiente · generado · publicado
# 4 tesis × 4 tipos = 8 semanas (≈2 meses por vuelta). Espiral: al cerrar la semana 8 se reinicia
# todo a "pendiente" con evidencia/analogías nuevas (misma estructura).

| Semana | Tesis | Carousel (tipo) | Newsletter (tipo) | Estado |
|--------|-------|-----------------|-------------------|--------|
| 1 | T1 Cambio ≠ Transformación | Problema   | Método    | generado |
| 2 | T1 Cambio ≠ Transformación | Resultados | Conexión  | pendiente |
| 3 | T2 Cultura = sistema operativo | Problema   | Método    | pendiente |
| 4 | T2 Cultura = sistema operativo | Resultados | Conexión  | pendiente |
| 5 | T3 Transformación Continua®    | Problema   | Método    | pendiente |
| 6 | T3 Transformación Continua®    | Resultados | Conexión  | pendiente |
| 7 | T4 Tecnología commodity        | Problema   | Método    | pendiente |
| 8 | T4 Tecnología commodity        | Resultados | Conexión  | pendiente |

# REGLA PARA LA CASCADA:
# 1. Paulo indica la FECHA (lunes de la semana) y, opcional, la semana (1-8).
# 2. Si no indica semana, tomá la PRIMERA "pendiente" de arriba hacia abajo.
# 3. Generá UN manifiesto semanal (manifiestos/manifiesto_<fecha>.json) con los 6 canales:
#    - Carousel (martes): linkedin_paulo (PDF) + instagram (HEM) + x_paulo_hem (hilo)
#    - Institucional (miércoles): linkedin_motion
#    - Newsletter (jueves): instagram_newsletter (carrusel news) + x_paulo_news (hilo) + newsletter_<fecha>.md (manual)
# 4. Paleta del carrusel HEM por tipo: problema=negro · resultados=naranja.
# 5. Tras generar, cambiá el estado de esa fila a "generado".
