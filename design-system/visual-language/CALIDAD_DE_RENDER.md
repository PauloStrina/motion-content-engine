# CALIDAD DE RENDER — REGLAS DURAS

**Estado:** vigente  
**Alcance:** todas las piezas visuales producidas por código, especialmente la familia `line_system`  
**Precedencia:** complementa `PRINCIPIOS.md` y no puede contradecir el concepto visual aprobado.

## 1. Regla central

> **Las líneas, curvas, nodos, íconos y tipografía deben producirse con calidad de publicación, no con calidad de preview.**

Un contact sheet, screenshot o preview reducido nunca puede reutilizarse como asset final.

## 2. Render obligatorio

Para piezas 1080 × 1350:

- construir la composición completa a una escala mínima de 4×;
- utilizar curvas Bézier o geometría vectorial para trayectorias;
- utilizar `linecap` y `linejoin` redondeados;
- rasterizar o reducir únicamente al final con un filtro de alta calidad;
- exportar PNG final a 1080 × 1350 con antialiasing;
- no dibujar curvas directamente a resolución final;
- no ampliar PNGs, screenshots, previews o contact sheets;
- no reutilizar líneas rasterizadas de versiones anteriores;
- regenerar cada placa desde su fuente y especificación vigentes.

Si el sistema permite SVG, PDF u otra fuente vectorial, debe conservarse también el master editable.

## 3. Control visual obligatorio

Antes de presentar una versión:

1. revisar cada pieza individual a tamaño real;
2. revisar curvas y diagonales con zoom de 200 %;
3. comprobar que no existan escalones, serruchos, bordes cortados o líneas quebradas;
4. comprobar que los nodos sean circulares y no estén deformados;
5. comprobar contraste y legibilidad de todos los rótulos;
6. comprobar que ninguna línea, nodo, ícono o texto provenga de un preview reducido;
7. comprobar que el contact sheet haya sido generado desde los assets finales, y no al revés.

Una pieza con líneas pixeladas o texto degradado no puede presentarse como candidata.

## 4. Posición vertical del contenido

En carruseles 4:5:

- conservar espacio vacío dominante en la parte superior;
- ubicar el bloque de texto principal más abajo en el eje Y, cerca del centro óptico;
- agrupar texto y visual como una única composición;
- evitar colocar el texto inmediatamente debajo de la paginación;
- comenzar el bloque principal aproximadamente desde Y = 285, ajustándolo según su altura;
- mantener el gráfico en una zona inferior separada, sin comprimirlo contra la firma;
- nunca compensar un texto demasiado alto desplazando o reduciendo el gráfico hasta perder claridad.

## 5. No solapamiento

Se mantiene como regla dura:

- texto, rótulos, líneas, nodos, gráficos, logo, firma y paginación no se solapan;
- cada elemento respeta su bounding box y margen de seguridad;
- cuando la composición no cabe, se simplifica o redistribuye el esquema;
- el espacio vacío es preferible a una composición saturada.

## 6. Regeneración completa

Cuando una versión contiene recursos rasterizados deficientes, no se corrige solamente la placa visible. Deben regenerarse todas las piezas que compartan el mismo pipeline, helper, renderer o fuente de baja calidad.

No se permite conservar silenciosamente placas anteriores dentro de un paquete nuevo si no pasaron el mismo control de calidad.

## 7. Criterio de aprobación

El asset final debe verse limpio y continuo en:

- archivo individual;
- vista móvil;
- zoom 100 %;
- zoom 200 %;
- contact sheet.

La calidad de línea y tipografía forma parte del contenido: no es un detalle cosmético ni un ajuste posterior.
