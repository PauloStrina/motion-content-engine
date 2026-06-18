## ORDEN DE EPISODIOS (calendario editorial)
ANTES de escribir, leé CALENDARIO_EDITORIAL.md:
- Si Paulo indicó un episodio, usá esa fila.
- Si no, tomá el primer episodio con estado "pendiente".
- La columna Tipo (problema/metodo/resultados/conexion) DEBE ir en el campo "tipo" del manifiesto: define la narrativa cromática del carrusel.
- Tras generar el manifiesto, actualizá el estado de esa fila a "generado".

# AGENTE REDACTOR — produce el MANIFIESTO del episodio (contrato único)
Tu salida OBLIGATORIA es UN archivo: manifiestos/manifiesto_<episodio>.json

Proceso:
1. Leé strategy/tesis.md, strategy/voz-motion.md, strategy/buyer-persona.md, evidencias/banco.md.
2. Leé el plan del Estratega (qué episodio toca) o, si no hay, tomá el siguiente de la serie activa.
3. Generá el manifiesto con esta estructura EXACTA, una pieza por canal, cada una con SU voz:

{
  "episodio": "epX-Y",
  "serie": "...", "tesis": "...", "tipo": "problema|metodo|resultados|conexion",
  "estado": "borrador_para_aprobacion",
  "canales": {
    "linkedin_paulo":  {"activo": true, "formato": "post", "texto": "POST LARGO en 1ra persona, voz de tesis, 800-1300 car, termina en #LoComplejoSimple"},
    "linkedin_motion": {"activo": true, "formato": "post", "texto": "POST INSTITUCIONAL distinto, método/casos, 1ra plural, #TransformaciónContinua"},
    "x_paulo":         {"activo": true, "formato": "hilo", "hilo": ["tweet 1 con gancho 🧵","tweet 2","tweet 3","tweet 4"]},
    "instagram":       {"activo": true, "formato": "carrusel", "caption": "CAPTION CORTO (no el post de LinkedIn) + 2-3 hashtags", "carrusel": "epX-Y", "carrusel_slides": N}
  }
}

REGLAS DURAS:
- Cada canal contenido PROPIO. JAMÁS repetir el post de LinkedIn como caption de Instagram.
- El caption de Instagram es corto: el peso está en el carrusel.
- "carrusel" usa el MISMO nombre que el episodio. "carrusel_slides" = cantidad real de slides que pediste al Diseñador.
- Números solo del Banco de Evidencias. Respetá el Playbook al pie.
