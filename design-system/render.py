#!/usr/bin/env python3
"""MOTION render paramétrico.

Lee un JSON de slides y produce PDF o PNG. Conserva el sistema tipográfico
existente y añade capas gráficas absolutas para diagramas, geometrías e
imágenes conceptuales aprobadas.
"""
from __future__ import annotations

import base64
import html
import json
import math
import os
import sys
from pathlib import Path

from weasyprint import HTML

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent.resolve()
C = {
    "negro": "#1A1A1A",
    "naranja": "#FF5000",
    "violeta": "#50235A",
    "aqua": "#9DEDE3",
    "blanco": "#FFFFFF",
}
SHADOW_FOR_BG = {
    "negro": "aqua",
    "violeta": "aqua",
    "naranja": "violeta",
    "aqua": "violeta",
    "blanco": "violeta",
}
LOGO_FOR_BG = {
    "negro": "blanco",
    "violeta": "blanco",
    "naranja": "blanco",
    "aqua": "negro",
    "blanco": "negro",
}


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


LOGO = {
    color_name: b64(BASE / "assets" / f"logo-{color_name}.png")
    for color_name in ["blanco", "negro", "naranja", "aqua", "violeta"]
}


def color(value: str | None, fallback: str = "#FFFFFF") -> str:
    if not value:
        return fallback
    return C.get(value, value)


def css_num(value, default=0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def hex2rgb(value: str):
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))


def rgb2hex(values):
    return "#%02X%02X%02X" % tuple(int(x) for x in values)


def mix(a: str, b: str, t: float) -> str:
    first, second = hex2rgb(a), hex2rgb(b)
    return rgb2hex([first[i] + (second[i] - first[i]) * t for i in range(3)])


def lam(word, size, front, shadow_hex, bg_hex, depth=10):
    line = int(size * 1.06)
    shadows = [
        f"{i}px {i}px 0 {mix(shadow_hex, bg_hex, i / depth * 0.85)}"
        for i in range(1, depth + 1)
    ]
    return (
        f'<div class="futura" style="font-size:{size}px;line-height:{line}px;'
        f'color:{front};text-shadow:{", ".join(shadows)}">{word}</div>'
    )


def eco(word, size, text_color, n=3):
    ops = [1.0, 0.45, 0.16][:n]
    return "".join(
        f'<div class="futura" style="font-size:{size}px;line-height:{int(size * 0.88)}px;'
        f'color:{text_color};opacity:{opacity}">{word}</div>'
        for opacity in ops
    )


def block_html(block, bg_hex):
    block_type = block["type"]
    text_color = color(block.get("color"), "#FFFFFF")
    size = block.get("size", 60)
    if block_type == "futura":
        line_height = block.get("lh", int(size * 0.98))
        return (
            f'<div class="futura" style="font-size:{size}px;line-height:{line_height}px;'
            f'color:{text_color};margin-bottom:{block.get("mb", 0)}px">{block["text"]}</div>'
        )
    if block_type == "lyon":
        return (
            f'<div class="lyon" style="font-size:{size}px;line-height:{block.get("lh2", 1.25)};'
            f'color:{text_color};margin-bottom:{block.get("mb", 0)}px;'
            f'max-width:{block.get("maxw", 912)}px">{block["text"]}</div>'
        )
    if block_type == "lyont":
        return (
            f'<div class="lyont" style="font-size:{size}px;line-height:1.4;'
            f'color:{text_color};margin-top:{block.get("mt", 0)}px">{block["text"]}</div>'
        )
    if block_type == "eco":
        return eco(block["text"], size, text_color, block.get("n", 3))
    if block_type == "lam":
        shadow = color(block.get("shadow") or SHADOW_FOR_BG[block["_bgname"]])
        return lam(block["text"], size, text_color, shadow, bg_hex, block.get("depth", 10))
    if block_type == "spacer":
        return f'<div style="height:{block.get("h", 40)}px"></div>'
    if block_type == "rows":
        rows = ""
        for opacity in block.get("ops", [1.0, 0.55, 0.25]):
            rows += (
                f'<div style="opacity:{opacity};margin-bottom:{block.get("gap", 18)}px">'
                f'{block["html"]}</div>'
            )
        return rows
    return ""


def _style_position(layer):
    return (
        f'position:absolute;left:{css_num(layer.get("x"))}px;top:{css_num(layer.get("y"))}px;'
        f'z-index:{int(css_num(layer.get("z"), 1))};opacity:{css_num(layer.get("opacity"), 1)};'
        f'transform-origin:center center;'
    )


