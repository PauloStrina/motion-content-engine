#!/usr/bin/env python3
"""Corta los reels de una grabación larga según manifiesto_reels.json (corre en CI, requiere ffmpeg).
Por cada reel:
- Recorta los segmentos elegidos por el Editor de Video y QUITA LOS SILENCIOS internos
  (pausas entre palabras > GAP_MAX se colapsan) para darle dinamismo.
- Reencuadra a 1080x1920: modo "crop" (cara a pantalla completa) o "marco" (16:9 sobre fondo negro).
- Quema subtítulos ASS estilo karaoke (palabra activa en naranja), título con caja del color del tipo
  y logo Motion.
Uso: python cortar.py <video.mp4> <carpeta de la sesión> [carpeta de salida]
"""
import json, pathlib, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parents[2]  # raíz del repo
FONTS_DIR = BASE / "design-system" / "fonts"
FONT_FILE = FONTS_DIR / "FuturaStd-CondensedExtraBd.otf"
LOGO = BASE / "design-system" / "assets" / "logo-blanco.png"

GAP_MAX = 0.45   # pausa mayor a esto = silencio que se corta
PAD = 0.12       # aire que se deja a cada lado del corte de silencio
PAD_IN = 0.15    # aire antes de la primera palabra del segmento
PAD_OUT = 0.30   # aire después de la última palabra del segmento

# colores de marca (tokens del design system)
NEGRO, VIOLETA, NARANJA, AQUA = "1A1A1A", "50235A", "FF5000", "9DEDE3"
COLOR_TIPO = {"problema": NEGRO, "metodo": VIOLETA, "resultados": NARANJA, "conexion": AQUA}

MAX_CHARS_LINEA = 16  # caracteres por línea de subtítulo (Futura condensada, mayúsculas)
MAX_WORDS_LINEA = 4


def ass_color(hexrgb):
    """#RRGGBB → &HAABBGGRR (formato ASS)."""
    r, g, b = hexrgb[0:2], hexrgb[2:4], hexrgb[4:6]
    return f"&H00{b}{g}{r}"


def font_family():
    """Nombre real de la familia dentro del .otf (libass matchea por esto, no por el archivo)."""
    try:
        out = subprocess.run(["fc-scan", "--format", "%{family}", str(FONT_FILE)],
                             capture_output=True, text=True, check=True).stdout
        return out.split(",")[0].strip() or "Futura Std"
    except Exception:
        return "Futura Std"


def palabras_en(words, desde, hasta):
    return [w for w in words if w["desde"] >= desde - 0.05 and w["hasta"] <= hasta + 0.05]


def cortes_sin_silencio(reel, words):
    """Devuelve (intervalos [(a,b)] a conservar del video original, palabras con tiempos remapeados
    a la línea de tiempo del reel ya sin silencios)."""
    keep, sub_words = [], []
    for seg in reel["segmentos"]:
        ws = palabras_en(words, seg["desde"], seg["hasta"])
        if not ws:
            print(f"  AVISO: segmento {seg} sin palabras en transcript.json — se omite")
            continue
        a = max(0.0, ws[0]["desde"] - PAD_IN)
        grupo = [ws[0]]
        for w in ws[1:]:
            if w["desde"] - grupo[-1]["hasta"] > GAP_MAX:  # silencio: cerrar intervalo
                keep.append((a, grupo[-1]["hasta"] + PAD, grupo))
                a, grupo = w["desde"] - PAD, [w]
            else:
                grupo.append(w)
        keep.append((a, grupo[-1]["hasta"] + PAD_OUT, grupo))

    intervalos, t = [], 0.0
    for a, b, grupo in keep:
        intervalos.append((a, b))
        for w in grupo:
            sub_words.append({"w": w["w"], "desde": t + (w["desde"] - a), "hasta": t + (w["hasta"] - a)})
        t += b - a
    return intervalos, sub_words, t


def lineas_subtitulo(sub_words):
    """Agrupa palabras en líneas cortas (estilo OpusClip)."""
    lineas, actual = [], []
    for w in sub_words:
        texto = " ".join(x["w"] for x in actual)
        salto = (len(actual) >= MAX_WORDS_LINEA or len(texto) + len(w["w"]) + 1 > MAX_CHARS_LINEA
                 or (actual and w["desde"] - actual[-1]["hasta"] > 0.6))
        if actual and salto:
            lineas.append(actual)
            actual = []
        actual.append(w)
    if actual:
        lineas.append(actual)
    return lineas


