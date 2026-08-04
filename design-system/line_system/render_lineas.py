#!/usr/bin/env python3
"""render_lineas.py — renderer del sistema visual `line_system` de Motion.

Uso:
    python render_lineas.py <spec.json> <outdir> [--no-png] [--no-contact-sheet]

Emite un SVG autocontenido por placa (fuentes OTF embebidas y subseteadas),
su PNG a 1080x1350 y un contact sheet de la pieza completa.

El spec JSON declara copy literal + esquema declarativo. Nunca coordenadas:
el layout lo resuelve este archivo.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import primitivas as P  # noqa: E402
import esquemas as E  # noqa: E402
from primitivas import C  # noqa: E402

MARGEN = 96
TEXTO_TOP = 236
FIRMA_Y = 1252
ZONA_VISUAL_BOTTOM = 1178

ESTILOS = {
    # clave: (fuente, size_max, size_min, line_height_factor, color)
    "destacada": ("futura", 74, 52, 1.00, "violeta"),
    "cuerpo": ("lyon", 46, 34, 1.30, "violeta"),
    "cuerpo_negro": ("lyon", 44, 32, 1.30, "negro"),
}


# --------------------------------------------------------------- texto


def _bloque_auto(items, x, y_top, max_w, max_h, anchor):
    """Ajusta el cuerpo de texto para que entre en (max_w, max_h) sin bajar de
    la legibilidad minima. Devuelve (svg, y_bottom)."""
    escala = 1.0
    while True:
        svg, y = [], y_top
        ok = True
        for it in items:
            fuente, smax, smin, lhf, color_def = ESTILOS[it.get("estilo", "cuerpo")]
            size = max(smin, smax * escala)
            txt = it["texto"]
            if fuente == "futura":
                txt = txt.upper()
            lineas = P.wrap(txt, fuente, size, max_w)
            lh = size * lhf
            b, y2 = P.bloque(x, y, lineas, fuente, size, lh,
                             C[it.get("color", color_def)], anchor)
            svg.append(b)
            y = y2 + it.get("gap", 22) * escala
        alto = y - y_top
        if alto <= max_h or escala <= 0.72:
            return "".join(svg), y - items[-1].get("gap", 22) * escala
        escala -= 0.04


# --------------------------------------------------------------- placas


def placa_carrusel(spec, pl, idx):
    align = spec.get("align", "center")
    anchor = "middle" if align == "center" else "start"
    x_txt = 540 if align == "center" else MARGEN
    max_w = 1080 - 2 * MARGEN if align != "center" else 900
    if align == "center":
        x_txt = 540
    cuerpo = [P.pager(pl.get("n", idx + 1))]
    txt_svg, y_end = _bloque_auto(pl["texto"], x_txt, TEXTO_TOP, max_w,
                                  spec.get("alto_texto", 340), anchor)
    cuerpo.append(txt_svg)

    y0 = max(y_end + 74, TEXTO_TOP + 200)
    inset_bottom = 62 if pl.get("onda", spec.get("onda", False)) else 8
    box = (MARGEN, y0, 1080 - 2 * MARGEN, ZONA_VISUAL_BOTTOM - y0 - inset_bottom)
    cuerpo.append(E.dibujar(box, pl["esquema"]))
    if pl.get("onda", spec.get("onda", False)):
        cuerpo.append(P.linea_base_punteada(MARGEN + 10, 1080 - MARGEN - 10,
                                            ZONA_VISUAL_BOTTOM - 18))
    cuerpo.append(P.firma(y_centro=FIRMA_Y))
    body = "".join(cuerpo)
    return P.documento(body, P.chars_usados(body))


# --------------------------------------------------------------- linkedin


def placa_linkedin(spec):
    pl = spec["placa"]
    cuerpo = []
    # headline
    size = 78
    lh = 80
    y = 152
    for ln in pl["headline"]:
        cuerpo.append(P.texto(MARGEN, y + size * 0.78, ln.upper(), "futura", size,
                              C["violeta"]))
        y += lh
    # separador
    y += 30
    cuerpo.append(P.nodo(MARGEN + 9, y, 9, C["naranja"]))
    y += 40
    # bajada
    bs = 29
    for ln in pl["bajada"]:
        cuerpo.append(P.texto(MARGEN, y + bs * 0.78, ln, "gotham", bs, C["negro"]))
        y += bs * 1.42
    # secuencia de nodos
    pasos = pl["pasos"]
    y_top = y + 52
    y_bot = 1178
    r = 38
    pesos = [1.0, 1.0, 1.0, 1.5]
    total = sum(pesos)
    disp = y_bot - y_top - 2 * r
    cxs, acum = [], 0.0
    for i in range(len(pasos)):
        cy = y_top + r + disp * acum / total
        if i < len(pesos):
            acum += pesos[i]
        cx = MARGEN + r + (10 if i % 2 else 0)
        cxs.append((cx, cy))
    # conectores
    for i in range(len(pasos) - 1):
        (x0, y0), (x1, y1) = cxs[i], cxs[i + 1]
        if pasos[i + 1].get("conector") == "propagacion":
            for off in (-34, 0, 34):
                pts = [(x0, y0 + r + 5),
                       (x0 + off * 0.5, (y0 + y1) / 2),
                       (x1 + off, y1 - r - 14)]
                cuerpo.append(P.curva(pts, C["aqua"], 2.8))
                ax, ay = pts[-1]
                cuerpo.append(P.path(
                    f"M{ax - 7:.1f},{ay - 11:.1f} L{ax:.1f},{ay:.1f} "
                    f"L{ax + 7:.1f},{ay - 11:.1f}", C["aqua"], 2.8))
        else:
            s = 1 if i % 2 == 0 else -1
            pts = [(x0, y0 + r + 4), (x0 + s * 26, (y0 + y1) / 2), (x1, y1 - r - 4)]
            cuerpo.append(P.curva(pts, C["violeta"], 3.0))
    # nodos + texto
    for i, (paso, (cx, cy)) in enumerate(zip(pasos, cxs)):
        cc = C[paso.get("color", "violeta")]
        cuerpo.append(P.nodo(cx, cy, r, cc, paso["icono"]))
        if paso.get("icono_texto"):
            cuerpo.append(P.texto(cx, cy + 14, paso["icono_texto"], "gotham", 17,
                                  C["blanco"], "middle"))
        tx = MARGEN + 2 * r + 46
        titulo = paso["titulo"]
        ts = 36
        n = len(titulo)
        y_t = cy - (16 if n == 1 else 34)
        for j, ln in enumerate(titulo):
            cuerpo.append(P.texto(tx, y_t + j * 33, ln.upper(), "futura", ts, cc))
        desc_lines = P.wrap(paso["desc"], "gotham", 24, 1080 - MARGEN - tx)
        y_d = y_t + (len(titulo) - 1) * 33 + 30
        for j, ln in enumerate(desc_lines):
            cuerpo.append(P.texto(tx, y_d + j * 29, ln, "gotham", 24, C["negro"]))
    cuerpo.append(P.firma(y_centro=1284))
    body = "".join(cuerpo)
    return P.documento(body, P.chars_usados(body))


# --------------------------------------------------------------- salida


def rasterizar(svgs, destinos):
    """SVG -> PNG con Chromium (Playwright). Las OTF van embebidas en el SVG."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page(viewport={"width": P.W, "height": P.H},
                          device_scale_factor=1)
        for svg, dest in zip(svgs, destinos):
            page.set_content(
                '<html><head><meta charset="utf-8"></head>'
                '<body style="margin:0;padding:0;background:#FAF8F5">'
                + svg + "</body></html>")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(60)
            page.screenshot(path=dest, clip={"x": 0, "y": 0, "width": P.W, "height": P.H})
            print("  png:", os.path.basename(dest))
        b.close()


