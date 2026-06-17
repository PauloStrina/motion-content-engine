#!/usr/bin/env python3
"""MOTION motion-graphics — genera frames con WeasyPrint y los ensambla con ffmpeg.
Animacion por interpolacion de propiedades entre keyframes, a 30fps.
Uso: python video.py slides/guion_video.json salida.mp4"""
import base64, json, os, sys, math, subprocess, tempfile, shutil
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
C = {'negro':'#1A1A1A','naranja':'#FF5000','violeta':'#50235A','aqua':'#9DEDE3','blanco':'#FFFFFF'}
FPS = 30
W, H = 1080, 1920  # 9:16 vertical

def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
LOGO = {c: b64(f'{BASE}/assets/logo-{c}.png') for c in ['blanco','negro','naranja','aqua','violeta']}

def ease(t):  # easeOutCubic
    return 1 - pow(1-t, 3)

def frame_html(scene, t):
    """t = progreso 0..1 dentro de la escena."""
    bg = C[scene.get('bg','negro')]
    e = ease(min(t*scene.get('speed',1.4), 1.0))   # la animacion entra y se queda
    items = ''
    for el in scene['elements']:
        delay = el.get('delay', 0)
        lt = max(0, min((t - delay) / max(0.001, el.get('dur', 0.5)), 1))
        le = ease(lt)
        # animaciones: fade + slide up
        opacity = le if el.get('anim') != 'none' else 1
        ty = (1-le) * el.get('rise', 40)
        font = el.get('font','futura')
        cls = {'futura':'futura','lyon':'lyon','lyont':'lyont'}[font]
        size = el['size']
        col = C.get(el.get('color',''), el.get('color','#FFF'))
        lh = el.get('lh', int(size*1.0))
        scale = el.get('scale_from', 1) + (1 - el.get('scale_from',1))*le
        items += f'''<div style="opacity:{opacity:.3f};transform:translateY({ty:.1f}px) scale({scale:.3f});transform-origin:left center;margin-bottom:{el.get("mb",12)}px">
          <span class="{cls}" style="font-size:{size}px;line-height:{lh}px;color:{col}">{el['text']}</span></div>'''
    show_logo = scene.get('logo')
    logo_html = f'<img src="data:image/png;base64,{LOGO[show_logo]}" style="position:absolute;bottom:90px;right:84px;width:200px;opacity:{e:.2f}">' if show_logo else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'FuturaM'; src: url('file://{BASE}/fonts/FuturaStd-CondensedExtraBd.otf') format('opentype'); }}
@font-face {{ font-family:'LyonD'; src: url('file://{BASE}/fonts/LyonDisplay-Regular.otf') format('opentype'); }}
@font-face {{ font-family:'LyonT'; src: url('file://{BASE}/fonts/Lyon_Text-Regular.otf') format('opentype'); }}
@page {{ size:{W}px {H}px; margin:0; }} *{{margin:0;padding:0;box-sizing:border-box}}
body {{ width:{W}px; height:{H}px; background:{bg}; overflow:hidden; }}
.stage {{ position:absolute; top:0; left:84px; right:84px; height:{H}px; display:flex; flex-direction:column; justify-content:center; }}
.futura {{ font-family:'FuturaM'; text-transform:uppercase; }}
.lyon {{ font-family:'LyonD'; }} .lyont {{ font-family:'LyonT'; }}
</style></head><body><div class="stage">{items}</div>{logo_html}</body></html>'''

def render_video(spec_path, out_path):
    spec = json.load(open(spec_path))
    tmp = tempfile.mkdtemp()
    fi = 0
    for si, scene in enumerate(spec['scenes']):
        nframes = int(scene['seconds'] * FPS)
        for f in range(nframes):
            t = f / max(1, nframes-1)
            html = frame_html(scene, t)
            pdf = f'{tmp}/f{fi:05d}.pdf'
            HTML(string=html).write_pdf(pdf)
            subprocess.run(['pdftoppm','-png','-r','51.2','-singlefile',pdf,f'{tmp}/f{fi:05d}'],
                           check=True, capture_output=True)
            os.remove(pdf)
            fi += 1
        print(f"escena {si+1}/{len(spec['scenes'])} ({nframes} frames)")
    # ensamblar
    subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',f'{tmp}/f%05d.png',
        '-c:v','libx264','-pix_fmt','yuv420p','-vf',f'scale={W}:{H}', out_path],
        check=True, capture_output=True)
    shutil.rmtree(tmp)
    print(f"OK: {out_path} ({os.path.getsize(out_path)//1024} KB, {fi} frames, {fi/FPS:.1f}s)")

if __name__ == '__main__':
    render_video(sys.argv[1], sys.argv[2])