def _asset_data_uri(raw_path: str) -> str:
    path = (REPO_ROOT / raw_path).resolve()
    try:
        path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(f"Asset fuera del repositorio: {raw_path}") from exc
    if not path.exists():
        raise FileNotFoundError(f"No existe el asset: {raw_path}")
    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(suffix)
    if not mime:
        raise ValueError(f"Formato de imagen no soportado: {raw_path}")
    return f"data:{mime};base64,{b64(path)}"


def layer_html(layer):
    kind = layer.get("type")
    base = _style_position(layer)
    rotate = css_num(layer.get("rotate"), 0)
    transform = f"transform:rotate({rotate}deg);"
    width = css_num(layer.get("w"), 100)
    height = css_num(layer.get("h"), width)
    fill = color(layer.get("fill"), "transparent")
    stroke = color(layer.get("stroke"), "transparent")
    stroke_width = css_num(layer.get("stroke_width"), 0)

    if kind in {"circle", "ellipse", "rect"}:
        radius = "50%" if kind in {"circle", "ellipse"} else f'{css_num(layer.get("radius"), 0)}px'
        shadow = html.escape(str(layer.get("shadow", "none")))
        return (
            f'<div style="{base}{transform}width:{width}px;height:{height}px;'
            f'background:{fill};border:{stroke_width}px solid {stroke};'
            f'border-radius:{radius};box-shadow:{shadow};"></div>'
        )

    if kind == "line":
        x1 = css_num(layer.get("x1"))
        y1 = css_num(layer.get("y1"))
        x2 = css_num(layer.get("x2"))
        y2 = css_num(layer.get("y2"))
        length = math.hypot(x2 - x1, y2 - y1)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        border_style = "dashed" if layer.get("dash") else "solid"
        return (
            f'<div style="position:absolute;left:{x1}px;top:{y1}px;width:{length}px;'
            f'height:0;border-top:{css_num(layer.get("stroke_width"), 4)}px {border_style} '
            f'{color(layer.get("stroke"), "#1A1A1A")};transform:rotate({angle}deg);'
            f'transform-origin:0 0;z-index:{int(css_num(layer.get("z"), 1))};'
            f'opacity:{css_num(layer.get("opacity"), 1)};"></div>'
        )

    if kind == "svg_path":
        path_data = html.escape(str(layer.get("d", "")), quote=True)
        view_box = html.escape(str(layer.get("viewBox", "0 0 1080 1350")), quote=True)
        dasharray = html.escape(str(layer.get("dasharray", "")), quote=True)
        dash_attr = f' stroke-dasharray="{dasharray}"' if dasharray else ""
        return (
            f'<svg style="position:absolute;inset:0;width:1080px;height:1350px;'
            f'z-index:{int(css_num(layer.get("z"), 1))};opacity:{css_num(layer.get("opacity"), 1)};" '
            f'viewBox="{view_box}" preserveAspectRatio="none">'
            f'<path d="{path_data}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}" stroke-linecap="{layer.get("linecap", "round")}" '
            f'stroke-linejoin="{layer.get("linejoin", "round")}"{dash_attr}/></svg>'
        )

    if kind == "text":
        fonts = {
            "futura": "FuturaM",
            "gotham": "GothamM",
            "lyon": "LyonD",
            "lyont": "LyonT",
        }
        font_family = fonts.get(layer.get("font", "gotham"), "GothamM")
        text = html.escape(str(layer.get("text", ""))).replace("\n", "<br>")
        text_transform = "uppercase" if layer.get("uppercase") or layer.get("font") == "futura" else "none"
        align = layer.get("align", "left")
        line_height = css_num(layer.get("line_height"), css_num(layer.get("size"), 32) * 1.15)
        letter_spacing = css_num(layer.get("letter_spacing"), 0)
        return (
            f'<div style="{base}{transform}width:{width}px;height:{height}px;'
            f'font-family:{font_family};font-size:{css_num(layer.get("size"), 32)}px;'
            f'line-height:{line_height}px;color:{color(layer.get("color"), "#1A1A1A")};'
            f'text-align:{align};letter-spacing:{letter_spacing}px;text-transform:{text_transform};'
            f'overflow:hidden;">{text}</div>'
        )

    if kind == "image":
        src = _asset_data_uri(layer["src"])
        fit = layer.get("fit", "contain")
        radius = css_num(layer.get("radius"), 0)
        return (
            f'<img src="{src}" style="{base}{transform}width:{width}px;height:{height}px;'
            f'object-fit:{fit};border-radius:{radius}px;">'
        )

    raise ValueError(f"Tipo de layer no soportado: {kind!r}")


