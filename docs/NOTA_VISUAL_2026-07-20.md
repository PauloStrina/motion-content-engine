# Corrección visual — publicación del 20 de julio de 2026

Las primeras imágenes generadas para la publicación del 20 de julio se consideran inválidas y no publicables.

## Problema detectado

El sistema visual contenía recursos de dos familias distintas, pero no obligaba a elegir una de ellas. Como consecuencia, una misma pieza podía combinar líneas, nodos, módulos, sombras, formas volumétricas y recursos artísticos sin una jerarquía clara.

También faltaba una separación entre:

- conceptualización visual;
- selección de familia;
- ejecución técnica;
- control de calidad conceptual;
- aprobación final.

## Aprendizaje

Motion trabaja con dos familias visuales principales:

1. `line_system`: diagramas bidimensionales de líneas, nodos, trayectorias, ejes y relaciones.
2. `conceptual_art`: metáforas visuales esquemáticas o artísticas con profundidad, volumen, sombra, pliegues, materia o imagen conceptual.

Una pieza debe elegir una sola familia. No puede mezclarlas dentro del mismo asset ni dentro de un mismo carrusel.

La tipografía, la paleta y el logotipo son capas de identidad comunes a ambas familias; no constituyen una tercera familia.

## Corrección requerida

- incorporar una taxonomía formal de familias visuales;
- exigir `visual_family` en cada contrato nuevo;
- limitar recursos permitidos por familia;
- validar contaminación entre familias;
- usar referencias pertenecientes a una sola familia;
- aprobar primero el concepto y después la ejecución;
- evaluar la calidad conceptual, no solo que el archivo renderice.

Las visuales del 20 de julio deberán rehacerse después de incorporar esta arquitectura.
