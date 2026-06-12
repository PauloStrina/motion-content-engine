#!/usr/bin/env python3
"""Corte automático de reels desde una grabación. Requiere: pip install openai-whisper && ffmpeg instalado.
Uso: python cut_reels.py grabacion.mp4 cortes.json
cortes.json lo genera el Agente de Video: [{"in":"00:03:12","out":"00:03:54","slug":"gancho-cambio"}]"""
import json, subprocess, sys, pathlib

SUBS_STYLE = "FontName=Arial,Fontsize=18,PrimaryColour=&H00D4E38F,OutlineColour=&H00862A5B,BorderStyle=3"  # TODO: fuente Motion real vía subs.ass

def cut(src, c, outdir):
    out = pathlib.Path(outdir)/f"reel_{c['slug']}.mp4"
    # corte + reencuadre 9:16 centrado + audio normalizado
    subprocess.run(["ffmpeg","-y","-ss",c["in"],"-to",c["out"],"-i",src,
        "-vf","crop=ih*9/16:ih,scale=1080:1920","-af","loudnorm",
        "-c:v","libx264","-preset","fast", str(out)], check=True)
    print("OK", out)

if __name__ == "__main__":
    src, plan = sys.argv[1], json.load(open(sys.argv[2]))
    pathlib.Path("out").mkdir(exist_ok=True)
    for c in plan: cut(src, c, "out")
    # Paso 2 (subtítulos): whisper genera .srt del corte y se queman con -vf subtitles=archivo.srt:force_style=SUBS_STYLE
