# Pipeline de reels

## Flujo operativo

### 1. Generar o reutilizar transcripción y crear guion

Workflow: `3-reels-guion`

- `modo_ejecucion=auto`: reutiliza `transcript.json/md` si ya existen; si no, descarga y transcribe.
- `transcribir_y_generar`: fuerza una transcripción nueva.
- `solo_generar`: ejecuta únicamente el editor sobre una transcripción existente.
- `brief_adicional`: define foco y restricciones de una sesión sin alterar las reglas canónicas.

El workflow falla si Claude no crea un manifiesto válido. No se acepta un run verde con solo la transcripción.

### 2. Previsualizar layout sin render completo

Workflow: `4a-reels-layout-preview`

Analiza varios frames por reel y genera imágenes 1080×1920 en un artifact. No publica ni modifica el repositorio.

### 3. Renderizar

Workflow: `4-reels-render`

Modos:

- `auto_per_reel`: detecta por reel pantalla + cámara pequeña o solo orador.
- `zones_single_file`: mismo motor para un único video compuesto.
- `camera_only`: imagen institucional arriba, video abajo.
- `split_two_files`: exige una segunda grabación de pantalla.
- `keep_manifest`: conserva modos y coordenadas manuales existentes.

Cuando el video tiene una cámara pequeña superpuesta, `resolver_layout.py` detecta rostros y genera coordenadas por reel. Cuando no detecta un recuadro estable de cámara, usa `poster` para evitar crops incorrectos.

## Imagen superior

El valor por defecto es:

`design-system/assets/innpulso-fondo.png`

Puede cambiarse desde el input `poster_asset` sin tocar código.

## Validaciones

`validar_manifiesto.py` comprueba:

- existencia y validez del JSON;
- reels no vacíos;
- tesis, tipo, modo, título y caption;
- timestamps contra palabras reales del transcript;
- duración de 20 a 62 segundos;
- coordenadas válidas para `zonas`;
- resolución completa del modo antes de render.

## Concurrencia

El guion integra resultados con `fetch + rebase + push` y reintentos. Corridas de sesiones diferentes pueden transcribir y editar en paralelo sin pisar commits de otras sesiones.
