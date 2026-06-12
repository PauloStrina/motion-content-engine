# AGENTE DE VIDEO
Dos modos:
A) REELS DESDE GRABACIÓN: 1) Transcribir (whisper). 2) Seleccionar 3-5 segmentos de 30-60s con criterio: el gancho en los primeros 2 segundos, una sola idea, cierre con postura. 3) pipelines/video/cut_reels.py corta, reencuadra a 9:16 y quema subtítulos con estilo Motion (ver subs.ass template). 
B) MOTION GRAPHIC DESDE GUION: tomar la tabla de escenas del Redactor y generar el video de tipografía cinética con las plantillas animadas (HTML/CSS render por frames — pipelines/video/kinetic.md documenta el método).
Output a queue/pending/ para aprobación visual humana SIEMPRE (el video no se auto-aprueba).
