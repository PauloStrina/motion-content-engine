#!/usr/bin/env python3
"""MOTION render parametrico — lee un JSON de slides y produce el PDF del carrusel.
Uso: python render.py slides/episodio.json salida.pdf      (PDF)
     python render.py slides/episodio.json carpeta --png   (PNG por slide)
Kit fijo: eco vertical · degradé laminado 10px monocolor · contraste serif Lyon."""
import base64, json, os, sys
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
C = {'negro':'#1A1A1A','naranja':'#FF5000','violeta':'#50235A','aqua':'#9DEDE3','blanco':'#FFFFFF'}
SHADOW_FOR_BG = {'negro':'aqua','violeta':'aqua','naranja':'violeta','aqua':'violeta','blanco':'violeta'}
LOGO_FOR_BG  = {'negro':'blanco','violeta':'blanco','naranja':'blanco','aqua':'negro','blanco':'negro'}

def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
LOGO = {c: b64(f'{BASE}/assets/logo-{c}.png') for c in ['blanco','negro','naranja','aqua','violeta']}

def hex2rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def rgb2hex(r): return '#%02X%02X%02X' % tuple(int(x) for x in r)
def mix(a, b, t):
    A, B = hex2rgb(a), hex2rgb(b)
    return rgb2hex([A[i]+(B[i]-A[i])*t for i in range(3)])

def lam(word, size, front, shadow_hex, bg_hex, depth=10):
    # text-shadow: wraps naturally (no fixed-height container), visually equivalent
    line = int(size*1.06)
    shadows = [f'{i}px {i}px 0 {mix(shadow_hex, bg_hex, i/depth*0.85)}' for i in range(1, depth+1)]
    return f'<div class="futura" style="font-size:{size}px;line-height:{line}px;color:{front};text-shadow:{", ".join(shadows)}">{word}</div>'

def eco(word, size, color, n=3):
    ops = [1.0, 0.45, 0.16][:n]
    return ''.join(f'<div class="futura" style="font-size:{size}px;line-height:{int(size*0.88)}px;color:{color};opacity:{o}">{word}</div>' for o in ops)

def block_html(b, bg_hex):
    t = b['type']; col = C.get(b.get('color',''), b.get('color','#FFF'))
    size = b.get('size', 60)
    if t == 'futura':
        lh = b.get('lh', int(size*0.98))
        return f'<div class="futura" style="font-size:{size}px;line-height:{lh}px;color:{col};margin-bottom:{b.get("mb",0)}px">{b["text"]}</div>'
    if t == 'lyon':
        return f'<div class="lyon" style="font-size:{size}px;line-height:{b.get("lh2",1.25)};color:{col};margin-bottom:{b.get("mb",0)}px;max-width:{b.get("maxw",912)}px">{b["text"]}</div>'
    if t == 'lyont':
        return f'<div class="lyont" style="font-size:{size}px;line-height:1.4;color:{col};margin-top:{b.get("mt",0)}px">{b["text"]}</div>'
    if t == 'eco':
        return eco(b['text'], size, col, b.get('n',3))
    if t == 'lam':
        shadow = C[b.get('shadow') or SHADOW_FOR_BG[b['_bgname']]]
        return lam(b['text'], size, col, shadow, bg_hex, b.get('depth',10))
    if t == 'spacer':
        return f'<div style="height:{b.get("h",40)}px"></div>'
    if t == 'rows':
        rows = ''
        for op in b.get('ops',[1.0,0.55,0.25]):
            rows += f'<div style="opacity:{op};margin-bottom:{b.get("gap",18)}px">{b["html"]}</div>'
        return rows
    return ''