def ts(t):
    """segundos → h:mm:ss.cc de ASS."""
    cs = int(round(t * 100))
    h, resto = divmod(cs, 360000)
    m, resto = divmod(resto, 6000)
    s, c = divmod(resto, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def escribir_ass(path, reel, sub_words, duracion, familia):
    tipo_hex = COLOR_TIPO.get(reel.get("tipo"), NARANJA)
    titulo_texto = ass_color(NEGRO) if tipo_hex == AQUA else ass_color("FFFFFF")
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{familia},84,{ass_color(NARANJA)},{ass_color('FFFFFF')},{ass_color(NEGRO)},{ass_color(NEGRO)},-1,0,0,0,100,100,0,0,1,6,0,2,60,60,560,1
Style: Titulo,{familia},58,{titulo_texto},{titulo_texto},{ass_color(tipo_hex)},{ass_color(tipo_hex)},-1,0,0,0,100,100,1,0,3,16,0,8,90,90,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    eventos = [f"Dialogue: 1,{ts(0)},{ts(duracion)},Titulo,,0,0,0,,{{\\fad(200,0)}}{reel['titulo'].upper()}"]
    lineas = lineas_subtitulo(sub_words)
    for i, linea in enumerate(lineas):
        ini = linea[0]["desde"]
        fin = linea[-1]["hasta"] + 0.08
        if i + 1 < len(lineas):
            fin = min(fin, lineas[i + 1][0]["desde"])
        partes = []
        for j, w in enumerate(linea):
            fin_k = linea[j + 1]["desde"] if j + 1 < len(linea) else w["hasta"]
            dur_cs = max(1, int(round((fin_k - w["desde"]) * 100)))
            texto = w["w"].upper().replace("{", "").replace("}", "").replace("\\", "")
            partes.append(f"{{\\k{dur_cs}}}{texto}")
        eventos.append(f"Dialogue: 0,{ts(ini)},{ts(fin)},Sub,,0,0,0,,{' '.join(partes)}")
    path.write_text(header + "\n".join(eventos) + "\n", encoding="utf-8")


def render(video, reel, intervalos, ass_path, out_path):
    """UNA sola decodificación por reel (seek al inicio del reel + duración acotada, nunca desde el
    segundo 0) y los silencios se saltan adentro con select/aselect sobre ese único stream — no se
    concatenan clips de decodificadores separados, así video y audio quedan siempre sincronizados."""
    overall_a = min(a for a, b in intervalos)
    overall_b = max(b for a, b in intervalos)
    seek = max(0.0, overall_a - 2)
    duracion_lectura = overall_b - seek + 0.5
    cond = "+".join(f"between(t\\,{a:.3f}\\,{b:.3f})" for a, b in intervalos)

    filtros = [
        f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB[vc];",
        f"[0:a]aselect='{cond}',asetpts=N/SR/TB[ac];",
    ]
    if reel.get("modo") == "marco":
        filtros.append("[vc]scale=1080:-2:force_original_aspect_ratio=decrease,"
                       f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x{NEGRO}[vf];")
    else:
        filtros.append("[vc]crop=min(iw\\,ih*9/16):ih,scale=1080:1920[vf];")
    filtros.append("[1:v]scale=170:-1[lg];[vf][lg]overlay=W-w-48:H-h-64[vl];")
    filtros.append(f"[vl]ass=filename={ass_path.as_posix()}:fontsdir={FONTS_DIR.as_posix()}[vout];")
    filtros.append("[ac]loudnorm=I=-16:TP=-1.5:LRA=11[aout]")

    script = out_path.with_suffix(".filter")
    script.write_text("\n".join(filtros), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-copyts",
                    "-ss", f"{seek:.3f}", "-t", f"{duracion_lectura:.3f}", "-i", str(video),
                    "-i", str(LOGO),
                    "-filter_complex_script", str(script),
                    "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-crf", "18", "-preset", "faster", "-pix_fmt", "yuv420p",
                    "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    str(out_path)], check=True)
    script.unlink()


def main(video, sesion_dir, out_dir="media_out"):
    sesion = pathlib.Path(sesion_dir)
    manifiesto = json.loads((sesion / "manifiesto_reels.json").read_text(encoding="utf-8"))
    words = json.loads((sesion / "transcript.json").read_text(encoding="utf-8"))["palabras"]
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    familia = font_family()
    print(f"Fuente para subtítulos: {familia}")

    for reel in manifiesto["reels"]:
        nombre = f"reel_{reel['n']}_{reel['slug']}"
        print(f"\n== {nombre} ({reel.get('tipo')}, tesis {reel.get('tesis')}) ==")
        intervalos, sub_words, duracion = cortes_sin_silencio(reel, words)
        if not intervalos:
            print("  AVISO: sin intervalos — reel omitido")
            continue
        print(f"  {len(intervalos)} cortes (silencios quitados), duración final {duracion:.1f}s"
              + ("  ⚠ PASA DE 62s" if duracion > 62 else ""))
        ass_path = out / f"{nombre}.ass"
        escribir_ass(ass_path, reel, sub_words, duracion, familia)
        render(video, reel, intervalos, ass_path, out / f"{nombre}.mp4")
        print(f"  OK → {out / (nombre + '.mp4')}")


if __name__ == "__main__":
    main(*sys.argv[1:])
