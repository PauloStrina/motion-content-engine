# CONTRATO DEL MANIFIESTO MENSUAL

## Archivo

```text
manifiestos/mes_<YYYY-MM>.json
```

El manifiesto es el input operativo aprobado. La unidad estratégica sigue siendo el mes, pero el archivo puede completarse, aprobarse y ejecutarse semana por semana.

## Estructura raíz

```json
{
  "mes": "2026-08",
  "primer_lunes": "2026-08-03",
  "estado": "borrador_para_aprobacion",
  "aprobado_por": null,
  "aprobado_en": null,
  "contrato_visual_version": 1,
  "contrato_storytelling_version": 1,
  "semanas": []
}
```

La aprobación raíz gobierna una ejecución del ciclo completo. Mientras el mes se construye progresivamente puede permanecer en `borrador_para_aprobacion`.

`contrato_visual_version` es opcional para compatibilidad. Cuando vale `1`, el sistema exige un contrato visual aprobado en cada pieza no-video del alcance.

`contrato_storytelling_version` es opcional para compatibilidad. Cuando vale `1`, cada día debe declarar el contrato narrativo que gobierna la redacción y la adaptación.

## Estructura de semana

```json
{
  "numero": 1,
  "fecha_inicio": "2026-08-03",
  "estado": "aprobado",
  "aprobado_por": "Paulo",
  "aprobado_en": "2026-07-30T18:00:00-03:00",
  "dias": {}
}
```

La aprobación semanal habilita `dry` y `live` únicamente para esa semana. Las demás semanas pueden no existir todavía o permanecer en borrador.

## Reglas editoriales vigentes

- El ciclo completo contiene exactamente 4 semanas.
- Una operación semanal puede ejecutarse con un manifiesto progresivo que contenga entre 1 y 4 semanas.
- Cada semana declara un `numero` único entre 1 y 4 y una `fecha_inicio` consistente con `primer_lunes`.
- Cada semana contiene `lun`, `mar`, `mie` y `jue`.
- El orden de tipos es problema, método, resultados y conexión.
- Cada publicación debe funcionar de forma autónoma; la semana no se redacta como una historia serial obligatoria.
- Cada semana suma exactamente 2 piezas `video` o `faltante_video` cuando se utiliza el contrato técnico mensual completo.
- Cada día incluye `texto_linkedin` y `caption_instagram` cuando el formato y el flujo de publicación los requieren.
- Los carruseles incluyen `carrusel`, `carrusel_slides` y `slides`.
- `slides` contiene el copy final. Diseño y render no pueden modificarlo.
- `carousel_news` incluye la ruta del newsletter aprobado.
- `copy_locked: true` bloquea reescritura, reordenamiento argumental y agregados conceptuales.
- `live` semanal exige aprobación de la semana seleccionada.
- `live` de `todas` exige las 4 semanas y aprobación completa en la raíz.

## Contrato narrativo por día

Cuando `contrato_storytelling_version` vale `1`, cada día incluye:

```json
"narrativa": {
  "efecto_editorial": "reconocimiento",
  "centro_narrativo": "tensión de autoridad transversal",
  "punto_de_llegada": "la legitimidad puede construirse produciendo evidencia",
  "source_mode": "situacion_potencial",
  "source_refs": [],
  "evidence_id": null,
  "copy_locked": false,
  "copy_source": null
}
```

### Campos

- `efecto_editorial`: cambio que la pieza debe producir en el lector.
- `centro_narrativo`: elemento que recibe el mayor peso.
- `punto_de_llegada`: límite conceptual donde debe terminar la pieza.
- `source_mode`: naturaleza de la fuente narrativa.
- `source_refs`: rutas o IDs de situaciones, conceptos, artefactos, corpus o referencias autorizadas.
- `evidence_id`: ID de evidencia cuando la pieza utiliza un caso o resultado.
- `copy_locked`: indica si el texto ya fue aprobado y no puede reescribirse.
- `copy_source`: ruta a la fuente aprobada cuando `copy_locked` es `true`.

### Valores permitidos para `source_mode`

- `situacion_potencial`;
- `caso_real`;
- `caso_real_anonimizado`;
- `concepto`;
- `artefacto`;
- `experiencia_personal`;
- `referencia_externa`.

### Controles por tipo

#### Problema

