# AGENTE DISEÑADOR — genera el carrusel a partir del MANIFIESTO

## ⭐ EXEMPLAR DE ORO (leer y replicar el NIVEL antes de diseñar)
ANTES de generar nada, abrí y estudiá `design-system/slides/EJEMPLO_HEM_carrusel.json`.
Es un carrusel HEM aprobado por Paulo. Tu salida debe alcanzar ESE nivel de riqueza:
- **8 slides** (no menos), con **arco cromático** que gira con el argumento (ej. negro → aqua → violeta → naranja → negro), NO todo en un solo fondo.
- **Mezcla de tratamientos**, no todo `futura`: combiná `futura` (golpes), `lam` (palabra resaltada), `eco` (palabra héroe repetida 3×), `lyon`/`lyont` (momentos editoriales y frases largas). Cada slide usa 2-3 bloques con jerarquía.
- **Una slide de analogía cultural** (tipo auto/tráfico) en Lyon, fondo de color.
- **Cierre** = la pregunta/frase sola en futura + `foot` ("Lo único permanente es el movimiento").
Si tu borrador tiene casi todo `futura`, un solo color de fondo, o menos de 8 slides → está POBRE: rehacelo imitando la variedad y el ritmo del exemplar. El exemplar manda sobre tu intuición.

1. Leé el manifiesto semanal (manifiestos/manifiesto_<fecha>.json) y README-kit.md. Vos hacés el carrusel HEM (el carrusel newsletter lo hace otro agente).
2. Tomá canales.instagram.carrusel (nombre, = `<fecha>`) y carrusel_slides (cantidad). El archivo de slides va en design-system/slides/<fecha>_carrusel.json.
3. ## PLANTILLA ESTRUCTURAL POR TIPO (no solo color)
Leé `carousel.tipo` del manifiesto (problema o resultados). Define color (problema=negro · resultados=naranja) Y arquitectura de slides:

- problema  → DOMINANTE: eco vertical. Portada eco/negro (palabra-eje). Interior: contraste binario dolor↔visión. Cierre: la pregunta sola, Futura grande, SIN respuesta. Prohibido número/método.
- metodo    → DOMINANTE: degradé laminado sobre verbo de acción + esqueleto de lista numerada. Portada violeta (nombre del método). Interior: pasos 1→2→3 (movimiento visible). Cierre: principio condensado.
- resultados→ DOMINANTE: plantilla dato (número héroe + sombra laminada). Portada naranja (framing del caso, sin nombre salvo OK). Interior: antes→después, UNA métrica por slide. Cierre: transformación en una frase. Usá el dato/caso que aporte; Paulo revisa antes de publicar.
- conexion  → DOMINANTE: contraste serif Lyon. Portada aqua (la creencia). Interior: editorial Lyon Text + analogía cultural. Cierre: creencia anclada en algo concreto. Menos display.

Regla: el tratamiento dominante manda la composición; los otros 2 tratamientos solo como apoyo puntual. NO inventar tratamientos nuevos.
4. Generá slides/<carrusel>_carrusel.json con el kit (lam monocolor, eco, lyon, narrativa cromática por tipo).
   El nombre del archivo DEBE coincidir con canales.instagram.carrusel.
   NOTA RENDER: El eyebrow está vacío (render.py no muestra texto arriba a la izquierda). En la portada (slide 1) render.py agrega automáticamente "#HistoriasEnMovimiento: casos reales de nuestro día a día." en el foot — no lo pongas vos. Sí ponés `eyebrow_color` en cada slide (define el color del pager y otros elementos según la paleta).
   ÚLTIMO SLIDE: siempre usar `"foot": "Lo único permanente es el movimiento", "foot_color": "naranja"` (reemplaza #LoComplejoSimple).
5. El número de slides DEBE coincidir con carrusel_slides (si difiere, actualizá el manifiesto).
El render posterior produce <carrusel>-1.png ... <carrusel>-N.png que el Publicador sube a Blotato.
