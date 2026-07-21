# VALIDACIÓN DE VERSIONES DE DISEÑO

## 1. Objetivo

Separar concepto, versión visual y publicación.

La validación de versiones no existe para obligar a elegir entre alternativas. Existe para comprobar que al menos una alternativa representa correctamente la gramática visual aprobada.

La generación de un archivo técnicamente correcto no habilita su uso.

## 2. Cuándo se aplica

Es obligatoria para:

- imágenes conceptuales nuevas;
- carruseles con una nueva dirección visual;
- piezas que introducen un concepto o diagrama nuevo;
- cambios relevantes sobre un formato existente;
- cualquier pieza sobre la que Paulo pida comparar alternativas.

Los reels ya aprobados y los formatos reutilizados sin cambios sustanciales no necesitan múltiples versiones.

## 3. Paquete de revisión

Cada revisión vive en:

```text
design-system/reviews/<ciclo>/review.json
design-system/reviews/<ciclo>/specs/*.json
```

`review.json` registra:

- las piezas revisadas;
- la familia visual de cada una;
- dos o más versiones;
- el fundamento de cada alternativa;
- la versión seleccionada;
- el estado de la revisión;
- una posible invalidación total por desvío respecto de las referencias.

## 4. Estados

- `awaiting_selection`: versiones generadas, todavía sin elección.
- `selected`: Paulo eligió una versión; todavía puede requerir ajustes.
- `approved`: preview final aprobado y habilitado para convertirse en contrato visual.
- `rejected`: versiones descartadas por decisión de contenido o preferencia.
- `invalidated_reference_mismatch`: todas las versiones comparten una gramática visual incorrecta o insuficiente respecto de las referencias.

Mientras la revisión no esté `approved`, la publicación permanece bloqueada.

## 5. Flujo

```text
copy aprobado
→ referencia visual concreta
→ hipótesis visuales realmente diferentes
→ CI renderiza previews
→ comparación explícita con la referencia
→ selección o invalidación total
→ ajustes sobre la versión elegida
→ preview final
→ aprobación visual
→ contrato visual approved
→ assets finales
→ dry run
→ live
```

## 6. Regla de invalidación total

Cuando todas las versiones:

- comparten la misma gramática incorrecta;
- se alejan de las referencias;
- parecen variaciones de layout en lugar de conceptos distintos;
- cumplen técnicamente, pero no alcanzan calidad conceptual;

la revisión completa debe pasar a `invalidated_reference_mismatch`.

No se elige la menos mala.

## 7. Revisión de `line_system`

Antes de presentar previews, verificar:

- que la pieza sea una ilustración conceptual y no una infografía corporativa;
- que la línea sea el concepto, no una decoración;
- que exista una sola relación visual dominante;
- que el trazo conserve organicidad controlada;
- que haya pocos nodos y un único color de acento;
- que el texto dentro del asset sea mínimo;
- que no existan simultáneamente título, subtítulo, múltiples etiquetas, pager, footer, leyenda y callouts;
- que el resultado se parezca en gramática a las referencias Matt Gray / Henso adaptadas a Motion;
- que sea meticuloso, reconocible, divertido, compartible, scroll-stopping y con una segunda lectura.

La especificación completa vive en `design-system/references/line-system/README.md`.

## 8. Revisión de otros estilos

Cada estilo debe contar con referencias concretas y una gramática operativa propia antes de generar versiones.

No alcanza con usar etiquetas como `journaling`, `editorial` o `conceptual_art`. Deben definirse:

- composición;
- densidad de texto;
- materialidad;
- tratamiento tipográfico;
- recursos permitidos;
- recursos prohibidos;
- indicadores observables de similitud con las referencias.

## 9. Reglas generales

- Las versiones comparan soluciones reales, no simples cambios de color.
- Todas las versiones de una pieza respetan la familia visual seleccionada.
- Una versión puede contener pocas placas representativas durante la exploración.
- La versión elegida se desarrolla luego hasta completar todos los assets.
- Las versiones descartadas permanecen como histórico de decisión, pero no se copian a las rutas de publicación.
- Ninguna selección se registra en nombre de Paulo sin su confirmación explícita.
- El workflow de revisión no publica ni modifica copies.
- Un workflow exitoso no equivale a un diseño aprobado.

## 10. Gate de publicación

La publicación permanece bloqueada cuando:

- `selected_version` es nulo;
- el paquete está `awaiting_selection`;
- el paquete está `invalidated_reference_mismatch`;
- falta aprobación explícita de Paulo;
- el preview aprobado no coincide con el asset final.

## 11. Automatización

`design-review-ci.yml` valida el paquete, renderiza todas las versiones y publica un artifact llamado `design-review-previews`.

El validador `scripts/validar_revision_diseno.py` comprueba:

- existencia de dos o más candidatos;
- IDs y versiones únicas;
- existencia y validez de los specs;
- coherencia de la versión seleccionada;
- selección obligatoria antes de marcar la revisión como aprobada;
- bloqueo explícito cuando la revisión fue invalidada por referencias.
