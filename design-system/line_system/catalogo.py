#!/usr/bin/env python3
"""catalogo.py — genera un thumbnail por primitiva para el README.

Uso: python catalogo.py [outdir]   (por defecto ./catalogo)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import primitivas as P  # noqa: E402
from primitivas import C, DOT  # noqa: E402

W, H = 420, 300


def _t_nodo():
    return (P.nodo(90, 150, 26, C["violeta"])
            + P.nodo(190, 150, 26, C["aqua"], "cubo")
            + P.nodo(300, 150, 26, C["naranja"]))


def _t_trayectoria():
    svg, _ = P.trayectoria(70, 230, 350, 80, [
        {"color": C["violeta"], "label": "Inicio", "side": "abajo_der"},
        {"color": C["aqua"]},
        {"color": C["naranja"], "label": "Hito", "side": "arriba"}],
        label_size=17)
    return svg


def _t_anillos():
    return P.anillos(150, 150, [46, 74, 102],
                     [C["aqua"], C["violeta"], C["naranja"]],
                     leyenda=[("Datos", C["aqua"]), ("Procesos", C["violeta"])],
                     leyenda_x=272, label_size=16)


def _t_orbita():
    return P.orbita(210, 150, 120, 76, label_satelite="Hito", label_size=16)


def _t_radial():
    return P.radial(210, 140, 16, 84, 8, label="Aliados", label_size=16)


def _t_contenedor():
    return P.contenedor(120, 92, 180, 110, C["violeta"], "Tablero", "grafico", 16)


def _t_convergencia():
    return P.convergencia(24, 250, 210, [
        {"label": "Tarea", "color": C["violeta"]},
        {"label": "Proceso", "color": C["aqua"]},
        {"label": "Otra", "color": C["gris"], "dash": DOT}],
        {"label": "Resultado", "color": C["naranja"]},
        y_span=120, label_size=16, salida_dx=110, salida_dy=-130)


def _t_anillo_programa():
    return P.anillo_programa(210, 150, 130, 62, label_size=15)


def _t_onda_inflexion():
    svg, _ = P.onda_inflexion(60, 360, 190, 52, label="Inflexión", label_size=16)
    return svg


def _t_diana():
    return P.diana(210, 140, (34, 66, 98), label="Foco", label_size=16)


def _t_rotulo():
    return (P.rotulo(210, 130, "Rótulo del esquema", C["violeta"], "middle", 22)
            + P.rotulo(210, 180, "Gotham Narrow · uppercase", C["aqua"], "middle", 16))


def _t_firma():
    return P.firma(x_der=380, y_centro=150)


def _t_pager():
    return (P.pager(1, 120, 150) + P.pager(7, 210, 150) + P.pager(12, 300, 150))


def _t_linea_base_punteada():
    return P.linea_base_punteada(40, 380, 150, 16, 2.5)


THUMBS = {
    "nodo": _t_nodo,
    "trayectoria": _t_trayectoria,
    "anillos": _t_anillos,
    "orbita": _t_orbita,
    "radial": _t_radial,
    "contenedor": _t_contenedor,
    "convergencia": _t_convergencia,
    "anillo_programa": _t_anillo_programa,
    "onda_inflexion": _t_onda_inflexion,
    "diana": _t_diana,
    "rotulo": _t_rotulo,
    "firma": _t_firma,
    "pager": _t_pager,
    "linea_base_punteada": _t_linea_base_punteada,
}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "catalogo")
    os.makedirs(out, exist_ok=True)
    svgs, dests = [], []
    for name, fn in THUMBS.items():
        body = fn()
        svg = P.documento(body, P.chars_usados(body), w=W, h=H)
        with open(os.path.join(out, name + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        svgs.append(svg)
        dests.append(os.path.join(out, name + ".png"))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for svg, dest in zip(svgs, dests):
            page.set_content('<html><head><meta charset="utf-8"></head>'
                             '<body style="margin:0;background:#FAF8F5">' + svg
                             + "</body></html>")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(50)
            page.screenshot(path=dest, clip={"x": 0, "y": 0, "width": W, "height": H})
            print("  ", os.path.basename(dest))
        b.close()


if __name__ == "__main__":
    main()
