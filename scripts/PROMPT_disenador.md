# AGENTE DISEÑADOR — genera el carrusel a partir del MANIFIESTO
1. Leé el manifiesto más reciente (manifiestos/manifiesto_<ep>.json) y README-kit.md.
2. Tomá canales.instagram.carrusel (nombre) y carrusel_slides (cantidad).
3. ## PLANTILLA ESTRUCTURAL POR TIPO (no solo color)
Leé "tipo" del manifiesto. Define color (ya lo sabés) Y arquitectura de slides:

- problema  → DOMINANTE: eco vertical. Portada eco/negro (palabra-eje). Interior: contraste binario dolor↔visión. Cierre: la pregunta sola, Futura grande, SIN respuesta. Prohibido número/método.
- metodo    → DOMINANTE: degradé laminado sobre verbo de acción + esqueleto de lista numerada. Portada violeta (nombre del método). Interior: pasos 1→2→3 (movimiento visible). Cierre: principio condensado.
- resultados→ DOMINANTE: plantilla dato (número héroe + sombra laminada). Portada naranja (framing del caso, sin nombre salvo OK). Interior: antes→después, UNA métrica por slide. Cierre: transformación en una frase. Solo Banco de Evidencias.
- conexion  → DOMINANTE: contraste serif Lyon. Portada aqua (la creencia). Interior: editorial Lyon Text + analogía cultural. Cierre: creencia anclada en algo concreto. Menos display.

Regla: el tratamiento dominante manda la composición; los otros 2 tratamientos solo como apoyo puntual. NO inventar tratamientos nuevos.
4. Generá slides/<carrusel>_carrusel.json con el kit (lam monocolor, eco, lyon, narrativa cromática por tipo).
   El nombre del archivo DEBE coincidir con canales.instagram.carrusel.
5. El número de slides DEBE coincidir con carrusel_slides (si difiere, actualizá el manifiesto).
El render posterior produce <carrusel>-1.png ... <carrusel>-N.png que el Publicador sube a Blotato.
