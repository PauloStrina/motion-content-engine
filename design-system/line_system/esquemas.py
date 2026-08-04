#!/usr/bin/env python3
"""esquemas.py — composiciones declarativas construidas sobre `primitivas.py`.

Cada funcion recibe (box, p): `box` = (x, y, w, h) de la zona visual disponible
y `p` = el dict `esquema` del spec JSON. Devuelve un string SVG.

El layout se resuelve aca: el spec nunca trae coordenadas.
"""
from __future__ import annotations

import math

import primitivas as P
from primitivas import C, DOT


def col(name, default="violeta"):
    return C.get(name or default, C[default])


def _b(box):
    x, y, w, h = box
    return x, y, w, h, x + w / 2, y + h / 2


# ------------------------------------------------------------------ genericos


def s_trayectoria(box, p):
    x, y, w, h, cx, cy = _b(box)
    nodos = [{"color": col(n.get("color")), "label": n.get("label"),
              "r": n.get("r", 14)} for n in p["nodos"]]
    labels = [n.get("label") or "" for n in p["nodos"]]
    ls = p.get("label_size", 22)
    # los rotulos intermedios salen hacia abajo-derecha: bajo una curva
    # ascendente ese cuadrante siempre queda limpio.
    pad_der = max(90.0, P.rotulo_w(labels[-1], ls) / 2 + 12)
    x0, x1 = x + 92, x + w - pad_der
    for i, n in enumerate(nodos):
        n["side"] = "arriba" if i == len(nodos) - 1 else "abajo_der"
    top = y + 78 if labels[-1] else y + 40
    bot = y + h - 62
    svg, _ = P.trayectoria(x0, bot, x1, top, nodos, dash=DOT if p.get("dash") else None,
                           color=col(p.get("color")), label_size=ls)
    return svg


def s_convergencia(box, p):
    x, y, w, h, cx, cy = _b(box)
    ent = [{"label": e.get("label"), "color": col(e.get("color")),
            "dash": DOT if e.get("dash") else None} for e in p["entradas"]]
    sal = {"label": p["salida"].get("label"), "color": col(p["salida"].get("color"), "naranja")}
    ls = p.get("label_size", 22)
    x0 = x + 8
    sal_w = P.rotulo_w(sal["label"] or "", ls)
    x_fin = x + w - max(60.0, sal_w / 2 + 8)
    dx = min(300.0, w * 0.34)
    x_hub = x_fin - dx
    y_hub = y + h * 0.66
    y_top = y + 62
    return P.convergencia(x0, x_hub, y_hub, ent, sal,
                          y_span=min(200.0, h * 0.52), label_size=ls,
                          hub_color=col(p.get("hub_color")),
                          hub_label=p.get("hub_label"),
                          salida_dx=dx, salida_dy=y_top - y_hub)


