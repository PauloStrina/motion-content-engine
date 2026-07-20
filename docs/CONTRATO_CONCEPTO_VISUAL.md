# CONTRATO DE CONCEPTO VISUAL

## 1. Función

El contrato visual traduce una idea aprobada a una especificación ejecutable.

No define el copy ni la estructura narrativa. Tampoco permite que GitHub invente la conceptualización. Registra una decisión visual ya validada y la vuelve trazable hasta el asset final.

Ruta:

```text
design-system/concepts/<YYYY-MM>/<piece_id>/concept.json
```

## 2. Versión vigente

Los contratos nuevos utilizan `schema_version: 2`.

La versión 2 obliga a seleccionar una de las dos familias visuales de Motion y bloquea su mezcla dentro de una pieza o carrusel.

## 3. Estructura mínima v2

```json
{
  "schema_version": 2,
  "piece_id": "2026-08-05-linkedin",
  "status": "draft",
  "approved_by": null,
  "approved_at": null,
  "visual_message": "La decisión tecnológica está definida antes que el proceso.",
  "concept": "Un bloque rígido representa la compra anticipada; el proceso todavía aparece incompleto.",
  "conceptual_rationale": "La idea depende de una relación entre una decisión cerrada y un sistema todavía abierto.",
  "visual_family": "line_system",
  "family_lock": true,
  "representation": "single_concept",
  "execution": "code",
  "visual_resources": [
    "topology",
    "absence",
    "scale"
  ],
  "exclusions": [
    "shadows",
    "3d_ribbons",
    "volumetric_objects"
  ],
  "quality_target": "reference_grade",
  "quality_checks": {
    "single_family": true,
    "single_dominant_idea": true,
    "mobile_legibility": true,
    "reference_consistency": true
  },
  "brand_resources": [
    "motion_palette",
    "motion_typography",
    "motion_logo"
  ],
  "references": [
    "design-system/references/line-system/README.md"
  ],
  "approved_preview": null,
  "generation": null
}
```

## 4. Estados

- `draft`: hipótesis todavía no validada.
- `approved`: concepto y preview aprobados; habilitado para ejecución.
- `generated`: recurso generado; aún requiere composición o revisión.
- `final`: asset final validado.

Un contrato no puede pasar a `approved` sin un preview revisado por Paulo.

## 5. Familias visuales

Valores válidos:

- `line_system`;
- `conceptual_art`.

La definición completa vive en:

```text
design-system/visual-language/FAMILIAS_VISUALES.md
design-system/visual-language/FAMILIAS_VISUALES.json
```

### Regla de exclusividad

- `family_lock` debe ser `true`.
- `visual_resources` debe pertenecer a la familia seleccionada.
- `references` debe apuntar al directorio de esa misma familia.
- todas las placas de un carrusel usan la misma familia.
- tipografía, paleta y logotipo son capas comunes, no familias visuales.

## 6. Representaciones válidas

- `single_concept`;
- `concept_map`;
- `diagram`;
- `typographic`;
- `photo_intervention`;
- `hybrid`;
- `motion`.

La representación describe la solución dominante. No autoriza a mezclar familias.

## 7. Modos de ejecución

### `code`

Geometría, diagramas, tipografía, datos y composición exacta. Es el modo principal de `line_system`.

### `openai`

Generación o edición de un recurso visual. Es válido para `conceptual_art`; el texto, el logo y la composición final se agregan después.

### `hybrid`

Recurso generado más composición determinística.

### `reuse`

Uso directo de una imagen aprobada.

Los modos permitidos para cada familia se definen en `FAMILIAS_VISUALES.json`.

## 8. Calidad conceptual

Cada contrato v2 debe incluir:

- `conceptual_rationale`: por qué la familia expresa la idea;
- `visual_resources`: recursos utilizados;
- `exclusions`: recursos que se excluyen para evitar contaminación;
- `quality_target: reference_grade`;
- controles explícitos de familia única, idea dominante, legibilidad y coherencia con referencias.

Un render correcto no equivale a una visual aprobada.

## 9. Fidelidad

Si existe `approved_preview` y el resultado debe ser idéntico, se utiliza el archivo. No se vuelve a generar desde el prompt.

Si se necesita una adaptación, la imagen aprobada se utiliza como referencia de edición con alta fidelidad.

## 10. Referencias

Las referencias:

- inspiran;
- orientan composición, densidad, materialidad y calidad;
- pertenecen a una sola familia;
- no se copian;
- no se publican;
- no se usan como asset final sin licencia.

## 11. Relación con el manifiesto

El día del manifiesto apunta al contrato:

```json
"visual": {
  "estado": "aprobado",
  "aprobado_por": "Paulo",
  "aprobado_en": "2026-07-30T18:00:00-03:00",
  "concept_path": "design-system/concepts/2026-08/2026-08-05-linkedin/concept.json",
  "execution": "code"
}
```

El manifiesto no duplica el concepto completo.

## 12. Migración

Los manifiestos históricos sin `contrato_visual_version` siguen funcionando.

- `contrato_visual_version: 1` admite contratos v1 legacy.
- `contrato_visual_version: 2` exige contratos v2 y la selección de una familia visual.
