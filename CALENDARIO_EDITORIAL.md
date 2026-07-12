# CALENDARIO EDITORIAL MOTION — Modelo MENSUAL (1 corrida = 1 mes = 4 semanas = las 4 tesis)
# Esta tabla la controla Paulo. La cascada mensual genera TODO el contenido del mes en una corrida.
#
# ESTRUCTURA DEL MES:
#   1 semana = 1 tesis (semana 1 → T1, semana 2 → T2, semana 3 → T3, semana 4 → T4).
#   Cada semana publica de lunes a jueves, un TIPO por día, en este orden FIJO (arco de persuasión):
#     LUNES     → problema    (abrir la tensión)
#     MARTES    → metodo      (el cómo — palabra martillo)
#     MIÉRCOLES → resultados  (la prueba: números, casos)
#     JUEVES    → conexion    (analogía/creencia — lo más compartible, cierra la semana)
#
# FORMATOS (regla dura: exactamente 2 VIDEOS por semana):
#   - 2 días son VIDEO: mismo reel en LinkedIn + Instagram, caption propio por canal.
#     QUÉ días son video lo decide la cascada mirando el BANCO DE REELS (banco/reels/catalogo.json):
#     usa video en los días cuyo tipo tenga stock disponible para la tesis de la semana.
#   - 1 día es CAROUSEL + NEWSLETTER: carrusel (mismo asset LinkedIn + IG, copy propio) y
#     newsletter de LinkedIn del MISMO tema (el newsletter se explaya, el carrusel sintetiza).
#     El newsletter lo publica Paulo a mano (Blotato no soporta newsletters de LinkedIn).
#   - 1 día es POST LARGO (LinkedIn) + CAROUSEL (Instagram): mismo tema, formato por canal.
#   Si el banco no tiene 2 videos para la tesis de la semana, la cascada lo marca como FALTANTE
#   en el manifiesto y sugiere qué grabar. No se inventa: se avisa.
#
# TEMAS (matriz tesis × tipo — la cascada usa ESTOS temas, no inventa):

| Tesis | problema (lun) | metodo (mar) | resultados (mié) | conexion (jue) |
|-------|----------------|--------------|------------------|----------------|
| T1 Cambio ≠ Transformación | ¿Cambio o Transformación? (la pregunta que casi nadie se hace a tiempo) | Cómo saber si tu organización busca un cambio o una transformación (antes de invertir) | Pidió un tablero, encontró una transformación (efecto cebolla) | Por qué elegimos trabajar con quien se siente incómodo |
| T2 Cultura = sistema operativo | La brecha Copilot: quedarse en la herramienta | Implementar ≠ adoptar IA · el Laboratorio de IA | Adopción real de IA + evidencia | Organizaciones más conscientes · los Heladeros de Disney |
| T3 Transformación Continua® | Obituarios de los modelos de gestión tradicionales | Los 6 principios de Transformación Continua® | Los 3 rieles del Programa (proyectos en marcha) | No se gestiona el cambio: se diseña la organización para vivir en cambio |
| T4 Tecnología commodity | La trampa del enlatado | Service as a Software | El ROI de orquestar a medida (caso) | Orquestadores: el perfil profesional emergente |

# MESES (estado del ciclo — la espiral: al cerrar un mes, el siguiente reusa la matriz con
# munición/evidencia/analogías NUEVAS; los temas se renuevan cuando Paulo lo decida):

| Mes | Primer lunes | Estado | Notas |
|-----|-------------|--------|-------|
| (pendiente de definir) | | pendiente | Primer mes del esquema nuevo |

# REGLA PARA LA CASCADA MENSUAL:
# 1. Paulo indica el MES (YYYY-MM) y la fecha del PRIMER LUNES.
# 2. Los temas salen de la matriz de arriba. NO inventar temas; afinar el título sí, cambiar el tema no.
# 3. Leer banco/reels/catalogo.json y asignar 2 videos por semana (tesis+tipo con stock "disponible").
#    Reservarlos: estado → "reservado", campo "reservado_para" = fecha del día.
# 4. Generar UN manifiesto mensual: manifiestos/mes_<YYYY-MM>.json (estructura en scripts/PROMPT_mes.md)
#    + slides de todos los carruseles + newsletters .md (4, uno por semana) — todo en la misma corrida.
# 5. Paleta del carrusel por tipo: problema=negro · metodo=violeta · resultados=naranja · conexion=aqua.
# 6. Tras generar, registrar el mes en la tabla MESES con estado "generado".
#
# NOTA HISTÓRICA: T1 ya tuvo una pasada completa en el formato semanal viejo (ep1-1 y ep1-2,
# publicados). Si el primer mes del esquema nuevo arranca por T1, renovar ángulos/evidencia
# para no repetir las piezas ya publicadas.
# LEGACY: el modelo semanal anterior (8 semanas, manifiesto_<fecha>.json) queda congelado.
# Sus workflows (1-cascada-semanal, 2-motor-completo) siguen en el repo hasta validar el mensual.
