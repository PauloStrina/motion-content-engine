#!/usr/bin/env python3
"""MOTION motion-graphics v2 — animacion dinamica + formas + audio.
Easings variados, escala con overshoot, formas geometricas animadas (barras/bloques del isotipo).
Uso: python video2.py slides/guion.json salida.mp4 [pista_audio.mp3]"""
import base64, json, os, sys, math, subprocess, tempfile, shutil
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
C = {'negro':'#1A1A1A','naranja':'#FF5000','violeta':'#50235A','aqua':'#9DEDE3','blanco':'#FFFFFF'}
FPS = 30; W, H = 1080, 1920

def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
LOGO = {c: b64(f'{BASE}/assets/logo-{c}.png') for c in ['blanco','negro','naranja','aqua','violeta']}

# ── EASINGS ──
def clamp(x): return max(0.0, min(1.0, x))
def out_cubic(t): return 1-pow(1-t,3)
def out_back(t):   # overshoot (rebote elegante)
    c1=1.70158; c3=c1+1
    return 1 + c3*pow(t-1,3) + c1*pow(t-1,2)
def out_expo(t): return 1 if t>=1 else 1-pow(2,-10*t)
EAS = {'cubic':out_cubic,'back':out_back,'expo':out_expo}

def hex2rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def rgb2hex(r): return '#%02X%02X%02X'%tuple(int(x) for x in r)
def mix(a,b,t):
    A,B=hex2rgb(a),hex2rgb(b); return rgb2hex([A[i]+(B[i]-A[i])*t for i in range(3)])

def shape_html(sh, t):
    """Formas animadas: barra que crece, bloque que entra, linea que cruza."""
    ease = EAS[sh.get('ease','expo')]
    lt = clamp((t - sh.get('delay',0))/max(0.001,sh.get('dur',0.6)))
    e = ease(lt)
    col = C.get(sh.get('color',''), sh.get('color','#FFF'))
    if sh['kind']=='bar':       # barra vertical que crece desde abajo (estetica isotipo)
        h = sh['h']*e
        return f'<div style="position:absolute;left:{sh["x"]}px;bottom:{sh["y"]}px;width:{sh["w"]}px;height:{h:.0f}px;background:{col};opacity:{sh.get("op",1)}"></div>'
    if sh['kind']=='block':     # bloque que entra deslizando
        dx = (1-e)*sh.get('from_x',-300)
        return f'<div style="position:absolute;left:{sh["x"]}px;top:{sh["y"]}px;width:{sh["w"]}px;height:{sh["h"]}px;background:{col};transform:translateX({dx:.0f}px);opacity:{e:.2f}"></div>'
    if sh['kind']=='line':      # linea horizontal que cruza
        w = sh['w']*e
        return f'<div style="position:absolute;left:{sh["x"]}px;top:{sh["y"]}px;width:{w:.0f}px;height:{sh.get("th",10)}px;background:{col}"></div>'
    return ''

def el_html(el, t):
    ease = EAS[el.get('ease','back')]
    lt = clamp((t - el.get('delay',0))/max(0.001,el.get('dur',0.5)))
    e = ease(lt)
    eo = out_cubic(lt)  # opacidad siempre suave
    col = C.get(el.get('color',''), el.get('color','#FFF'))
    font = {'futura':'futura','lyon':'lyon','lyont':'lyont'}[el.get('font','futura')]
    size = el['size']; lh = el.get('lh', int(size*1.0))
    sc = el.get('scale_from',0.7) + (1-el.get('scale_from',0.7))*e
    ty = (1-e)*el.get('rise',50)
    return f'''<div style="opacity:{eo:.3f};transform:translateY({ty:.1f}px) scale({sc:.3f});transform-origin:left center;margin-bottom:{el.get("mb",14)}px">
      <span class="{font}" style="font-size:{size}px;line-height:{lh}px;color:{col}">{el['text']}</span></div>'''

def frame_html(scene, t):
    bg = C[scene.get('bg','negro')]
    # fondo con barrido de color opcional
    bgstyle = f'background:{bg}'
    if scene.get('bg_sweep'):
        sc = out_expo(clamp(t*1.3))
        c2 = C[scene['bg_sweep']]
        bgstyle = f'background:linear-gradient(135deg,{bg} {100-sc*100:.0f}%,{c2} 100%)'
    shapes = ''.join(shape_html(s,t) for s in scene.get('shapes',[]))
    items = ''.join(el_html(e,t) for e in scene['elements'])
    logo = ''
    if scene.get('logo'):
        lo = out_cubic(clamp((t-0.3)*2))
        logo = f'<img src="data:image/png;base64,{LOGO[scene["logo"]]}" style="position:absolute;bottom:90px;right:84px;width:200px;opacity:{lo:.2f}">'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'FuturaM'; src:url('file://{BASE}/fonts/FuturaStd-CondensedExtraBd.otf'); }}
@font-face {{ font-family:'LyonD'; src:url('file://{BASE}/fonts/LyonDisplay-Regular.otf'); }}
@font-face {{ font-family:'LyonT'; src:url('file://{BASE}/fonts/Lyon_Text-Regular.otf'); }}
@page {{ size:{W}px {H}px; margin:0; }} *{{margin:0;padding:0;box-sizing:border-box}}
body {{ width:{W}px; height:{H}px; {bgstyle}; overflow:hidden; position:relative }}
.stage {{ position:absolute; top:0; left:84px; right:84px; height:{H}px; display:flex; flex-direction:column; justify-content:center; z-index:2 }}
.futura {{ font-family:'FuturaM'; text-transform:uppercase }} .lyon {{ font-family:'LyonD' }} .lyont {{ font-family:'LyonT' }}
</style></head><body>{shapes}<div class="stage">{items}</div>{logo}</body></html>'''

def render(spec_path, out_path, audio=None):
    spec = json.load(open(spec_path))
    tmp = tempfile.mkdtemp(); fi=0
    for si,scene in enumerate(spec['scenes']):
        nf=int(scene['seconds']*FPS)
        for f in range(nf):
            t=f/max(1,nf-1)
            HTML(string=frame_html(scene,t)).write_pdf(f'{tmp}/p.pdf')
            subprocess.run(['pdftoppm','-png','-r','51.2','-singlefile',f'{tmp}/p.pdf',f'{tmp}/f{fi:05d}'],check=True,capture_output=True)
            fi+=1
        print(f"escena {si+1}/{len(spec['scenes'])}")
    args=['ffmpeg','-y','-framerate',str(FPS),'-i',f'{tmp}/f%05d.png']
    if audio and os.path.exists(audio):
        args+=['-i',audio,'-c:a','aac','-shortest']
    args+=['-c:v','libx264','-pix_fmt','yuv420p',out_path]
    subprocess.run(args,check=True,capture_output=True)
    shutil.rmtree(tmp)
    print(f"OK: {out_path} ({os.path.getsize(out_path)//1024}KB, {fi/FPS:.1f}s)")

if __name__=='__main__':
    render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else None)
