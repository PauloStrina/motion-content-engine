# CONTRATO DE CONCEPTO VISUAL

## 1. Función

El contrato visual traduce una idea aprobada a una especificación ejecutable.

No define el copy ni la estructura narrativa. Tampoco permite que GitHub invente la conceptualización. Registra una decisión visual ya validada y la vuelve trazable hasta el asset final.

Ruta:

```text
design-system/concepts/<YYYY-MM>/<piece_id>/concept.json
```

## 2. Estructura mínima

```json
{
  "schema_version": 1,
  "piece_id": "2026-08-05-linkedin",
  "status": "approved",
  "approved_by": "Paulo",
  "approved_at": "2026-07-30T18:00:00-03:00",
  "visual_message": "La herramienta funciona, pero el sistema que la alimenta está desordenado.",
  "concept": "Una línea perfectamente procesada atraviesa una conversación caótica.",
  "representation": "single_concept",
  "execution": "hybrid",
  "brand_resources": [
    "black_background",
    "aqua_system_line",
    "orange_friction"
  ],
  "references": [
    "design-system/references/concepto-2/README.md"
  ],
  "approved_preview": null,
  "generation": {
    "model": "gpt-image-2-2026-04-21",
    "prompt": "Recurso visual sin texto final...",
    "size": "1024x1536",
    "quality": "high",
    "background": "opaque",
    "output_format": "png",
    "reference_image": null,
    "input_fidelity": "high",
    "output": "design-system/generated/2026-08-05-linkedin/base.png"
  }
}
```

## 3. Estados

- `draft`: hipótesis todavía no validada.
- `approved`: concepto aprobado y habilitado para ejecución.
- `generated`: recurso generado; aún requiere composición o revisión.
- `final`: asset final validado.

La generación automática exige `status: approved`, `generated` o `final`.

## 4. Representaciones válidas

- `single_concept`
- `concept_map`
- `diagram`
- `typographic`
- `photo_intervention`
- `hybrid`
- `motion`

La lista describe la solución dominante. No obliga una estructura narrativa.

## 5. Modos de ejecución

### `code`

Geometría, diagramas, tipografía, datos y composición exacta.

### `openai`

Generación o edición de un recurso visual.

### `hybrid`

Recurso generado más composición determinística.

### `reuse`

Uso directo de una imagen aprobada.

## 6. Fidelidad

Si existe `approved_preview` y el resultado debe ser idéntico, se utiliza el archivo. No se vuelve a generar desde el prompt.

Si se necesita una adaptación, la imagen aprobada se utiliza como referencia de edición con alta fidelidad.

## 7. Referencias

Las referencias:

- inspiran;
- orientan composición, densidad o lenguaje;
- no se copian;
- no se publican;
- no se usan como asset final sin licencia.

## 8. Relación con el manifiesto

El día del manifiesto apunta al contrato:

```json
"visual": {
  "estado": "aprobado",
  "aprobado_por": "Paulo",
  "aprobado_en": "2026-07-30T18:00:00-03:00",
  "concept_path": "design-system/concepts/2026-08/2026-08-05-linkedin/concept.json",
  "execution": "hybrid"
}
```

El manifiesto no duplica el concepto completo.

## 9. Regla de migración

Los manifiestos históricos siguen funcionando.

Cuando la raíz declara:

```json
"contrato_visual_version": 1
```

cada pieza no-video del alcance debe incluir un bloque `visual` válido y apuntar a un contrato aprobado.
