#!/usr/bin/env python3
"""MOTION render de STORIES — 6 stories verticales (1080×1920) que cuentan la misma
historia del carrusel con más detalle. Estilo minimalista (una idea por pantalla,
tipografía gigante, mucho aire) inspirado en ejemplo-story, con paleta y fuentes Motion.
NO usa Chrome: WeasyPrint (HTML/CSS→PDF) + pdftoppm (PDF→PNG), igual que render.py.

Uso: python render_stories.py slides/<ep>_stories.json salida.pdf      (PDF)
     python render_stories.py slides/<ep>_stories.json carpeta --png    (PNG por story)

Formato del JSON:
{
  "episodio": "ep1-1",
  "stories": [
    {"number":1, "type":"cover",    "bg":"negro",   "text":"...", "color":"blanco"},
    {"number":2, "type":"body",     "bg":"negro",   "text":"..."},
    {"number":3, "type":"question", "bg":"violeta", "text":"..."},
    {"number":6, "type":"closing",  "bg":"negro",   "text":"..."}
  ]
}
- 6 stories. type ∈ cover|body|question|closing (define tipografía y tamaño).
- bg ∈ negro|naranja|violeta|aqua|blanco (paleta Motion; narrativa cromática del episodio).
- color opcional; si falta, se elige por contraste con el fondo.
- En text se puede usar <br> y <span class="acc">palabra</span> para resaltar en color acento.
"""
import base64, json, os, sys
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
C = {'negro':'#1A1A1A','naranja':'#FF5000','violeta':'#50235A','aqua':'#9DEDE3','blanco':'#FFFFFF'}
# color de texto y logo por contraste con el fondo
TEXT_FOR_BG  = {'negro':'blanco','violeta':'blanco','naranja':'blanco','aqua':'negro','blanco':'negro'}
ACCENT_FOR_BG = {'negro':'naranja','violeta':'aqua','naranja':'aqua','aqua':'violeta','blanco':'violeta'}
LOGO_FOR_BG  = {'negro':'blanco','violeta':'blanco','naranja':'blanco','aqua':'negro','blanco':'negro'}

def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
LOGO = {c: b64(f'{BASE}/assets/logo-{c}.png') for c in ['blanco','negro','naranja','aqua','violeta']}

# tamaño y fuente por tipo de story (escala para 1920px de alto)
TYPE_STYLE = {
    'cover':    {'font':'futura', 'size':108, 'lh':1.02, 'upper':True},
    'body':     {'font':'lyon',   'size':70,  'lh':1.12, 'upper':False},
    'question': {'font':'lyon',   'size':78,  'lh':1.10, 'upper':False, 'italic':True},
    'closing':  {'font':'futura', 'size':96,  'lh':1.04, 'upper':True},
}

def story_html(s, total):
    bgname = s.get('bg','negro'); bg = C[bgname]
    txtname = s.get('color') or TEXT_FOR_BG[bgname]
    txt = C[txtname]
    acc = C[ACCENT_FOR_BG[bgname]]
    logo = LOGO[ s.get('logo') or LOGO_FOR_BG[bgname] ]
    st = TYPE_STYLE.get(s.get('type','body'), TYPE_STYLE['body'])
    cls = st['font'] + (' upper' if st.get('upper') else '') + (' ital' if st.get('italic') else '')
    num = f"{s.get('number','')} / {total}"
    return f'''<div class="story" style="background:{bg};color:{txt};--acc:{acc}">
      <div class="brand">#HistoriasEnMovimiento</div>
      <div class="content"><p class="{cls}" style="font-size:{st['size']}px;line-height:{st['lh']}">{s["text"]}</p></div>
      <div class="footer">
        <span class="pager">{num}</span>
        <img class="logo" src="data:image/png;base64,{logo}">
      </div>
    </div>'''

def render(spec_path, out_path):
    spec = json.load(open(spec_path))
    stories = spec['stories']; total = len(stories)
    body = ''.join(story_html(s, total) for s in stories)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'FuturaM'; src: url('file://{BASE}/fonts/FuturaStd-CondensedExtraBd.otf') format('opentype'); }}
@font-face {{ font-family:'GothamM'; src: url('file://{BASE}/fonts/GothamNarrow-Medium.otf') format('opentype'); }}
@font-face {{ font-family:'LyonD'; src: url('file://{BASE}/fonts/LyonDisplay-Regular.otf') format('opentype'); }}
@page {{ size:1080px 1920px; margin:0; }} * {{ margin:0; padding:0; box-sizing:border-box; }}
.story {{ width:1080px; height:1920px; position:relative; padding:120px 96px; display:flex; flex-direction:column; justify-content:space-between; overflow:hidden; }}
.brand {{ font-family:'GothamM'; font-size:30px; letter-spacing:2px; opacity:0.62; }}
.content {{ flex:1; display:flex; align-items:center; }}
.content p {{ max-width:888px; letter-spacing:-0.01em; }}
.futura {{ font-family:'FuturaM'; letter-spacing:-0.02em; }}
.futura.upper {{ text-transform:uppercase; }}
.lyon {{ font-family:'LyonD'; }}
.lyon.ital {{ font-style:italic; }}
.acc {{ color:var(--acc); }}
.footer {{ display:flex; justify-content:space-between; align-items:flex-end; }}
.pager {{ font-family:'GothamM'; font-size:28px; letter-spacing:3px; opacity:0.5; }}
.logo {{ width:170px; }}
</style></head><body>{body}</body></html>'''
    HTML(string=html).write_pdf(out_path)
    print(f"OK: {out_path}")

def render_pngs(spec_path, out_dir):
    import subprocess
    os.makedirs(out_dir, exist_ok=True)
    spec = json.load(open(spec_path))
    ep = spec.get('episodio','stories')
    tmp_pdf = "/tmp/_stories_tmp.pdf"
    render(spec_path, tmp_pdf)
    subprocess.run(["pdftoppm","-png","-r","96",tmp_pdf, os.path.join(out_dir, f"{ep}-story")], check=True)
    os.remove(tmp_pdf)
    pngs = sorted([f for f in os.listdir(out_dir) if f.startswith(f"{ep}-story") and f.endswith(".png")])
    print(f"OK: {len(pngs)} stories en {out_dir}/")
    return pngs

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "--png":
        render_pngs(sys.argv[1], sys.argv[2])
    else:
        render(sys.argv[1], sys.argv[2])