def contact_sheet(pngs, titulo, dest, cols=5):
    from PIL import Image, ImageDraw, ImageFont
    cell_w = 340
    cell_h = int(cell_w * P.H / P.W)
    pad = 22
    top = 132
    filas = (len(pngs) + cols - 1) // cols
    W_ = pad + cols * (cell_w + pad)
    H_ = top + filas * (cell_h + pad) + 10
    sheet = Image.new("RGB", (W_, H_), (250, 248, 245))
    d = ImageDraw.Draw(sheet)
    f_tit = ImageFont.truetype(os.path.join(P.FONT_DIR, P.FONT_FILES["futura"]), 62)
    f_num = ImageFont.truetype(os.path.join(P.FONT_DIR, P.FONT_FILES["gotham"]), 22)
    d.text((pad + 6, 42), titulo.upper(), font=f_tit, fill="#50235A")
    for i, p_ in enumerate(pngs):
        im = Image.open(p_).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS)
        x = pad + (i % cols) * (cell_w + pad)
        y = top + (i // cols) * (cell_h + pad)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline=(220, 214, 206))
        d.text((x + 6, y + cell_h + 2), f"{i + 1:02d}", font=f_num, fill="#1A1A1A")
    sheet.save(dest)
    print("  contact sheet:", dest)


def render(spec_path, outdir, png=True, sheet=True):
    spec = json.load(open(spec_path, encoding="utf-8"))
    os.makedirs(os.path.join(outdir, "svg"), exist_ok=True)
    if png:
        os.makedirs(os.path.join(outdir, "png"), exist_ok=True)
    svgs, names = [], []
    if spec.get("layout") == "linkedin_static":
        svgs.append(placa_linkedin(spec))
        names.append(spec["pieza"])
    else:
        for i, pl in enumerate(spec["placas"]):
            svgs.append(placa_carrusel(spec, pl, i))
            names.append(f"placa-{i + 1:02d}")
    svg_paths, png_paths = [], []
    for svg, name in zip(svgs, names):
        sp = os.path.join(outdir, "svg", f"{name}.svg")
        with open(sp, "w", encoding="utf-8") as fh:
            fh.write(svg)
        svg_paths.append(sp)
        png_paths.append(os.path.join(outdir, "png", f"{name}.png"))
        print("  svg:", os.path.basename(sp))
    if png:
        rasterizar(svgs, png_paths)
        if sheet:
            contact_sheet(png_paths, spec.get("titulo", spec["pieza"]),
                          os.path.join(outdir, "contact-sheet.png"),
                          cols=spec.get("sheet_cols", 5))
    return png_paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("outdir")
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--no-contact-sheet", action="store_true")
    a = ap.parse_args()
    print(f"[line_system] {a.spec}")
    render(a.spec, a.outdir, png=not a.no_png, sheet=not a.no_contact_sheet)


if __name__ == "__main__":
    main()
