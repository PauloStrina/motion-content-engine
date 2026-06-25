# CALENDARIO EDITORIAL MOTION — Modelo de 8 semanas
# Esta tabla la controla Paulo. El Estratega la lee y genera la próxima semana con estado "pendiente".
# UNA SEMANA = 1 tesis + 2 formatos (2 episodios). El TIPO se asigna POR FORMATO:
#   Carousel  → problema (ep n-1) / resultados (ep n-3)   (idea fuerte, visual, audiencia fría)
#   Newsletter→ metodo   (ep n-2) / conexion   (ep n-4)   (profundidad, lectura elegida)
# Misma tesis toda la semana; carousel y newsletter NUNCA comparten ángulo.
# Estados: pendiente · generado · publicado
# 4 tesis × 4 tipos = 8 semanas (≈2 meses por vuelta). Espiral: al cerrar la semana 8 se reinicia
# todo a "pendiente" con evidencia/analogías nuevas (misma estructura).

| Semana | Tesis | Carousel (tipo) | Newsletter (tipo) | Estado |
|--------|-------|-----------------|-------------------|--------|
| 1 | T1 Cambio ≠ Transformación | ep1-1 Problema   | ep1-2 Método    | pendiente |
| 2 | T1 Cambio ≠ Transformación | ep1-3 Resultados | ep1-4 Conexión  | pendiente |
| 3 | T2 Cultura = sistema operativo | ep2-1 Problema   | ep2-2 Método    | pendiente |
| 4 | T2 Cultura = sistema operativo | ep2-3 Resultados | ep2-4 Conexión  | pendiente |
| 5 | T3 Transformación Continua®    | ep3-1 Problema   | ep3-2 Método    | pendiente |
| 6 | T3 Transformación Continua®    | ep3-3 Resultados | ep3-4 Conexión  | pendiente |
| 7 | T4 Tecnología commodity        | ep4-1 Problema   | ep4-2 Método    | pendiente |
| 8 | T4 Tecnología commodity        | ep4-3 Resultados | ep4-4 Conexión  | pendiente |

# REGLA PARA EL ESTRATEGA:
# 1. Si Paulo indicó una semana (1-8) al disparar la cascada, generá ESA (los 2 episodios).
# 2. Si no indicó ninguna, tomá la PRIMERA semana con estado "pendiente" de arriba hacia abajo.
# 3. Generá SIEMPRE los 2 episodios de la semana: primero el carousel, después el newsletter.
#    - Carousel (problema/resultados): linkedin_paulo (PDF) + instagram (HEM) + x_paulo (hilo) + linkedin_motion.
#    - Newsletter (metodo/conexion): newsletter .md (manual) + instagram_newsletter (carrusel news) + x_paulo (hilo).
# 4. El Tipo define la paleta del carrusel: problema=negro · metodo=violeta · resultados=naranja · conexion=aqua
# 5. Tras generar ambos, cambiá el estado de esa fila a "generado".