def slide_html(s, is_portada=False):
    bgname = s.get('bg','negro'); bg = C[bgname]
    logoname = s.get('logo') or LOGO_FOR_BG[bgname]
    logo = LOGO[logoname]
    ebc = C.get(s.get('eyebrow_color',''), s.get('eyebrow_color','#888'))
    blocks = ''
    for b in s.get('blocks', []):
        b['_bgname'] = bgname
        blocks += block_html(b, bg)
    # foot: frase en esquina inferior izquierda, 2 líneas, mismo color que el logo,
    # alto total = alto del logo (≈46px @ width 190px). Usar <br> para forzar 2 líneas.
    if s.get('foot'):
        foottext = s['foot']
    elif is_portada:
        foottext = '#HistoriasEnMovimiento:<br>casos reales del día a día Motion.'
    else:
        foottext = ''
    foot = f'<div class="foot" style="color:{C[logoname]}">{foottext}</div>' if foottext else ''
    eb = ''
    return f'''<div class="slide" style="background:{bg}">
      {eb}<div class="pager" style="color:{ebc}">{s.get('pager','')}</div>
      <div class="mid">{blocks}</div>{foot}
      <img class="logo" src="data:image/png;base64,{logo}"></div>'''

def render(spec_path, out_path):
    spec = json.load(open(spec_path))
    body = ''.join(slide_html(s, i==0) for i, s in enumerate(spec['slides']))
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'FuturaM'; src: url('file://{BASE}/fonts/FuturaStd-CondensedExtraBd.otf') format('opentype'); }}
@font-face {{ font-family:'GothamM'; src: url('file://{BASE}/fonts/GothamNarrow-Medium.otf') format('opentype'); }}
@font-face {{ font-family:'LyonD'; src: url('file://{BASE}/fonts/LyonDisplay-Regular.otf') format('opentype'); }}
@font-face {{ font-family:'LyonT'; src: url('file://{BASE}/fonts/Lyon_Text-Regular.otf') format('opentype'); }}
@page {{ size:1080px 1350px; margin:0; }} * {{ margin:0; padding:0; box-sizing:border-box; }}
.slide {{ width:1080px; height:1350px; position:relative; overflow:hidden; padding:90px 84px; }}
.futura {{ font-family:'FuturaM'; text-transform:uppercase; }}
.lyon {{ font-family:'LyonD'; }} .lyont {{ font-family:'LyonT'; }}
.eyebrow {{ font-family:'GothamM'; font-size:25px; letter-spacing:5px; text-transform:uppercase; position:absolute; top:96px; left:84px; }}
.pager {{ position:absolute; top:96px; right:84px; font-family:'GothamM'; font-size:24px; letter-spacing:3px; }}
.logo {{ position:absolute; bottom:64px; right:84px; width:190px; }}
.foot {{ position:absolute; bottom:64px; left:84px; height:46px; font-family:'GothamM'; font-size:21px; line-height:23px; display:flex; flex-direction:column; justify-content:center; }}
.mid {{ position:absolute; top:150px; left:84px; width:912px; bottom:140px; display:flex; flex-direction:column; justify-content:center; overflow:hidden; }}
.futura {{ font-family:'FuturaM'; text-transform:uppercase; max-width:912px; word-break:break-word; }}
</style></head><body>{body}</body></html>'''
    HTML(string=html).write_pdf(out_path)
    print(f"OK: {out_path}")

def render_pngs(spec_path, out_dir):
    """Exporta cada slide como PNG individual (para Instagram/carrusel de imagenes)."""
    import subprocess
    os.makedirs(out_dir, exist_ok=True)
    tmp_pdf = "/tmp/_render_tmp.pdf"
    render(spec_path, tmp_pdf)
    base = os.path.splitext(os.path.basename(spec_path))[0]
    subprocess.run(["pdftoppm","-png","-r","96",tmp_pdf, os.path.join(out_dir, base)], check=True)
    os.remove(tmp_pdf)
    pngs = sorted([f for f in os.listdir(out_dir) if f.startswith(base) and f.endswith(".png")])
    print(f"OK: {len(pngs)} PNGs en {out_dir}/")
    return pngs

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "--png":
        render_pngs(sys.argv[1], sys.argv[2])
    else:
        render(sys.argv[1], sys.argv[2])
