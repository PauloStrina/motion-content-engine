# VALIDACIÓN DE VERSIONES DE DISEÑO

## 1. Objetivo

Separar la exploración visual de la aprobación y de la publicación.

La generación de un archivo técnicamente correcto no habilita su uso. Antes de producir assets finales, Motion compara versiones visibles, selecciona una dirección y registra esa decisión.

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
- el estado de la revisión.

## 4. Estados

- `awaiting_selection`: versiones generadas, todavía sin elección.
- `selected`: Paulo eligió una versión; todavía puede requerir ajustes.
- `approved`: preview final aprobado y habilitado para convertirse en contrato visual.
- `rejected`: todas las versiones fueron descartadas.

Mientras la revisión no esté `approved`, la publicación permanece bloqueada.

## 5. Flujo

```text
copy aprobado
→ concepto visual y familia
→ versiones de diseño
→ CI renderiza previews
→ Paulo compara y selecciona
→ ajustes sobre la versión elegida
→ preview final
→ aprobación visual
→ contrato visual approved
→ assets finales
→ dry run
→ live
```

## 6. Reglas

- Las versiones comparan soluciones reales, no simples cambios de color.
- Todas las versiones de una pieza respetan la familia visual seleccionada.
- Una versión puede contener pocas placas representativas durante la exploración.
- La versión elegida se desarrolla luego hasta completar todos los assets.
- Las versiones descartadas permanecen como histórico de decisión, pero no se copian a las rutas de publicación.
- Ninguna selección se registra en nombre de Paulo sin su confirmación explícita.
- El workflow de revisión no publica ni modifica copies.

## 7. Automatización

`design-review-ci.yml` valida el paquete, renderiza todas las versiones y publica un artifact llamado `design-review-previews`.

El validador `scripts/validar_revision_diseno.py` comprueba:

- existencia de dos o más candidatos;
- IDs y versiones únicas;
- existencia y validez de los specs;
- coherencia de la versión seleccionada;
- selección obligatoria antes de marcar la revisión como aprobada.
