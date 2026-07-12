# PREPARACIÓN DE ASSETS DEL MES

## Alcance

Tu única responsabilidad es convertir el copy ya aprobado del manifiesto mensual en especificaciones visuales para el sistema de diseño.

No redactes, no resumas, no corrijas, no completes y no cambies ninguna palabra del manifiesto.

## Inputs

1. `manifiestos/mes_<YYYY-MM>.json`.
2. `design-system/slides/EJEMPLO_HEM_carrusel.json`.
3. documentación y código del `design-system/`.

No leas `archive/**`. No uses archivos estratégicos para inventar contenido. No modifiques el subsistema de video.

## Output

Por cada día cuyo `formato` sea:

- `carousel_news`;
- `post_carousel`;
- `faltante_video`;

creá:

```text
design-system/slides/<valor de carrusel>.json
```

## Contrato de copy

- La cantidad de slides debe coincidir con `carrusel_slides`.
- Cada slide del diseño debe tener exactamente tantos bloques de texto como elementos haya en `slides[n].lineas`.
- Los bloques de texto válidos son `futura`, `lam`, `eco`, `lyon` y `lyont`.
- Podés agregar bloques no textuales, como `spacer` o elementos gráficos.
- El campo `text` debe contener temporalmente la misma línea del manifiesto. El render vuelve a inyectar y verificar el copy.
- No unas dos líneas en un solo bloque.
- No dividas una línea en varios bloques.
- No agregues frases, CTA, hashtags, firmas ni aclaraciones.

## Sistema visual

Usá exclusivamente los tratamientos y tokens existentes. No inventes componentes nuevos.

Orientación dominante por tipo:

- `problema`: contraste y tensión; portada predominantemente negra.
- `metodo`: progresión y estructura; portada predominantemente violeta.
- `resultados`: evidencia y transformación; portada predominantemente naranja.
- `conexion`: registro editorial y humano; portada predominantemente aqua.

La paleta puede evolucionar dentro del carrusel cuando el argumento lo requiera. Replicá el nivel de riqueza del exemplar sin copiar su contenido.

## Reglas

- Una idea visual por slide.
- Jerarquía clara y legibilidad en 1080 × 1350.
- `pager` consistente con la cantidad real.
- Última slide con `foot` de marca cuando el template lo requiera.
- No modificar el manifiesto.
- No modificar estrategia, conocimiento, newsletters, workflows ni scripts.

## Autocontrol

Antes de terminar:

1. Confirmá que existe un JSON por cada carrusel del manifiesto.
2. Confirmá que la cantidad de slides coincide.
3. Confirmá que cada slide tiene la misma cantidad de bloques de texto que líneas de copy.
4. Confirmá que el copy es idéntico carácter por carácter.
5. Ejecutá:

```bash
python scripts/validar_assets_mes.py --mes <YYYY-MM>
```

El trabajo no está terminado si la validación falla.