def s_anillos(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    leyenda = [(t, col(c)) for t, c in p.get("leyenda", [])]
    radios = p.get("radios") or [70 + 42 * i for i in range(len(p["colores"]))]
    colores = [col(c) for c in p["colores"]]
    rmax = max(radios)
    if leyenda:
        leg_w = 46 + max(P.rotulo_w(t, ls) for t, _ in leyenda)
        gx = x + (w - (2 * rmax + 62 + leg_w)) / 2
        ccx = gx + rmax
        lx = ccx + rmax + 62
    else:
        ccx, lx = cx, None
    ccy = cy - 6 if not p.get("centro_label") else cy
    return P.anillos(ccx, ccy, radios, colores, span=p.get("span", 285),
                     centro_color=col(p["centro_color"]) if p.get("centro_color") else None,
                     centro_r=p.get("centro_r", 0),
                     centro_label=p.get("centro_label"),
                     leyenda=leyenda or None, leyenda_x=lx, label_size=ls)


def s_anillo_programa(box, p):
    x, y, w, h, cx, cy = _b(box)
    r = min(242.0, (h - 30) / 2, w / 2 - 40)
    return P.anillo_programa(cx, cy, r, r * 0.48, label_size=p.get("label_size", 22))


def s_radial(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    r_spoke = min(140.0, (h - 110) / 2)
    return P.radial(cx, cy - 18, r_core=24, r_spoke=r_spoke, n=p.get("n", 8),
                    core_color=col(p.get("core_color")),
                    spoke_color=col(p.get("spoke_color"), "aqua"),
                    label=p.get("label"), label_size=ls)


def s_orbita(box, p):
    x, y, w, h, cx, cy = _b(box)
    rx = min(210.0, w / 2 - 60)
    ry = min(132.0, (h - 120) / 2)
    return P.orbita(cx, cy - 12, rx, ry, color=col(p.get("color")),
                    centro_color=col(p.get("centro_color")),
                    satelite_color=col(p.get("satelite_color"), "naranja"),
                    satelite_ang=p.get("satelite_ang", -35),
                    label_centro=p.get("label_centro"),
                    label_satelite=p.get("label_satelite"),
                    label_size=p.get("label_size", 22))


def s_diana(box, p):
    x, y, w, h, cx, cy = _b(box)
    rmax = min(150.0, (h - 120) / 2)
    radios = tuple(rmax * f for f in (0.34, 0.67, 1.0))
    return P.diana(cx, cy - 14, radios, color=col(p.get("color")),
                   nodo_color=col(p.get("nodo_color"), "naranja"),
                   nodo_r_pos=radios[0] * 0.78, label=p.get("label"),
                   label_size=p.get("label_size", 22))


def s_onda_inflexion(box, p):
    x, y, w, h, cx, cy = _b(box)
    svg, _ = P.onda_inflexion(x + 90, x + w - 90, cy + 44,
                              amp=min(78.0, (h - 150) / 2.6),
                              color=col(p.get("color")),
                              marca_color=col(p.get("marca_color"), "naranja"),
                              label=p.get("label"),
                              label_size=p.get("label_size", 22))
    return svg


# ------------------------------------------------------------------ pieza B


def s_ojo_desconectado(box, p):
    x, y, w, h, cx, cy = _b(box)
    r = min(104.0, (h - 130) / 2)
    ox = cx - 96
    out = [f'<circle cx="{ox:.1f}" cy="{cy - 10:.1f}" r="{r:.1f}" fill="none" '
           f'stroke="{C["violeta"]}" stroke-width="3.5"/>']
    out.append(P.icono("ojo", ox, cy - 10, r / 46.0, C["violeta"], 3.0))
    for dx, dy, cc, rr in ((196, -74, "naranja", 15), (232, 22, "aqua", 13),
                           (168, 92, "aqua", 11)):
        out.append(P.nodo(ox + dx, cy - 10 + dy, rr, C[cc]))
    if p.get("label"):
        out.append(P.rotulo(ox, cy - 10 + r + 40, p["label"], C["violeta"], "middle",
                            p.get("label_size", 22)))
    return "".join(out)


def s_nodos_a_contenedor(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    yb = cy - 6
    cw, ch = 168.0, 112.0
    out = [P.path(f"M{x + 96:.1f},{yb:.1f} L{x + w - 96:.1f},{yb:.1f}",
                  C["violeta"], 3)]
    izq = [C["violeta"], C["aqua"], C["naranja"]]
    for i, cc in enumerate(izq):
        out.append(P.nodo(x + 96 + i * 62, yb, 13, cc))
    der = [C["aqua"], C["violeta"]]
    for i, cc in enumerate(der):
        out.append(P.nodo(x + w - 96 - i * 62, yb, 13, cc))
    out.append(f'<rect x="{cx - cw / 2:.1f}" y="{yb - ch / 2:.1f}" width="{cw:.1f}" '
               f'height="{ch:.1f}" rx="6" fill="{C["fondo"]}" stroke="{C["violeta"]}" '
               f'stroke-width="3"/>')
    out.append(P.icono("personas", cx, yb, 1.5, C["violeta"], 2.6))
    if p.get("label"):
        out.append(P.rotulo(cx, yb + ch / 2 + ls + 14, p["label"], C["violeta"],
                            "middle", ls))
    return "".join(out)


def s_dispersion(box, p):
    """Curvas que se cruzan una vez y despues se dispersan a nodos separados."""
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    x0, x1 = x + 108, x + w - 118
    spread = min(122.0, (h - 150) / 2)
    colores = ["violeta", "aqua", "naranja"]
    orig_y = [cy - spread * 0.55, cy, cy + spread * 0.55]
    dest_y = [cy + spread, cy - spread * 0.62, cy + spread * 0.18]
    out = []
    for i, cc in enumerate(colores):
        oy, dy = orig_y[i], dest_y[i]
        bow = (-1) ** i * 34
        out.append(P.curva([(x0, oy), ((x0 + x1) * 0.5, (oy + dy) / 2 + bow),
                            (x1 - i * 44, dy)], C[cc], 3, DOT))
        out.append(P.nodo(x0, oy, 11, C[cc]))
        out.append(P.nodo(x1 - i * 44, dy, 14, C[cc]))
    if p.get("label"):
        out.append(P.rotulo(cx, y + h - 14, p["label"], C["violeta"], "middle", ls))
    return "".join(out)


def s_cubo_a_calendario(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    yb = cy - 10
    nx = x + 156
    out = [P.nodo(nx, yb, 54, C["violeta"], "cubo")]
    bw, bh = 168.0, 168.0
    bx = x + w - 156 - bw / 2
    out.append(P.path(f"M{nx + 70:.1f},{yb:.1f} L{bx - 18:.1f},{yb:.1f}",
                      C["naranja"], 3, DOT))
    out.append(f'<rect x="{bx:.1f}" y="{yb - bh / 2:.1f}" width="{bw:.1f}" '
               f'height="{bh:.1f}" rx="8" fill="none" stroke="{C["naranja"]}" '
               f'stroke-width="3.5"/>')
    out.append(P.icono("calendario", bx + bw / 2, yb - 34, 1.45, C["naranja"], 2.8))
    out.append(P.texto(bx + bw / 2, yb + 52, "16", "futura", 50, C["naranja"], "middle"))
    out.append(P.rotulo(nx, yb + 54 + ls + 16, p.get("label_izq", ""), C["violeta"],
                        "middle", ls))
    out.append(P.rotulo(bx + bw / 2, yb + bh / 2 + ls + 16, p.get("label_der", ""),
                        C["naranja"], "middle", ls))
    return "".join(out)


def s_tres_nodos_pico(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    nodos = p["nodos"]
    yb = cy + 48
    ypico = cy - 62
    xs = [x + 150, cx, x + w - 150]
    ys = [yb, ypico, yb]
    out = [P.path(f"M{xs[0]:.1f},{ys[0]:.1f} L{xs[1]:.1f},{ys[1]:.1f} "
                  f"L{xs[2]:.1f},{ys[2]:.1f}", C["violeta"], 3)]
    for i, n in enumerate(nodos):
        cc = col(n.get("color"))
        out.append(P.nodo(xs[i], ys[i], 15, cc))
        if n.get("label"):
            side = "arriba" if i == 1 else "abajo"
            out.append(P.rotulo_pos(xs[i], ys[i], n["label"], cc, side, 15, ls))
    return "".join(out)


def s_estrella_a_nodo(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    r = 62.0
    sx, sy = x + 168, y + h - 92
    nx, ny = x + w - 168, y + 84
    out = [P.curva([(sx + r + 8, sy - 12), ((sx + nx) / 2, sy - 74), (nx, ny)],
                   C["naranja"], 3, DOT)]
    out.append(P.nodo(sx, sy, r, C["violeta"], "estrella"))
    out.append(P.nodo(nx, ny, 17, C["naranja"]))
    if p.get("label_izq"):
        out.append(P.rotulo(sx, sy + r + ls + 14, p["label_izq"], C["violeta"], "middle", ls))
    if p.get("label_der"):
        out.append(P.rotulo(nx, ny - 32, p["label_der"], C["naranja"], "middle", ls))
    return "".join(out)


# ------------------------------------------------------------------ pieza C


def s_secuencia_horizontal(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    nodos = p["nodos"]
    n = len(nodos)
    pad = max(P.rotulo_w(nodos[0].get("label", ""), ls) / 2 + 8,
              P.rotulo_w(nodos[-1].get("label", ""), ls) / 2 + 8, 60.0)
    x0, x1 = x + pad, x + w - pad
    yb = cy - 4
    out = []
    for i in range(n - 1):
        xa = x0 + (x1 - x0) * i / (n - 1)
        xbb = x0 + (x1 - x0) * (i + 1) / (n - 1)
        seg = nodos[i + 1].get("tramo", {})
        out.append(P.path(f"M{xa + 20:.1f},{yb:.1f} L{xbb - 20:.1f},{yb:.1f}",
                          col(seg.get("color")), 3,
                          DOT if seg.get("dash") else None))
    for i, nd in enumerate(nodos):
        px = x0 + (x1 - x0) * i / (n - 1)
        cc = col(nd.get("color"))
        rr = nd.get("r", 15)
        out.append(P.nodo(px, yb, rr, cc, relleno=not nd.get("hueco")))
        if nd.get("label"):
            side = "arriba" if i % 2 == 0 else "abajo"
            out.append(P.rotulo_pos(px, yb, nd["label"], cc, side, rr, ls))
    return "".join(out)


def s_dos_jorobas(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    yb = cy + 66
    amp = min(118.0, (h - 170))
    x0, x1 = x + 96, x + w - 110
    m = (x1 - x0)
    p1 = [(x0, yb), (x0 + m * 0.10, yb - amp * 0.85), (x0 + m * 0.22, yb - amp),
          (x0 + m * 0.34, yb - amp * 0.85), (x0 + m * 0.44, yb)]
    p2 = [(x0 + m * 0.44, yb), (x0 + m * 0.54, yb - amp * 0.7),
          (x0 + m * 0.66, yb - amp * 0.82), (x0 + m * 0.78, yb - amp * 0.7),
          (x0 + m * 0.88, yb)]
    out = [P.path(f"M{x0 - 26:.1f},{yb:.1f} L{x1:.1f},{yb:.1f}", C["gris"], 2.4, DOT)]
    out.append(P.curva(p1, C["violeta"], 3.4))
    out.append(P.curva(p2, C["aqua"], 3.4))
    out.append(P.nodo(x0 + m * 0.22, yb - amp, 14, C["naranja"]))
    out.append(P.nodo(x1, yb, 15, C["violeta"]))
    out.append(P.rotulo(x0 + m * 0.22, yb + ls + 20, p["labels"][0], C["violeta"], "middle", ls))
    out.append(P.rotulo(x0 + m * 0.66, yb + ls + 20, p["labels"][1], C["aqua"], "middle", ls))
    out.append(P.rotulo(x1, yb - 34, p["labels"][2], C["violeta"], "middle", ls))
    return "".join(out)


def s_aislados_vs_anillo(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    lx = x + w * 0.24
    out = [P.nodo(lx - 46, cy - 44, 15, C["violeta"]),
           P.nodo(lx + 44, cy + 14, 15, C["aqua"])]
    out.append(P.rotulo_multi(lx, cy + 108, p["label_izq"], C["violeta"], w * 0.42, ls))
    rx = x + w * 0.74
    r = min(112.0, (h - 160) / 2)
    out.append(P.arco(rx, cy - 10, r, -58, 232, C["violeta"], 3.5))
    out.append(P.nodo(rx + r * math.cos(math.radians(-58)),
                      cy - 10 + r * math.sin(math.radians(-58)), 12, C["violeta"]))
    out.append(P.rotulo_multi(rx, cy - 10 + r + 46, p["label_der"], C["violeta"], w * 0.4, ls))
    return "".join(out)


def s_despegue(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    yb = cy + 76
    x0, x1 = x + 96, x + w - 116
    out = [P.path(f"M{x0:.1f},{yb:.1f} L{x1:.1f},{yb:.1f}", C["gris"], 2.6, DOT)]
    out.append(P.rotulo(x0 + (x1 - x0) * 0.24, yb + ls + 22, p["label_base"],
                        C["gris"], "middle", ls))
    top = max(y + 66, yb - (h - 150))
    px = [(x0 + (x1 - x0) * 0.30, yb), (x0 + (x1 - x0) * 0.58, yb - (yb - top) * 0.45),
          (x1, top)]
    out.append(P.curva(px, C["aqua"], 5.0))
    out.append(P.nodo(px[0][0], px[0][1], 11, C["aqua"]))
    out.append(P.nodo(x1, top, 16, C["aqua"]))
    out.append(P.rotulo(x1, top - 30, p["label_nueva"], C["aqua"], "middle", ls))
    return "".join(out)


def s_curva_hito(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    x0, x1 = x + 110, x + w - 110
    yb, top = y + h - 74, y + 76
    pts = [(x0, yb), ((x0 + x1) / 2, yb - (yb - top) * 0.52), (x1, top)]
    out = [P.curva(pts, C["violeta"], 3.4)]
    out.append(P.nodo(x0, yb, 11, C["violeta"]))
    out.append(P.nodo(pts[1][0], pts[1][1], 15, C["naranja"]))
    out.append(P.rotulo_multi(pts[1][0] + 26, pts[1][1] + 46, p["label_medio"],
                              C["naranja"], w * 0.42, ls, anchor="start"))
    out.append(P.nodo(x1, top, 15, C["violeta"]))
    out.append(P.rotulo(x1, top - 30, p["label_fin"], C["violeta"], "middle", ls))
    return "".join(out)


def s_curva_s(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    nodos = p["nodos"]
    x0, x1 = x + 116, x + w - 116
    yb, top = y + h - 96, y + 78
    xs = [x0 + (x1 - x0) * t for t in (0.0, 0.33, 0.66, 1.0)]
    ys = [yb, yb - (yb - top) * 0.16, yb - (yb - top) * 0.72, top]
    pts = list(zip(xs, ys))
    out = [P.curva([(xs[0], ys[0]), (xs[0] + (xs[1] - xs[0]) * 0.6, ys[0] - 6),
                    (xs[1], ys[1]), (xs[1] + 40, ys[1] - 4),
                    (xs[2], ys[2]), (xs[3], ys[3])], C["violeta"], 3.4)]
    sides = ["abajo", "abajo_der", "abajo_der", "arriba"]
    for i, nd in enumerate(nodos):
        cc = col(nd.get("color"))
        out.append(P.nodo(xs[i], ys[i], 15, cc))
        out.append(P.rotulo_pos(xs[i], ys[i], nd["label"], cc, sides[i], 15, ls))
    return "".join(out)


def s_barras_vs_curva(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 20)
    barras = p["barras"]
    bx = x + 8
    bw = w * 0.30
    y0 = cy - (len(barras) - 1) * 46 / 2 - 10
    out = []
    for i, lab in enumerate(barras):
        by = y0 + i * 46
        out.append(P.path(f"M{bx:.1f},{by:.1f} L{bx + bw:.1f},{by:.1f}", C["gris"], 3))
        out.append(P.nodo(bx + bw, by, 9, C["gris"]))
        out.append(P.rotulo(bx, by - 12, lab, C["gris"], "start", ls))
    sep = x + w * 0.42
    out.append(P.path(f"M{sep:.1f},{y + 44:.1f} L{sep:.1f},{y + h - 54:.1f}",
                      C["gris_claro"], 2, dash="6 8", cap="butt"))
    cx0, cx1 = sep + 78, x + w - 96
    cyb, ctop = y + h - 86, y + 76
    nodos = p["curva"]
    xs = [cx0, (cx0 + cx1) / 2, cx1]
    ys = [cyb, cyb - (cyb - ctop) * 0.42, ctop]
    out.append(P.curva(list(zip(xs, ys)), C["aqua"], 4.0))
    sides = ["abajo", "abajo_der", "arriba"]
    for i, nd in enumerate(nodos):
        cc = col(nd.get("color"), "aqua")
        out.append(P.nodo(xs[i], ys[i], 14, cc))
        out.append(P.rotulo_pos(xs[i], ys[i], nd["label"], cc, sides[i], 14, ls))
    return "".join(out)


def s_fin_vs_medio(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 20)
    lx0, lx1 = x + 26, x + w * 0.28
    ly = cy + 22
    out = [P.path(f"M{lx0:.1f},{ly:.1f} L{lx1:.1f},{ly:.1f}", C["naranja"], 3.4)]
    out.append(P.nodo(lx1, ly, 16, C["naranja"]))
    out.append(P.rotulo(lx1, ly + 46, p["label_fin"], C["naranja"], "middle", ls))
    sep = x + w * 0.38
    out.append(P.path(f"M{sep:.1f},{y + 40:.1f} L{sep:.1f},{y + h - 50:.1f}",
                      C["gris_claro"], 2, dash="6 8", cap="butt"))
    ent = [{"label": e["label"], "color": col(e.get("color"))} for e in p["entradas"]]
    x0 = sep + 34
    x_hub = x + w - 150
    y_hub = y + h * 0.68
    return "".join(out) + P.convergencia(
        x0, x_hub, y_hub, ent,
        {"label": None, "color": C["violeta"]},
        y_span=min(170.0, h * 0.46), label_size=ls,
        hub_color=C["naranja"], hub_label=p["label_medio"],
        salida_dx=118, salida_dy=(y + 74) - y_hub)


def s_mapa_curva(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    x0, x1 = x + 96, x + w - 120
    top = y + 84
    yo = y + h - 92
    for_out = []
    for off in (-0.14, 0.24, 0.60):
        dy = min(yo + (top - yo) * off, y + h - 12)
        pts = [(x0, yo), ((x0 + x1) / 2, yo + (dy - yo) * 0.45), (x1, dy)]
        for_out.append(P.curva(pts, C["gris"], 2.8, DOT))
    pts = [(x0, yo), ((x0 + x1) * 0.54, yo + (top - yo) * 0.42), (x1, top)]
    for_out.append(P.curva(pts, C["aqua"], 5.0))
    for_out.append(P.nodo(x0, yo, 13, C["aqua"]))
    for_out.append(P.nodo(x1, top, 17, C["naranja"]))
    for_out.append(P.rotulo_multi(x1 - 8, top - 44, p["label"], C["naranja"], w * 0.5, ls))
    return "".join(for_out)


# ------------------------------------------------------------------ pieza D


def s_anillo_nucleo(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    r = min(126.0, (h - 130) / 2)
    ccx = cx - 62
    out = [P.arco(ccx, cy - 10, r, -90 - 142, -90 + 142, C["aqua"], 3.6)]
    out.append(P.nodo(ccx, cy - 10, 26, C["violeta"]))
    out.append(P.rotulo(ccx, cy - 10 + r + ls + 20, p["label"], C["violeta"], "middle", ls))
    for i in range(3):
        out.append(P.nodo(ccx + r + 78 + i * 46, cy - 10, 11, C["naranja"]))
    return "".join(out)


def s_anillo_hueco(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    r = min(146.0, (h - 90) / 2)
    out = [P.arco(cx, cy, r, -90 - 138, -90 + 138, C["aqua"], 3.6)]
    out.append(P.rotulo_multi(cx, cy, p["label"], C["violeta"], r * 1.55, ls))
    a = math.radians(-38)
    out.append(P.nodo(cx + r * math.cos(a), cy + r * math.sin(a), 15, C["naranja"]))
    return "".join(out)


def s_anillos_capa_suelta(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    ccx = cx - 44
    radios = [72, 112, 152]
    colores = [C["aqua"], C["violeta"], C["naranja"]]
    out = [P.anillos(ccx, cy - 8, radios, colores, span=272)]
    r = 196
    out.append(P.arco(ccx + 34, cy - 26, r, -104, 34, C["violeta"], 3.6, dash="14 12"))
    a = math.radians(34)
    ex, ey = ccx + 34 + r * math.cos(a), cy - 26 + r * math.sin(a)
    out.append(P.nodo(ex, ey, 13, C["violeta"]))
    out.append(P.rotulo(ex + 22, ey + 8, p["label"], C["violeta"], "start", ls))
    return "".join(out)


def s_dos_contenedores(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    cw, ch = 244.0, min(178.0, h - 130)
    gap = 74.0
    x0 = cx - (cw * 2 + gap) / 2
    top = cy - ch / 2 - 14
    out = []
    for i, c in enumerate(p["contenedores"]):
        cc = col(c.get("color"))
        out.append(P.contenedor(x0 + i * (cw + gap), top, cw, ch, cc,
                                None, c.get("mini", "grafico"), ls))
        out.append(P.rotulo_multi(x0 + i * (cw + gap) + cw / 2, top + ch + 34,
                                  c["label"], cc, cw + 30, ls))
    return "".join(out)


def s_contenedor_a_nodo(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    cw, ch = 216.0, min(158.0, h - 168)
    x0 = x + 40
    top = y + h - ch - 74
    cc = col(p.get("color_contenedor"), "aqua")
    out = [P.contenedor(x0, top, cw, ch, cc, None, p.get("mini", "grafico"), ls)]
    out.append(P.rotulo_multi(x0 + cw / 2, top + ch + 34, p["label_contenedor"], cc,
                              cw + 90, ls))
    mx, my = x0 + cw + 118, top + ch / 2 - 18
    out.append(P.curva([(x0 + cw + 14, top + ch / 2), (mx, my)], cc, 3.2))
    out.append(P.nodo(mx, my, 12, cc))
    nx, ny = x + w - 96, y + 82
    out.append(P.curva([(mx, my), ((mx + nx) / 2 + 20, my - (my - ny) * 0.5), (nx, ny)],
                       C["naranja"], 3.4))
    out.append(P.nodo(nx, ny, 17, C["naranja"]))
    if p.get("label_nodo"):
        out.append(P.rotulo_multi(nx - 20, ny - 44, p["label_nodo"], C["naranja"],
                                  w * 0.5, ls))
    return "".join(out)


def s_contenedor_sobre_anillos(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    leyenda = [(t, col(c)) for t, c in p.get("leyenda", [])]
    radios = [72, 110, 148]
    colores = [C["aqua"], C["violeta"], C["naranja"]]
    leg_w = 46 + max(P.rotulo_w(t, ls) for t, _ in leyenda)
    gx = x + (w - (2 * radios[-1] + 62 + leg_w)) / 2
    ccx = gx + radios[-1]
    ccy = y + h - radios[-1] - 26
    cw, ch = 190.0, 96.0
    top = y + 24
    out = [P.contenedor(ccx - cw / 2, top, cw, ch, C["aqua"], None, "grafico", ls)]
    out.append(P.rotulo_multi(ccx + cw / 2 + 26, top + ch / 2, p["label_contenedor"],
                              C["aqua"], w * 0.4, ls, anchor="start"))
    out.append(P.path(f"M{ccx:.1f},{top + ch:.1f} L{ccx:.1f},{ccy - radios[-1] - 10:.1f}",
                      C["aqua"], 2.6, DOT))
    out.append(P.anillos(ccx, ccy, radios, colores, span=250,
                         leyenda=leyenda, leyenda_x=ccx + radios[-1] + 62,
                         leyenda_y=ccy - 42, label_size=ls))
    return "".join(out)


def s_curva_atraviesa_anillos(box, p):
    x, y, w, h, cx, cy = _b(box)
    ls = p.get("label_size", 22)
    radios = [66, 102, 138]
    colores = [C["aqua"], C["violeta"], C["naranja"]]
    ccx = x + 208
    ccy = cy + 16
    out = [P.anillos(ccx, ccy, radios, colores, span=260)]
    sx, sy = x + 34, y + h - 56
    nx, ny = x + w - 116, y + 72
    out.append(P.curva([(sx, sy), (ccx - 20, ccy + 46), (ccx + 120, ccy - 40),
                        (nx, ny)], col(p.get("color")), 4.0))
    out.append(P.nodo(sx, sy, 14, col(p.get("color_inicio"), "aqua")))
    if p.get("label_inicio"):
        out.append(P.rotulo(sx + 22, sy + 8, p["label_inicio"],
                            col(p.get("color_inicio"), "aqua"), "start", ls))
    out.append(P.nodo(nx, ny, 17, C["naranja"]))
    out.append(P.rotulo_multi(nx - 10, ny - 46, p["label_fin"], C["naranja"], w * 0.44, ls))
    return "".join(out)


SCHEMAS = {
    "trayectoria": s_trayectoria,
    "convergencia": s_convergencia,
    "anillos": s_anillos,
    "anillo_programa": s_anillo_programa,
    "radial": s_radial,
    "orbita": s_orbita,
    "diana": s_diana,
    "onda_inflexion": s_onda_inflexion,
    "ojo_desconectado": s_ojo_desconectado,
    "nodos_a_contenedor": s_nodos_a_contenedor,
    "dispersion": s_dispersion,
    "cubo_a_calendario": s_cubo_a_calendario,
    "tres_nodos_pico": s_tres_nodos_pico,
    "estrella_a_nodo": s_estrella_a_nodo,
    "secuencia_horizontal": s_secuencia_horizontal,
    "dos_jorobas": s_dos_jorobas,
    "aislados_vs_anillo": s_aislados_vs_anillo,
    "despegue": s_despegue,
    "curva_hito": s_curva_hito,
    "curva_s": s_curva_s,
    "barras_vs_curva": s_barras_vs_curva,
    "fin_vs_medio": s_fin_vs_medio,
    "mapa_curva": s_mapa_curva,
    "anillo_nucleo": s_anillo_nucleo,
    "anillo_hueco": s_anillo_hueco,
    "anillos_capa_suelta": s_anillos_capa_suelta,
    "dos_contenedores": s_dos_contenedores,
    "contenedor_a_nodo": s_contenedor_a_nodo,
    "contenedor_sobre_anillos": s_contenedor_sobre_anillos,
    "curva_atraviesa_anillos": s_curva_atraviesa_anillos,
}


def dibujar(box, p):
    return SCHEMAS[p["tipo"]](box, p)
