#!/usr/bin/env python3
"""primitivas.py — vocabulario grafico de la familia visual `line_system` de Motion.

Cada primitiva recibe coordenadas explicitas y devuelve un string SVG.
Sin dependencias externas mas alla de fontTools (solo para medir y subsetear texto).

Convencion de canvas: 1080 x 1350, fondo blanco hueso #FAF8F5.
"""
from __future__ import annotations

import base64
import functools
import io
import math
import os

from fontTools.ttLib import TTFont
from fontTools import subset

DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # design-system/
FONT_DIR = os.path.join(DS, "fonts")
ASSET_DIR = os.path.join(DS, "assets")

W, H = 1080, 1350

C = {
    "violeta": "#50235A",
    "naranja": "#FF5000",
    "aqua": "#2BAFA4",
    "aqua_claro": "#9DEDE3",
    "negro": "#1A1A1A",
    "blanco": "#FFFFFF",
    "fondo": "#FAF8F5",
    "gris": "#C9C2BC",
    "gris_claro": "#D9D3CC",
}

FONT_FILES = {
    "futura": "FuturaStd-CondensedExtraBd.otf",
    "gotham": "GothamNarrow-Medium.otf",
    "lyon": "LyonDisplay-Regular.otf",
    "lyontext": "Lyon_Text-Regular.otf",
}
FAMILY = {
    "futura": "MotionFutura",
    "gotham": "MotionGotham",
    "lyon": "MotionLyon",
    "lyontext": "MotionLyonText",
}

# ---------------------------------------------------------------- tipografia


@functools.lru_cache(maxsize=None)
def _font(key: str) -> TTFont:
    return TTFont(os.path.join(FONT_DIR, FONT_FILES[key]), fontNumber=0)


@functools.lru_cache(maxsize=None)
def _metrics(key: str):
    f = _font(key)
    return f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm, f["hhea"].ascent


def text_width(txt: str, key: str, size: float, tracking: float = 0.0) -> float:
    """Ancho en px. Se renderiza con font-kerning:none, asi que la suma de
    advances es exacta respecto de lo que dibuja el rasterizador."""
    cmap, hmtx, upem, _ = _metrics(key)
    total = 0
    for ch in txt:
        gn = cmap.get(ord(ch))
        if gn is None:
            gn = cmap.get(ord(" "))
        total += hmtx[gn][0]
    return total / upem * size + tracking * len(txt)


def ascent(key: str, size: float) -> float:
    _, _, upem, asc = _metrics(key)
    return asc / upem * size


def wrap(txt: str, key: str, size: float, max_w: float, tracking: float = 0.0):
    """Corta el texto en lineas que caben en max_w. Respeta saltos explicitos."""
    out = []
    for para in txt.split("\n"):
        words = para.split(" ")
        line = ""
        for wd in words:
            probe = wd if not line else line + " " + wd
            if text_width(probe, key, size, tracking) <= max_w or not line:
                line = probe
            else:
                out.append(line)
                line = wd
        out.append(line)
    return out


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def texto(x, y, txt, key="gotham", size=20, color=C["negro"], anchor="start",
          tracking=0.0, opacity=1.0):
    """Un <text> con baseline en y."""
    a = {"start": "start", "middle": "middle", "end": "end"}[anchor]
    ls = f' letter-spacing="{tracking}"' if tracking else ""
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY[key]}" '
            f'font-size="{size:.1f}" fill="{color}" text-anchor="{a}"{ls}{op}>'
            f'{esc(txt)}</text>')


def bloque(x, y_top, lines, key, size, line_h, color, anchor="start"):
    """Bloque de lineas ya cortadas. Devuelve (svg, y_bottom)."""
    out = []
    base = y_top + size * 0.78
    for i, ln in enumerate(lines):
        out.append(texto(x, base + i * line_h, ln, key, size, color, anchor))
    return "".join(out), y_top + (len(lines) - 1) * line_h + size * 1.02


# ---------------------------------------------------------------- geometria


def path(d, color, w=3.0, dash=None, fill="none", cap="round", opacity=1.0):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="{cap}" stroke-linejoin="round"{da}{op}/>')


def catmull(pts, tension=1.0):
    """Path suave (bezier) que pasa por todos los puntos."""
    if len(pts) < 2:
        return ""
    if len(pts) == 2:
        return f"M{pts[0][0]:.1f},{pts[0][1]:.1f} L{pts[1][0]:.1f},{pts[1][1]:.1f}"
    p = [pts[0]] + list(pts) + [pts[-1]]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d += (f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} "
              f"{p2[0]:.1f},{p2[1]:.1f}")
    return d


