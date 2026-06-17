# Kit visual MOTION — reglas fijas (el Agente Diseñador NO improvisa fuera de esto)
1. **Eco vertical** (3 repeticiones, opacidad 1/.45/.16): palabra héroe que va sola (DOLOR, EL CÓMO).
2. **Degradé laminado 10px MONOCOLOR** (`type:"lam"`): resaltado de palabras/remates. La sombra la elige render.py automáticamente: oscura (violeta) sobre fondos claros, clara (aqua) sobre fondos oscuros. JAMÁS más de un color de sombra.
3. **Contraste serif** (Lyon para analogías y voz editorial, Futura para sentencias).
4. Narrativa cromática: la portada lleva el color del tipo Rubilar del episodio (problema=negro, método=violeta, resultados=naranja, conexión=aqua). El interior puede girar de fondo cuando el argumento gira.
5. Formato de spec: ver slides/ejemplo_ep1-1.json — el Diseñador escribe un JSON igual y ejecuta render.py.

## Plantillas estáticas (render_static.py — formato 1080x1080 feed)
- **quote**: cita institucional. Campos: bg, quote.
- **data**: número/estadística destacada con sombra laminada. Campos: bg, eyebrow, number, label. (El número se ancla SIEMPRE al Banco de Evidencias.)
- **list**: lista numerada (pasos, principios). Campos: bg, title, items[].
Spec de ejemplo: slides/piezas_demo.json. Mismo kit visual y reglas de color que el carrusel.
