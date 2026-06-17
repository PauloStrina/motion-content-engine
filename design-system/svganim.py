#!/usr/bin/env python3
"""MOTION SVG concept animator — anima trazos (stroke-dashoffset) + pelotitas.
Render: cada frame es un SVG -> PNG (cairosvg) -> ffmpeg. Sin Chrome.
Plantilla 1: Transformacion Continua (3 curvas: mejora / cambio / continua)."""
import os, sys, math, subprocess, tempfile, shutil
try:
    import cairosvg
except ImportError:
    os.system("pip install cairosvg --quiet")
    import cairosvg

C = {'negro':'#1A1A1A','naranja':'#FF5000','violeta':'#50235A','aqua':'#9DEDE3','blanco':'#FFFFFF','coral':'#FF7A59'}
FPS=30; W,H=1080,1920

def ease_io(t):  # easeInOutCubic
    return 4*t*t*t if t<0.5 else 1-pow(-2*t+2,3)/2
def ease_out(t): return 1-pow(1-t,3)
def ease_back(t):
    c1=1.70158; c3=c1+1
    return 1+c3*pow(t-1,3)+c1*pow(t-1,2)
def clamp(x): return max(0.0,min(1.0,x))

# longitudes aproximadas de cada path (para dashoffset)
def path_len(kind):
    return {'mejora':720,'cambio':560,'continua':880}[kind]

def frame_svg(t):
    """t: 0..1 progreso global de la escena."""
    # fase 1 (0-.7): se dibujan las 3 curvas escalonadas. fase 2 (.5-1): pelotita recorre la continua.
    def draw(kind, color, delay, dur, d_path):
        L = path_len(kind)
        p = ease_io(clamp((t-delay)/dur))
        off = L*(1-p)
        return f'<path d="{d_path}" fill="none" stroke="{color}" stroke-width="11" stroke-linecap="round" stroke-dasharray="{L}" stroke-dashoffset="{off:.0f}"/>'

    # Curvas estilo imagen 1, en un panel vertical (apiladas)
    # MEJORA CONTINUA: escalones suaves ascendentes
    mejora = "M 160 760 Q 230 760 250 700 Q 290 700 320 640 Q 370 640 400 580 Q 450 580 480 520"
    # GESTION DEL CAMBIO: dos curvas que se cruzan
    cambio = "M 160 1180 Q 350 1180 560 1000"
    cambio2 = "M 160 1000 Q 350 1180 560 1180"
    # TRANSFORMACION CONTINUA: linea serpenteante orgánica que sube
    continua = "M 160 1640 C 280 1560 200 1480 320 1420 C 440 1360 360 1280 480 1220"

    s = ''
    # ejes sutiles
    axis_op = ease_out(clamp(t*2))
    # bloque 1
    s += draw('mejora', C['aqua'], 0.0, 0.5, mejora)
    s += draw('cambio', C['violeta'], 0.25, 0.5, cambio)
    s += draw('cambio', C['violeta'], 0.25, 0.5, cambio2)
    s += draw('continua', C['naranja'], 0.5, 0.6, continua)

    # pelotitas al final de cada curva (aparecen cuando la curva termina)
    def dot(cx, cy, color, delay):
        e = ease_back(clamp((t-delay)/0.4))
        r = 26*max(0,e)
        return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{color}"/>'
    s += dot(480,520, C['aqua'], 0.5)
    s += dot(560,1000, C['violeta'], 0.75)
    s += dot(480,1220, C['naranja'], 1.05)

    # labels (Lyon-like via system serif fallback en SVG -> usamos texto simple)
    def label(txt, y, color, delay, size=46):
        o = ease_out(clamp((t-delay)/0.4))
        return f'<text x="160" y="{y}" fill="{color}" opacity="{o:.2f}" font-family="Futura,Arial" font-weight="bold" font-size="{size}" letter-spacing="1">{txt}</text>'
    s += label("MEJORA CONTINUA", 600, C['aqua'], 0.55)
    s += label("GESTIÓN DEL CAMBIO", 1100, C['violeta'], 0.8)
    s += label("TRANSFORMACIÓN CONTINUA", 1740, C['naranja'], 1.1, 52)

    # titulo superior
    ot = ease_out(clamp(t*1.5))
    title = f'<text x="160" y="260" fill="{C["blanco"]}" opacity="{ot:.2f}" font-family="Futura,Arial" font-weight="bold" font-size="76">LOS MODELOS</text>'
    title += f'<text x="160" y="350" fill="{C["naranja"]}" opacity="{ot:.2f}" font-family="Futura,Arial" font-weight="bold" font-size="76">DE GESTIÓN</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
      <rect width="{W}" height="{H}" fill="{C['negro']}"/>
      {title}{s}
    </svg>'''

def render(out_path, seconds=5.0):
    tmp=tempfile.mkdtemp(); nf=int(seconds*FPS)
    for f in range(nf):
        t=f/max(1,nf-1)
        cairosvg.svg2png(bytestring=frame_svg(t).encode(), write_to=f'{tmp}/f{f:05d}.png', output_width=W, output_height=H)
    subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',f'{tmp}/f%05d.png',
        '-c:v','libx264','-pix_fmt','yuv420p',out_path],check=True,capture_output=True)
    shutil.rmtree(tmp)
    print(f"OK: {out_path} ({os.path.getsize(out_path)//1024}KB, {seconds}s)")

if __name__=='__main__':
    render(sys.argv[1] if len(sys.argv)>1 else 'out.mp4')
