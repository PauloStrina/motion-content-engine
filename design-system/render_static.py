#!/usr/bin/env python3
"""MOTION plantillas estaticas — quote card, dato, lista. Formato cuadrado 1080x1080 (feed) o 1080x1350.
Uso: python render_static.py slides/piezas.json salida.pdf"""
import base64, json, os, sys
from weasyprint import HTML
BASE = os.path.dirname(os.path.abspath(__file__))
C = {'negro':'#1A1A1A','naranja':'#FF5000','violeta':'#50235A','aqua':'#9DEDE3','blanco':'#FFFFFF'}
SHADOW_FOR_BG={'negro':'aqua','violeta':'aqua','naranja':'violeta','aqua':'violeta','blanco':'violeta'}
LOGO_FOR_BG={'negro':'blanco','violeta':'blanco','naranja':'blanco','aqua':'negro','blanco':'negro'}
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
LOGO={c:b64(f'{BASE}/assets/logo-{c}.png') for c in ['blanco','negro','naranja','aqua','violeta']}
def hex2rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def rgb2hex(r): return '#%02X%02X%02X'%tuple(int(x) for x in r)
def mix(a,b,t):
    A,B=hex2rgb(a),hex2rgb(b); return rgb2hex([A[i]+(B[i]-A[i])*t for i in range(3)])
def lam(word,size,front,shadow,bg,depth=10):
    line=int(size*1.06);ly=''
    for i in range(depth,0,-1):
        ly+=f'<div class="futura" style="position:absolute;top:{i}px;left:{i}px;font-size:{size}px;line-height:{line}px;color:{mix(shadow,bg,i/depth*0.85)}">{word}</div>'
    ly+=f'<div class="futura" style="position:absolute;top:0;left:0;font-size:{size}px;line-height:{line}px;color:{front}">{word}</div>'
    return f'<div style="position:relative;height:{line+depth}px">{ly}</div>'

def quote_card(p):
    bg=C[p.get('bg','violeta')];bgn=p.get('bg','violeta')
    logo=LOGO[LOGO_FOR_BG[bgn]];txtcol=C['blanco'] if bgn in('negro','violeta','naranja') else C['negro']
    acc=C['aqua'] if bgn in('negro','violeta') else C['violeta']
    return f'''<div class="slide sq" style="background:{bg}">
      <div class="quote-mark" style="color:{acc}">"</div>
      <div class="lyon" style="font-size:74px;line-height:1.2;color:{txtcol};max-width:880px">{p['quote']}</div>
      <div class="gotham" style="font-size:30px;letter-spacing:2px;color:{acc};margin-top:54px;text-transform:uppercase">MOTION · Lo complejo, simple</div>
      <img class="logo" src="data:image/png;base64,{logo}"></div>'''

def data_card(p):
    bg=C[p.get('bg','negro')];bgn=p.get('bg','negro')
    logo=LOGO[LOGO_FOR_BG[bgn]];txtcol=C['blanco'] if bgn in('negro','violeta','naranja') else C['negro']
    num=p['number'];shadow=C[SHADOW_FOR_BG[bgn]]
    return f'''<div class="slide sq" style="background:{bg}">
      <div class="gotham" style="font-size:30px;letter-spacing:3px;color:{C['aqua'] if bgn in('negro','violeta') else C['violeta']};text-transform:uppercase;margin-bottom:20px">{p.get('eyebrow','')}</div>
      {lam(num,300,C['naranja'] if bgn!='naranja' else C['blanco'],shadow,bg,12)}
      <div class="lyon" style="font-size:54px;line-height:1.2;color:{txtcol};max-width:880px;margin-top:30px">{p['label']}</div>
      <img class="logo" src="data:image/png;base64,{logo}"></div>'''

def list_card(p):
    bg=C[p.get('bg','negro')];bgn=p.get('bg','negro')
    logo=LOGO[LOGO_FOR_BG[bgn]];txtcol=C['blanco'] if bgn in('negro','violeta','naranja') else C['negro']
    acc=C['naranja']
    items=''
    for i,it in enumerate(p['items'],1):
        items+=f'<div style="display:flex;align-items:baseline;margin-bottom:28px"><span class="futura" style="font-size:54px;color:{acc};margin-right:24px;min-width:60px">{i:02d}</span><span class="lyon" style="font-size:46px;line-height:1.2;color:{txtcol}">{it}</span></div>'
    return f'''<div class="slide sq" style="background:{bg}">
      <div class="futura" style="font-size:78px;line-height:0.98;color:{txtcol};margin-bottom:54px;text-transform:uppercase">{p['title']}</div>
      {items}
      <img class="logo" src="data:image/png;base64,{logo}"></div>'''

def render(spec_path,out):
    spec=json.load(open(spec_path));body=''
    R={'quote':quote_card,'data':data_card,'list':list_card}
    for p in spec['pieces']: body+=R[p['type']](p)
    html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'FuturaM';src:url('file://{BASE}/fonts/FuturaStd-CondensedExtraBd.otf')}}
@font-face{{font-family:'GothamM';src:url('file://{BASE}/fonts/GothamNarrow-Medium.otf')}}
@font-face{{font-family:'LyonD';src:url('file://{BASE}/fonts/LyonDisplay-Regular.otf')}}
@page{{size:1080px 1080px;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
.sq{{width:1080px;height:1080px;position:relative;overflow:hidden;padding:90px 84px;display:flex;flex-direction:column;justify-content:center}}
.futura{{font-family:'FuturaM';text-transform:uppercase}}.lyon{{font-family:'LyonD'}}.gotham{{font-family:'GothamM'}}
.quote-mark{{font-family:'LyonD';font-size:200px;line-height:0.5;height:90px}}
.logo{{position:absolute;bottom:60px;right:84px;width:170px}}
</style></head><body>{body}</body></html>'''
    HTML(string=html).write_pdf(out);print(f"OK: {out}")
if __name__=='__main__': render(sys.argv[1],sys.argv[2])