def mid_style(slide):
    spec = slide.get("mid", {})
    top = css_num(spec.get("top"), 150)
    bottom = css_num(spec.get("bottom"), 140)
    left = css_num(spec.get("left"), 84)
    width = css_num(spec.get("width"), 912)
    justify = spec.get("justify", "center")
    align = spec.get("align", "stretch")
    z = int(css_num(spec.get("z"), 10))
    return (
        f"top:{top}px;bottom:{bottom}px;left:{left}px;width:{width}px;"
        f"justify-content:{justify};align-items:{align};z-index:{z};"
    )


def slide_html(slide, is_portada=False):
    bgname = slide.get("bg", "negro")
    bg = color(bgname, C["negro"])
    logoname = slide.get("logo") or LOGO_FOR_BG.get(bgname, "blanco")
    logo = LOGO[logoname]
    eyebrow_color = color(slide.get("eyebrow_color"), "#888888")

    layers = "".join(layer_html(layer) for layer in slide.get("layers", []))

    blocks = ""
    for block in slide.get("blocks", []):
        block["_bgname"] = bgname
        blocks += block_html(block, bg)

    if slide.get("foot"):
        foottext = slide["foot"]
    elif is_portada:
        foottext = "#HistoriasEnMovimiento:<br>casos reales de nuestro día a día."
    else:
        foottext = ""

    foot_color = color(slide.get("foot_color"), C[logoname])
    foot = (
        f'<div class="foot" style="color:{foot_color}">{foottext}</div>'
        if foottext
        else ""
    )

    return (
        f'<div class="slide" style="background:{bg}">'
        f'{layers}<div class="pager" style="color:{eyebrow_color}">{slide.get("pager", "")}</div>'
        f'<div class="mid" style="{mid_style(slide)}">{blocks}</div>{foot}'
        f'<img class="logo" src="data:image/png;base64,{logo}"></div>'
    )


def render(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    body = "".join(slide_html(slide, index == 0) for index, slide in enumerate(spec["slides"]))
    html_doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'FuturaM'; src: url('file://{BASE}/fonts/FuturaStd-CondensedExtraBd.otf') format('opentype'); }}
@font-face {{ font-family:'GothamM'; src: url('file://{BASE}/fonts/GothamNarrow-Medium.otf') format('opentype'); }}
@font-face {{ font-family:'LyonD'; src: url('file://{BASE}/fonts/LyonDisplay-Regular.otf') format('opentype'); }}
@font-face {{ font-family:'LyonT'; src: url('file://{BASE}/fonts/Lyon_Text-Regular.otf') format('opentype'); }}
@page {{ size:1080px 1350px; margin:0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
.slide {{ width:1080px; height:1350px; position:relative; overflow:hidden; padding:90px 84px; }}
.futura {{ font-family:'FuturaM'; text-transform:uppercase; max-width:912px; word-break:break-word; }}
.lyon {{ font-family:'LyonD'; }}
.lyont {{ font-family:'LyonT'; }}
.pager {{ position:absolute; top:96px; right:84px; font-family:'GothamM'; font-size:24px; letter-spacing:3px; z-index:30; }}
.logo {{ position:absolute; bottom:64px; right:84px; width:190px; z-index:30; }}
.foot {{ position:absolute; bottom:64px; left:84px; height:46px; font-family:'GothamM'; font-size:21px; line-height:23px; display:flex; flex-direction:column; justify-content:center; z-index:30; }}
.mid {{ position:absolute; display:flex; flex-direction:column; overflow:hidden; }}
</style></head><body>{body}</body></html>'''
    HTML(string=html_doc).write_pdf(out_path)
    print(f"OK: {out_path}")


def render_pngs(spec_path, out_dir):
    import subprocess

    os.makedirs(out_dir, exist_ok=True)
    tmp_pdf = "/tmp/_render_tmp.pdf"
    render(spec_path, tmp_pdf)
    base = os.path.splitext(os.path.basename(spec_path))[0]
    subprocess.run(
        ["pdftoppm", "-png", "-r", "96", tmp_pdf, os.path.join(out_dir, base)],
        check=True,
    )
    os.remove(tmp_pdf)
    pngs = sorted(
        filename
        for filename in os.listdir(out_dir)
        if filename.startswith(base) and filename.endswith(".png")
    )
    print(f"OK: {len(pngs)} PNGs en {out_dir}/")
    return pngs


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "--png":
        render_pngs(sys.argv[1], sys.argv[2])
    else:
        render(sys.argv[1], sys.argv[2])
