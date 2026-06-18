# CALENDARIO EDITORIAL MOTION
# Esta tabla la controla Paulo. El Estratega la lee y genera el próximo episodio con estado "pendiente".
# CADA TESIS se recorre desde los 4 TIPOS de mensaje (método Rubilar):
#   problema · metodo · resultados · conexion  (el Tipo define la narrativa cromática del carrusel)
# Estados: pendiente · generado · programado · publicado
# 4 tesis × 4 tipos = 16 episodios base (≈4 meses a ritmo semanal). Al terminar, se reinicia con evidencia nueva.

| Episodio | Tesis | Tipo | Estado |
|----------|-------|------|--------|
| ep1-1 | Cambio ≠ Transformación | problema | pendiente |
| ep1-2 | Cambio ≠ Transformación | metodo | generado |
| ep1-3 | Cambio ≠ Transformación | resultados | pendiente |
| ep1-4 | Cambio ≠ Transformación | conexion | pendiente |
| ep2-1 | La cultura es el sistema operativo | problema | pendiente |
| ep2-2 | La cultura es el sistema operativo | metodo | pendiente |
| ep2-3 | La cultura es el sistema operativo | resultados | pendiente |
| ep2-4 | La cultura es el sistema operativo | conexion | pendiente |
| ep3-1 | Modelos de gestión obsoletos → Transformación Continua | problema | pendiente |
| ep3-2 | Modelos de gestión obsoletos → Transformación Continua | metodo | pendiente |
| ep3-3 | Modelos de gestión obsoletos → Transformación Continua | resultados | pendiente |
| ep3-4 | Modelos de gestión obsoletos → Transformación Continua | conexion | pendiente |
| ep4-1 | Tecnología es commodity, el valor está en la orquestación | problema | pendiente |
| ep4-2 | Tecnología es commodity, el valor está en la orquestación | metodo | pendiente |
| ep4-3 | Tecnología es commodity, el valor está en la orquestación | resultados | pendiente |
| ep4-4 | Tecnología es commodity, el valor está en la orquestación | conexion | pendiente |

# REGLA PARA EL ESTRATEGA:
# 1. Si Paulo indicó un episodio específico al disparar la cascada (ej: ep3-1), generá ESE, ignorando el orden.
# 2. Si no indicó ninguno, tomá el PRIMER episodio con estado "pendiente" de arriba hacia abajo.
# 3. Usá la Tesis y el Tipo de esa fila. El Tipo define la paleta del carrusel:
#    problema=negro · metodo=violeta · resultados=naranja · conexion=aqua
# 4. Tras generar, cambiá el estado de esa fila a "generado".