- el efecto editorial principal es reconocimiento o nueva comprensión;
- el centro narrativo es una tensión, contradicción o punto ciego;
- el punto de llegada no debe incluir el método completo.

#### Método

- el efecto editorial principal es comprensión del mecanismo;
- el centro narrativo es una decisión, secuencia, artefacto o dinámica concreta;
- el problema inicial funciona como contexto y no debe dominar la pieza.

#### Resultados

- requiere `source_mode` real y evidencia autorizada cuando se presentan hechos, resultados o aprendizajes de un caso;
- debe diferenciar hecho, intervención, resultado e interpretación;
- no puede completar vacíos narrativos con información inventada.

#### Conexión

- el efecto editorial principal es afinidad con la perspectiva de Motion;
- debe anclarse en una experiencia, decisión, símbolo, método o referencia concreta;
- no necesita desarrollar toda la oferta.

## Regla de copy bloqueado

Cuando `copy_locked` es `true`:

- `copy_source` es obligatorio;
- `slides`, `texto_linkedin`, `caption_instagram` y newsletter deben trazarse a la fuente aprobada;
- se permite segmentar, jerarquizar, adaptar densidad y crear CTA por canal;
- no se permite regenerar desde un resumen, cambiar la persona narrativa, alterar el orden argumental ni agregar conceptos no aprobados;
- un error tipográfico se conserva hasta recibir autorización explícita para corregirlo.

## Contrato visual por día

Cuando `contrato_visual_version` vale `1`, cada formato no-video incluye:

```json
"visual": {
  "estado": "aprobado",
  "aprobado_por": "Paulo",
  "aprobado_en": "2026-07-30T18:00:00-03:00",
  "concept_path": "design-system/concepts/2026-08/2026-08-05-linkedin/concept.json",
  "execution": "code"
}
```

Valores permitidos para `execution`:

- `code`
- `openai`
- `hybrid`
- `reuse`

El bloque visual no contiene el concepto completo. Solo registra aprobación, modo de ejecución y ruta al contrato.

El contrato visual no puede modificar el contrato narrativo ni el copy bloqueado.

## Formatos permitidos

- `video`.
- `carousel_news`.
- `post_carousel`.
- `faltante_video` con fallback de carrusel.

Los manifiestos progresivos o de revisión pueden utilizar nombres de formato adicionales mientras no ingresen al workflow mensual legacy. Deben documentar explícitamente si la publicación es manual o no está gobernada por el motor.

## Ejemplo de día con carrusel

```json
{
  "tipo": "metodo",
  "tema": "Adopción de IA como transformación del trabajo",
  "lente_buyer": "innovacion",
  "objetivo": "mostrar el método",
  "formato": "carousel_news",
  "narrativa": {
    "efecto_editorial": "comprension_del_mecanismo",
    "centro_narrativo": "elegir una práctica, observarla, rediseñarla, acompañarla y medirla",
    "punto_de_llegada": "la adopción ocurre cuando cambia la forma de operar",
    "source_mode": "situacion_potencial",
    "source_refs": [
      "knowledge/guides/GUIA_OPERATIVA_STORYTELLING.md"
    ],
    "evidence_id": null,
    "copy_locked": true,
    "copy_source": "editorial/2026-08/semana-1/martes-metodo.md"
  },
  "carrusel": "2026-08-04-mar",
  "carrusel_slides": 13,
  "slides": [
    {"lineas": ["Copy aprobado de la portada"]},
    {"lineas": ["Copy aprobado de la placa 2"]}
  ],
  "texto_linkedin": "Texto final aprobado.",
  "caption_instagram": "Caption final aprobado.",
  "newsletter": "newsletters/newsletter_2026-08-04.md",
  "visual": {
    "estado": "aprobado",
    "aprobado_por": "Paulo",
    "aprobado_en": "2026-07-30T18:00:00-03:00",
    "concept_path": "design-system/concepts/2026-08/2026-08-04-mar/concept.json",
    "execution": "hybrid"
  }
}
```

## Gate previo a producción

Antes de preparar assets o ejecutar un dry run, verificar:

1. tesis, tipo y audiencia correctos;
2. efecto editorial, centro narrativo y punto de llegada definidos;
3. fuentes y evidencia autorizadas;
4. copy aprobado y ruta correcta;
5. ausencia de reescrituras posteriores al bloqueo;
6. coherencia entre copy, visual y CTA;
7. autonomía de cada publicación.