def curva(pts, color=C["violeta"], w=3.0, dash=None, tension=1.0, opacity=1.0):
    return path(catmull(pts, tension), color, w, dash, opacity=opacity)


def arco(cx, cy, r, a0, a1, color, w=3.0, dash=None):
    """Arco de circunferencia entre angulos en grados (0 = este, horario)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    d = f"M{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 {large} {sweep} {x1:.1f},{y1:.1f}"
    return path(d, color, w, dash)


DOT = "0.1 9"  # dasharray de linea punteada


# ---------------------------------------------------------------- iconos
# Todos los iconos se dibujan en una caja -20..20 y se escalan con s = r/26.


def _ico(inner, x, y, s, color=C["blanco"], w=2.6):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" '
            f'fill="none" stroke="{color}" stroke-width="{w / s:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</g>')


def icono(nombre, x, y, s, color=C["blanco"], w=2.6):
    if nombre == "ojo":
        inner = ('<path d="M-17,0 Q0,-12 17,0 Q0,12 -17,0 Z"/>'
                 '<circle cx="0" cy="0" r="4.6"/>')
    elif nombre == "cubo":
        pts = [(15 * math.cos(math.radians(a)), 15 * math.sin(math.radians(a)))
               for a in (30, 90, 150, 210, 270, 330)]
        poly = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        inner = (f'<polygon points="{poly}"/>'
                 '<path d="M0,0 L0,15 M0,0 L-13,-7.5 M0,0 L13,-7.5"/>')
    elif nombre == "calendario":
        inner = ('<rect x="-15" y="-13" width="30" height="26" rx="2.5"/>'
                 '<path d="M-15,-5 L15,-5 M-8,-18 L-8,-11 M8,-18 L8,-11"/>')
    elif nombre == "personas":
        inner = ('<circle cx="0" cy="-8" r="5"/>'
                 '<path d="M-8,4 Q0,-4 8,4"/>'
                 '<circle cx="-13" cy="-3" r="4"/><path d="M-19,7 Q-13,1 -7,7"/>'
                 '<circle cx="13" cy="-3" r="4"/><path d="M7,7 Q13,1 19,7"/>')
    elif nombre == "expansion":
        inner = ""
        for a in (45, 135, 225, 315):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            x0, y0 = 5 * ca, 5 * sa
            x1, y1 = 16 * ca, 16 * sa
            hx, hy = -5 * ca, -5 * sa
            px, py = -sa * 4, ca * 4
            inner += (f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f} '
                      f'M{x1:.1f},{y1:.1f} l{hx + px:.1f},{hy + py:.1f} '
                      f'M{x1:.1f},{y1:.1f} l{hx - px:.1f},{hy - py:.1f}"/>')
    elif nombre == "estrella":
        pts = []
        for i in range(10):
            ang = math.radians(-90 + i * 36)
            r = 17 if i % 2 == 0 else 7.4
            pts.append((r * math.cos(ang), r * math.sin(ang)))
        poly = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        inner = f'<polygon points="{poly}"/>'
    elif nombre == "grafico":
        inner = ('<path d="M-16,12 L16,12 M-16,12 L-16,-12"/>'
                 '<path d="M-10,8 L-10,-2 M-2,8 L-2,-8 M6,8 L6,2 M14,8 L14,-10"/>')
    elif nombre == "interrogacion":
        inner = ('<path d="M-6,-6 Q-6,-13 0,-13 Q7,-13 7,-6 Q7,-1 0,2 L0,6"/>'
                 '<path d="M0,12 L0,12.5"/>')
    else:
        raise ValueError(f"icono desconocido: {nombre}")
    return _ico(inner, x, y, s, color, w)


# ---------------------------------------------------------------- primitivas


def nodo(x, y, r=13, color=C["violeta"], icono_nombre=None, icono_color=C["blanco"],
         relleno=True):
    """Bolita del sistema. Opcionalmente con un icono lineal adentro."""
    if relleno:
        s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}"/>'
    else:
        s = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{C["fondo"]}" '
             f'stroke="{color}" stroke-width="3"/>')
    if icono_nombre:
        s += icono(icono_nombre, x, y, r / 26.0, icono_color, 2.6)
    return s


def rotulo(x, y, txt, color=C["violeta"], anchor="middle", size=22):
    """Rotulo de esquema: Gotham Narrow, uppercase, tracking amplio."""
    return texto(x, y, txt.upper(), "gotham", size, color, anchor, tracking=1.4)


def rotulo_w(txt, size=22):
    return text_width(txt.upper(), "gotham", size, 1.4)


def rotulo_multi(cx, cy, txt, color=C["violeta"], max_w=220, size=22, anchor="middle"):
    """Rotulo de varias lineas centrado verticalmente en cy."""
    lines = wrap(txt.upper(), "gotham", size, max_w, 1.4)
    lh = size * 1.35
    y0 = cy - (len(lines) - 1) * lh / 2 + size * 0.35
    return "".join(rotulo(cx, y0 + i * lh, ln, color, anchor, size)
                   for i, ln in enumerate(lines))


def trayectoria(x0, y0, x1, y1, nodos, dash=None, color=None, w=3.0,
                labels_side=None, r=13, label_size=22):
    """Curva ascendente entre (x0,y0) y (x1,y1) con nodos intermedios.

    nodos: lista de dicts {color, label, side?}. El primero se ubica en el
    origen y el ultimo en el destino.
    """
    n = len(nodos)
    pts = []
    for i in range(n):
        t = i / (n - 1)
        px = x0 + (x1 - x0) * t
        # curva con easing: sube despacio y despues acelera
        py = y0 + (y1 - y0) * (t ** 1.55 * 0.55 + t * 0.45)
        pts.append((px, py))
    linea_color = color or C["violeta"]
    out = [curva(pts, linea_color, w, dash)]
    for i, nd in enumerate(nodos):
        px, py = pts[i]
        out.append(nodo(px, py, nd.get("r", r), nd.get("color", C["violeta"])))
        lab = nd.get("label")
        if lab:
            side = nd.get("side") or (labels_side[i] if labels_side else "abajo")
            out.append(rotulo_pos(px, py, lab, nd.get("color", C["violeta"]),
                                  side, nd.get("r", r), label_size))
    return "".join(out), pts


def rotulo_pos(px, py, lab, color, side, r=13, size=22):
    """Coloca un rotulo respecto de un nodo sin pisarlo."""
    if side == "abajo":
        return rotulo(px, py + r + size + 8, lab, color, "middle", size)
    if side == "abajo2":
        return rotulo(px, py + r + size + 42, lab, color, "middle", size)
    if side == "arriba":
        return rotulo(px, py - r - 14, lab, color, "middle", size)
    if side == "izq":
        return rotulo(px - r - 12, py + size * 0.35, lab, color, "end", size)
    if side == "der":
        return rotulo(px + r + 12, py + size * 0.35, lab, color, "start", size)
    if side == "abajo_izq":
        return rotulo(px - r - 6, py + r + size + 6, lab, color, "end", size)
    if side == "abajo_der":
        return rotulo(px + r + 6, py + r + size + 6, lab, color, "start", size)
    if side == "arriba_der":
        return rotulo(px + r + 6, py - r - 12, lab, color, "start", size)
    if side == "arriba_izq":
        return rotulo(px - r - 6, py - r - 12, lab, color, "end", size)
    raise ValueError(side)


def anillos(cx, cy, radios, colores, span=280, rot=None, w=3.5,
            centro_color=None, centro_r=0, centro_label=None,
            leyenda=None, leyenda_x=None, leyenda_y=None, label_size=22):
    """Anillos concentricos incompletos (capas).

    radios/colores: de adentro hacia afuera. `leyenda`: lista de (texto, color)
    dibujada como nodo + linea corta + rotulo, a la derecha del esquema.
    """
    out = []
    for i, (rad, col) in enumerate(zip(radios, colores)):
        a0 = (rot[i] if rot else -90 + i * 26) - span / 2
        out.append(arco(cx, cy, rad, a0, a0 + span, col, w))
    if centro_r:
        out.append(nodo(cx, cy, centro_r, centro_color or C["naranja"]))
    if centro_label:
        out.append(rotulo(cx, cy + label_size * 0.36, centro_label,
                          centro_color or C["violeta"], "middle", label_size))
    if leyenda:
        lx = leyenda_x if leyenda_x is not None else cx + max(radios) + 62
        ly = leyenda_y if leyenda_y is not None else cy - (len(leyenda) - 1) * 19
        for i, (txt, col) in enumerate(leyenda):
            y = ly + i * 38
            out.append(nodo(lx, y, 8, col))
            out.append(path(f"M{lx + 14:.1f},{y:.1f} L{lx + 30:.1f},{y:.1f}", col, 2.5))
            out.append(rotulo(lx + 38, y + label_size * 0.35, txt, col, "start", label_size))
    return "".join(out)


def orbita(cx, cy, rx, ry, color=C["violeta"], centro_color=C["violeta"],
           satelite_ang=-40, satelite_color=C["naranja"], label_centro=None,
           label_satelite=None, label_size=22, dash=None):
    """Circulo/elipse con nodo al centro y un nodo sobre la orbita."""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    out = [f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
           f'fill="none" stroke="{color}" stroke-width="3"{da}/>']
    out.append(nodo(cx, cy, 15, centro_color))
    sx = cx + rx * math.cos(math.radians(satelite_ang))
    sy = cy + ry * math.sin(math.radians(satelite_ang))
    out.append(nodo(sx, sy, 13, satelite_color))
    if label_centro:
        out.append(rotulo(cx, cy + ry + 40, label_centro, centro_color, "middle", label_size))
    if label_satelite:
        out.append(rotulo(sx + 22, sy - 18, label_satelite, satelite_color, "start", label_size))
    return "".join(out)


def radial(cx, cy, r_core=22, r_spoke=118, n=8, core_color=C["violeta"],
           spoke_color=C["aqua"], nodo_r=13, label=None, label_size=22,
           ang0=-90):
    """Topologia radial: nucleo + n radios cortos terminados en nodos."""
    out = []
    for i in range(n):
        a = math.radians(ang0 + i * 360 / n)
        x0, y0 = cx + (r_core + 8) * math.cos(a), cy + (r_core + 8) * math.sin(a)
        x1, y1 = cx + r_spoke * math.cos(a), cy + r_spoke * math.sin(a)
        out.append(path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", spoke_color, 3))
        out.append(nodo(x1, y1, nodo_r, spoke_color))
    out.append(nodo(cx, cy, r_core, core_color))
    if label:
        out.append(rotulo(cx, cy + r_spoke + nodo_r + 40, label, core_color,
                          "middle", label_size))
    return "".join(out)


def contenedor(x, y, w_, h_, color=C["violeta"], label=None, mini="grafico",
               label_size=22, label_pos="abajo", label_color=None, mini_color=None):
    """Rectangulo de borde fino con un mini-grafico adentro y rotulo debajo."""
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h_:.1f}" '
           f'rx="6" fill="none" stroke="{color}" stroke-width="3"/>']
    if mini:
        s = min(w_, h_) / 88.0
        out.append(icono(mini, x + w_ / 2, y + h_ / 2, s, mini_color or color, 2.6))
    if label:
        lc = label_color or color
        if label_pos == "abajo":
            out.append(rotulo(x + w_ / 2, y + h_ + label_size + 12, label, lc,
                              "middle", label_size))
        else:
            out.append(rotulo(x + w_ / 2, y - 14, label, lc, "middle", label_size))
    return "".join(out)


def convergencia(x0, x_hub, y_hub, entradas, salida, y_span=180, w=3.0,
                 label_size=22, hub_color=None, hub_label=None,
                 salida_dx=170, salida_dy=-130):
    """Varias lineas de distinto color que confluyen en un unico nodo y salen
    como una sola linea hacia un nodo final.

    entradas: [{label, color, dash?}]; salida: {label, color}.
    """
    out = []
    n = len(entradas)
    for i, e in enumerate(entradas):
        y = y_hub - y_span / 2 + (y_span / (n - 1)) * i if n > 1 else y_hub
        col = e.get("color", C["violeta"])
        out.append(curva([(x0, y), (x0 + (x_hub - x0) * 0.55, y),
                          (x_hub, y_hub)], col, w, e.get("dash")))
        if e.get("label"):
            out.append(rotulo(x0, y - 16, e["label"], col, "start", label_size))
        out.append(nodo(x0, y, 9, col))
    hc = hub_color or C["violeta"]
    sx, sy = x_hub + salida_dx, y_hub + salida_dy
    out.append(curva([(x_hub, y_hub),
                      (x_hub + salida_dx * 0.45, y_hub + salida_dy * 0.28),
                      (sx, sy)], salida.get("color", C["naranja"]), w))
    out.append(nodo(x_hub, y_hub, 17, hc))
    if hub_label:
        out.append(rotulo(x_hub, y_hub + 46, hub_label, hc, "middle", label_size))
    out.append(nodo(sx, sy, 15, salida.get("color", C["naranja"])))
    if salida.get("label"):
        out.append(rotulo(sx, sy - 30, salida["label"], salida.get("color", C["naranja"]),
                          "middle", label_size))
    return "".join(out)


def anillo_programa(cx, cy, r_ext=190, r_int=104, label_size=22,
                    nucleo="PROGRAMA DE TRANSFORMACIÓN DIGITAL",
                    sectores=("NEGOCIO", "TECNOLOGÍA", "CULTURA")):
    """Patron canonico: disco naranja + nucleo aqua + 3 sectores iguales."""
    out = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_ext:.1f}" fill="{C["naranja"]}"/>']
    # separadores de sector
    for k in range(3):
        a = math.radians(-90 + k * 120)
        x0, y0 = cx + r_int * math.cos(a), cy + r_int * math.sin(a)
        x1, y1 = cx + r_ext * math.cos(a), cy + r_ext * math.sin(a)
        out.append(path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", C["fondo"], 4, cap="butt"))
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_int:.1f}" fill="{C["aqua_claro"]}"/>')
    # rotulos de sector, horizontales, en el centroide angular de cada sector
    rm = (r_int + r_ext) / 2
    for k, nombre in enumerate(sectores):
        a = math.radians(-90 + 60 + k * 120)
        x, y = rm * math.cos(a), rm * math.sin(a)
        # el rotulo se ajusta hasta que su caja entra completa en la corona
        ls = label_size - 2
        while ls > 13:
            hw = text_width(nombre.upper(), "gotham", ls, 1.4) / 2
            hh = ls * 0.42
            radios = [math.hypot(x + sx * hw, y + sy * hh)
                      for sx in (-1, 1) for sy in (-1, 1)]
            if min(radios) >= r_int + 9 and max(radios) <= r_ext - 9:
                break
            ls -= 1
        out.append(rotulo(cx + x, cy + y + ls * 0.35, nombre, C["blanco"], "middle", ls))
    # nucleo: se ajusta el cuerpo hasta que la palabra mas larga entre
    size = 32
    palabras = nucleo.upper().split(" ")
    while size > 16 and max(text_width(p_, "futura", size) for p_ in palabras) > r_int * 1.46:
        size -= 1
    lines = wrap(nucleo.upper(), "futura", size, r_int * 1.5)
    lh = size * 1.04
    y0 = cy - (len(lines) - 1) * lh / 2 + size * 0.34
    for i, ln in enumerate(lines):
        out.append(texto(cx, y0 + i * lh, ln, "futura", size, C["violeta"], "middle"))
    return "".join(out)


def onda_inflexion(x0, x1, y_base, amp=70, color=C["violeta"], marca_color=C["naranja"],
                   label=None, label_size=22, w=3.5, marca_r=34):
    """Curva que sube, baja y vuelve a subir; circulo naranja en la inflexion."""
    xs = [x0, x0 + (x1 - x0) * 0.22, x0 + (x1 - x0) * 0.46,
          x0 + (x1 - x0) * 0.70, x1]
    ys = [y_base, y_base - amp, y_base + amp * 0.35, y_base - amp * 0.35,
          y_base - amp * 1.5]
    pts = list(zip(xs, ys))
    out = [curva(pts, color, w)]
    mx, my = pts[2]
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{marca_r:.1f}" fill="none" '
               f'stroke="{marca_color}" stroke-width="3"/>')
    out.append(nodo(pts[0][0], pts[0][1], 11, color))
    out.append(nodo(pts[-1][0], pts[-1][1], 13, color))
    if label:
        out.append(rotulo(mx, my + marca_r + label_size + 12, label, marca_color,
                          "middle", label_size))
    return "".join(out), pts


def diana(cx, cy, radios=(46, 92, 138), color=C["violeta"], nodo_color=C["naranja"],
          nodo_ang=-35, nodo_r_pos=52, label=None, label_size=22):
    """Circulos concentricos con un nodo acercandose al centro."""
    out = []
    for i, r in enumerate(radios):
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
                   f'stroke="{color}" stroke-width="{3 if i else 3}" '
                   f'opacity="{1 - i * 0.22:.2f}"/>')
    out.append(nodo(cx, cy, 9, color))
    a = math.radians(nodo_ang)
    nx, ny = cx + nodo_r_pos * math.cos(a), cy + nodo_r_pos * math.sin(a)
    x_out = cx + (max(radios) + 66) * math.cos(a)
    y_out = cy + (max(radios) + 66) * math.sin(a)
    out.append(curva([(x_out, y_out), (nx, ny)], nodo_color, 3, DOT))
    out.append(nodo(nx, ny, 14, nodo_color))
    if label:
        out.append(rotulo(cx, cy + max(radios) + label_size + 26, label, nodo_color,
                          "middle", label_size))
    return "".join(out)


def linea_base_punteada(x0, x1, y, amp=13, ciclos=3.0, color=C["gris"], w=2.6):
    """Onda punteada horizontal que da continuidad de serie al pie del esquema."""
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps
        pts.append((x0 + (x1 - x0) * t, y + amp * math.sin(t * ciclos * 2 * math.pi)))
    return path(catmull(pts), color, w, dash="0.1 9")


# ---------------------------------------------------------------- marca


@functools.lru_cache(maxsize=None)
def _b64_asset(name):
    with open(os.path.join(ASSET_DIR, name), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


LOGO_W, LOGO_H = 450, 109


def firma(x_der=984, y_centro=1252, logo="logo-negro.png", ancho=152,
          color_texto=C["negro"], descriptor=("Lo complejo,", "simple.")):
    """Logo MOTION + separador vertical fino + descriptor en dos lineas."""
    lw = ancho
    lh = ancho * LOGO_H / LOGO_W
    size = 21
    tw = max(text_width(descriptor[0], "gotham", size),
             text_width(descriptor[1], "gotham", size))
    gap = 20
    total = lw + gap + 1 + gap + tw
    x0 = x_der - total
    out = [f'<image x="{x0:.1f}" y="{y_centro - lh / 2:.1f}" width="{lw:.1f}" '
           f'height="{lh:.1f}" href="data:image/png;base64,{_b64_asset(logo)}"/>']
    xs = x0 + lw + gap
    out.append(path(f"M{xs:.1f},{y_centro - 24:.1f} L{xs:.1f},{y_centro + 24:.1f}",
                    color_texto, 1.4, cap="butt", opacity=0.55))
    xt = xs + gap
    out.append(texto(xt, y_centro - 4, descriptor[0], "gotham", size, color_texto))
    out.append(texto(xt, y_centro + 21, descriptor[1], "gotham", size, color_texto))
    return "".join(out)


def pager(n, x=112, y=118, r=27, color=C["naranja"], texto_color=C["blanco"], size=25):
    """Marcador de paginacion: circulo relleno naranja con el numero adentro."""
    return (nodo(x, y, r, color)
            + texto(x, y + size * 0.35, str(n), "gotham", size, texto_color, "middle"))


# ---------------------------------------------------------------- documento


def _subset_b64(key, chars):
    """Subsetea la OTF a los caracteres usados y la devuelve en base64."""
    if not chars:
        return None
    src = os.path.join(FONT_DIR, FONT_FILES[key])
    opts = subset.Options()
    opts.layout_features = ["*"]
    opts.notdef_outline = True
    opts.desubroutinize = True
    font = subset.load_font(src, opts)
    subsetter = subset.Subsetter(options=opts)
    subsetter.populate(text="".join(sorted(chars)))
    subsetter.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, opts)
    font.close()
    return base64.b64encode(buf.getvalue()).decode()


_RE_TEXT = None


def chars_usados(svg: str):
    """Extrae, por fuente, el set de caracteres realmente dibujados en el SVG."""
    import re
    global _RE_TEXT
    if _RE_TEXT is None:
        _RE_TEXT = re.compile(r'font-family="([^"]+)"[^>]*>([^<]*)<')
    inv = {v: k for k, v in FAMILY.items()}
    out = {}
    for fam, txt in _RE_TEXT.findall(svg):
        key = inv.get(fam)
        if not key:
            continue
        txt = (txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
        out.setdefault(key, set()).update(txt)
    return out


def documento(cuerpo, chars_por_fuente, w=W, h=H, fondo=C["fondo"]):
    """Envuelve los fragmentos en un SVG autocontenido con las OTF embebidas."""
    faces = []
    for key, chars in chars_por_fuente.items():
        b64 = _subset_b64(key, chars)
        if not b64:
            continue
        faces.append(f"@font-face{{font-family:'{FAMILY[key]}';"
                     f"src:url(data:font/otf;base64,{b64}) format('opentype');"
                     "font-weight:normal;font-style:normal}")
    css = ("".join(faces) +
           "text{font-kerning:none;font-variant-ligatures:none;"
           "white-space:pre;paint-order:stroke fill}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">'
            f'<defs><style type="text/css">{css}</style></defs>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{fondo}"/>'
            f'{cuerpo}</svg>')
