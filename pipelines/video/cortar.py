#!/usr/bin/env python3
"""Corta los reels de una grabación larga según manifiesto_reels.json.

Por cada reel:
- recorta los segmentos elegidos y colapsa silencios internos;
- reencuadra a 1080x1920 según modo crop, marco, split, zonas o poster;
- genera video limpio + props para Remotion, o branding ASS directo.

Uso:
  python cortar.py VIDEO SESION [SALIDA] [--pantalla VIDEO] [--poster IMAGEN] [--remotion]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess

BASE = pathlib.Path(__file__).resolve().parents[2]
FONTS_DIR = BASE / "design-system" / "fonts"
FONT_FILE = FONTS_DIR / "FuturaStd-CondensedExtraBd.otf"
LOGO = BASE / "design-system" / "assets" / "logo-blanco.png"
FONDO_SIN_PANTALLA = BASE / "design-system" / "assets" / "innpulso-fondo.png"

GAP_MAX = 0.45
PAD = 0.12
PAD_IN = 0.15
PAD_OUT = 0.30

DURACION_MAX = 90

# Solo se borra la muletilla aislada: pegada al habla, el empalme suena peor que la muletilla.
MULETILLAS = {
    "eh", "ehh", "ehhh", "em", "mmm", "mm", "este", "esteee",
    "digamos", "viste", "tipo", "nada", "bueno",
}
MULETILLAS_FRASE = {("o", "sea"), ("es", "decir"), ("no", "sé")}
PAUSA_MULETILLA = 0.15

NEGRO, VIOLETA, NARANJA, AQUA = "1A1A1A", "50235A", "FF5000", "9DEDE3"
COLOR_TIPO = {"problema": NEGRO, "metodo": VIOLETA, "resultados": NARANJA, "conexion": AQUA}

MAX_CHARS_LINEA = 16
MAX_WORDS_LINEA = 4


def ass_color(hexrgb):
    r, g, b = hexrgb[0:2], hexrgb[2:4], hexrgb[4:6]
    return f"&H00{b}{g}{r}"


def font_family():
    try:
        out = subprocess.run(
            ["fc-scan", "--format", "%{family}", str(FONT_FILE)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return out.split(",")[0].strip() or "Futura Std"
    except Exception:
        return "Futura Std"


def palabras_en(words, desde, hasta):
    return [w for w in words if w["desde"] >= desde - 0.05 and w["hasta"] <= hasta + 0.05]


def _aislada(ws, i, largo):
    """La muletilla se borra si arranca el segmento o si tiene pausa de los dos lados."""
    antes = ws[i]["desde"] - ws[i - 1]["hasta"] if i > 0 else PAUSA_MULETILLA
    j = i + largo
    despues = ws[j]["desde"] - ws[j - 1]["hasta"] if j < len(ws) else PAUSA_MULETILLA
    return i == 0 or (antes >= PAUSA_MULETILLA and despues >= PAUSA_MULETILLA)


def sin_muletillas(ws):
    """Devuelve (palabras, cortar_antes) donde cortar_antes[k] marca que hubo un borrado."""
    salida, cortar, pendiente = [], [], False
    i = 0
    while i < len(ws):
        n = _normal(ws[i]["w"])
        par = (n, _normal(ws[i + 1]["w"])) if i + 1 < len(ws) else None
        largo = 2 if par in MULETILLAS_FRASE else (1 if n in MULETILLAS else 0)
        if largo and _aislada(ws, i, largo):
            pendiente = True
            i += largo
            continue
        salida.append(ws[i])
        cortar.append(pendiente)
        pendiente = False
        i += 1
    return salida, cortar


def cortes_sin_silencio(reel, words, muletillas=True):
    keep, sub_words = [], []
    for seg in reel["segmentos"]:
        ws = palabras_en(words, seg["desde"], seg["hasta"])
        if not ws:
            print(f"  AVISO: segmento {seg} sin palabras en transcript.json — se omite")
            continue
        cortar = [False] * len(ws)
        if muletillas:
            ws, cortar = sin_muletillas(ws)
            if not ws:
                print(f"  AVISO: segmento {seg} quedó vacío tras quitar muletillas — se omite")
                continue
        hablante = seg.get("hablante")
        a = max(0.0, ws[0]["desde"] - PAD_IN)
        grupo = [ws[0]]
        for w, corte in zip(ws[1:], cortar[1:]):
            if corte or w["desde"] - grupo[-1]["hasta"] > GAP_MAX:
                keep.append((a, grupo[-1]["hasta"] + PAD, grupo, hablante))
                a, grupo = w["desde"] - PAD, [w]
            else:
                grupo.append(w)
        keep.append((a, grupo[-1]["hasta"] + PAD_OUT, grupo, hablante))

    intervalos, inicios, tramos, t = [], [], [], 0.0
    for a, b, grupo, hablante in keep:
        intervalos.append((a, b))
        inicios.append(round(t, 3))
        for w in grupo:
            sub_words.append(
                {
                    "w": w["w"],
                    "desde": t + (w["desde"] - a),
                    "hasta": t + (w["hasta"] - a),
                    "orig": w["desde"],
                }
            )
        tramos.append((round(t, 3), round(t + (b - a), 3), hablante))
        t += b - a
    return intervalos, sub_words, t, inicios, tramos


def tramos_de(tramos, hablante, epsilon=0.02):
    """Une los tramos contiguos del mismo hablante en rangos de tiempo de salida."""
    unidos = []
    for a, b, quien in tramos:
        if quien != hablante:
            continue
        if unidos and a - unidos[-1][1] <= epsilon:
            unidos[-1][1] = b
        else:
            unidos.append([a, b])
    return [(a, b) for a, b in unidos]


def lineas_subtitulo(sub_words):
    lineas, actual = [], []
    for w in sub_words:
        texto = " ".join(x["w"] for x in actual)
        salto = (
            len(actual) >= MAX_WORDS_LINEA
            or len(texto) + len(w["w"]) + 1 > MAX_CHARS_LINEA
            or (actual and w["desde"] - actual[-1]["hasta"] > 0.6)
        )
        if actual and salto:
            lineas.append(actual)
            actual = []
        actual.append(w)
    if actual:
        lineas.append(actual)
    return lineas


def ts(t):
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


def render(
    video,
    reel,
    intervalos,
    ass_path,
    out_path,
    pantalla=None,
    poster=None,
    offset_pantalla=0.0,
    brand=True,
    zonas=None,
    zonas_personas=None,
    tramos=None,
):
    """UNA sola decodificación por reel (seek al inicio del reel + duración acotada, nunca desde el
    segundo 0) y los silencios se saltan adentro con select/aselect sobre ese único stream — no se
    concatenan clips de decodificadores separados, así video y audio quedan siempre sincronizados.
    modo "split": la grabación de pantalla (segundo video, mismos cortes) va arriba y la cámara abajo.
    modo "zonas": video ÚNICO ya compuesto (stream de conferencia) — se recortan dos regiones del
    mismo frame (zonas.pantalla y zonas.camara, fracciones 0-1 del ancho/alto) y se re-apilan.
    reel["sin_pantalla"]=true (solo con modo "zonas"): ese reel no tiene contenido de pantalla en
    este tramo (solo el orador) — la mitad superior usa FONDO_SIN_PANTALLA (imagen fija) en vez de
    recortar el frame en vivo.
    modo "entrevista": video ÚNICO con las dos personas en cuadro. Se recortan dos zonas 9:16 del
    mismo frame (zonas_personas.entrevistador y .entrevistado) y se conmuta entre ellas con overlay
    habilitado en los tramos del entrevistador. Las dos ramas salen del mismo decode y del mismo
    select, así que comparten timeline y el corte no puede desincronizar el audio."""
    overall_a = min(a for a, _ in intervalos)
    overall_b = max(b for _, b in intervalos)
    seek = max(0.0, overall_a - 2)
    duracion_lectura = overall_b - seek + 0.5
    cond = "+".join(f"between(t\\,{a:.3f}\\,{b:.3f})" for a, b in intervalos)

    modo = reel.get("modo", "crop")
    if modo == "auto":
        raise ValueError(f"{reel.get('slug')}: modo auto no resuelto; ejecutar resolver_layout.py")
    if modo == "split" and not pantalla:
        raise ValueError(f"{reel.get('slug')}: modo split requiere --pantalla")
    if modo == "zonas" and not zonas:
        raise ValueError(f"{reel.get('slug')}: modo zonas requiere coordenadas")
    if modo == "poster" and (not poster or not pathlib.Path(poster).exists()):
        raise ValueError(f"{reel.get('slug')}: modo poster requiere --poster válido")
    if modo == "entrevista" and not zonas_personas:
        raise ValueError(f"{reel.get('slug')}: modo entrevista requiere zonas_personas")

    entradas = ["-ss", f"{seek:.3f}", "-t", f"{duracion_lectura:.3f}", "-i", str(video)]
    filtros = [f"[0:a]aselect='{cond}',asetpts=N/SR/TB[ac];"]

    if modo == "split":
        off = offset_pantalla
        cond_p = "+".join(f"between(t\\,{a + off:.3f}\\,{b + off:.3f})" for a, b in intervalos)
        seek_p = max(0.0, overall_a + off - 2)
        entradas += ["-ss", f"{seek_p:.3f}", "-t", f"{duracion_lectura:.3f}", "-i", str(pantalla)]
        filtros.append(
            f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB,fps=30,"
            "crop=min(iw\\,ih*9/8):ih,scale=1080:960[vcam];"
        )
        filtros.append(
            f"[1:v]select='{cond_p}',setpts=N/FRAME_RATE/TB,fps=30,"
            "scale=1080:960:force_original_aspect_ratio=decrease,"
            f"pad=1080:960:(ow-iw)/2:(oh-ih)/2:color=0x{NEGRO}[vpan];"
        )
        filtros.append("[vpan][vcam]vstack=inputs=2[vf];")
        logo_idx = 2
    elif modo == "zonas":
        zp, zc = zonas["pantalla"], zonas["camara"]
        sin_pantalla = bool(reel.get("sin_pantalla"))
        if sin_pantalla:
            entradas += [
                "-loop", "1", "-framerate", "30", "-t", f"{duracion_lectura:.3f}",
                "-i", str(FONDO_SIN_PANTALLA),
            ]
            fondo_idx = 1
            filtros.append(f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB,fps=30[vzb];")
            filtros.append(
                f"[{fondo_idx}:v]fps=30,scale=1080:960:force_original_aspect_ratio=increase,"
                f"crop=1080:960,trim=duration={duracion_lectura:.3f},setpts=N/FRAME_RATE/TB[vpan];"
            )
            logo_idx = 2
        else:
            filtros.append(f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB,fps=30,split=2[vza][vzb];")
            filtros.append(
                f"[vza]crop=iw*{zp['w']}:ih*{zp['h']}:iw*{zp['x']}:ih*{zp['y']},"
                "scale=1080:960:force_original_aspect_ratio=decrease,"
                f"pad=1080:960:(ow-iw)/2:(oh-ih)/2:color=0x{NEGRO}[vpan];"
            )
            logo_idx = 1
        filtros.append(
            f"[vzb]crop=iw*{zc['w']}:ih*{zc['h']}:iw*{zc['x']}:ih*{zc['y']},"
            "scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[vcam];"
        )
        filtros.append("[vpan][vcam]vstack=inputs=2[vf];")
    elif modo == "entrevista":
        def recorte(entrada, zona, salida):
            return (
                f"[{entrada}]crop=iw*{zona['w']}:ih*{zona['h']}:iw*{zona['x']}:ih*{zona['y']},"
                f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[{salida}];"
            )

        preguntas = tramos_de(tramos or [], "entrevistador")
        base = f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB,fps=30"
        if preguntas:
            filtros.append(f"{base},split=2[vea][vei];")
            filtros.append(recorte("vea", zonas_personas["entrevistado"], "vbase"))
            filtros.append(recorte("vei", zonas_personas["entrevistador"], "vover"))
            enable = "+".join(f"between(t\\,{a:.3f}\\,{b:.3f})" for a, b in preguntas)
            filtros.append(f"[vbase][vover]overlay=0:0:enable='{enable}'[vf];")
        else:
            print("  AVISO: ningún segmento marcado como entrevistador — plano fijo del entrevistado")
            filtros.append(f"{base}[vea];")
            filtros.append(recorte("vea", zonas_personas["entrevistado"], "vf"))
        logo_idx = 1
    elif modo == "poster":
        entradas += [
            "-loop", "1", "-framerate", "30", "-t", f"{duracion_lectura:.3f}", "-i", str(poster)
        ]
        filtros.append(
            f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB,fps=30,"
            "scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[vcam];"
        )
        filtros.append(
            f"[1:v]fps=30,scale=1080:960:force_original_aspect_ratio=increase,"
            f"crop=1080:960,trim=duration={duracion_lectura:.3f},setpts=N/FRAME_RATE/TB[vpan];"
        )
        filtros.append("[vpan][vcam]vstack=inputs=2[vf];")
        logo_idx = 2
    else:
        filtros.append(f"[0:v]select='{cond}',setpts=N/FRAME_RATE/TB[vc];")
        if modo == "marco":
            filtros.append(
                "[vc]scale=1080:-2:force_original_aspect_ratio=decrease,"
                f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x{NEGRO}[vf];"
            )
        else:
            filtros.append("[vc]crop=min(iw\\,ih*9/16):ih,scale=1080:1920[vf];")
        logo_idx = 1

    if brand:
        filtros.append(f"[{logo_idx}:v]scale=170:-1[lg];[vf][lg]overlay=W-w-48:H-h-64[vl];")
        filtros.append(f"[vl]ass=filename={ass_path.as_posix()}:fontsdir={FONTS_DIR.as_posix()}[vout];")
    else:
        filtros.append("[vf]null[vout];")
    filtros.append("[ac]loudnorm=I=-16:TP=-1.5:LRA=11[aout]")

    if brand:
        entradas += ["-i", str(LOGO)]
    script = out_path.with_suffix(".filter")
    script.write_text("\n".join(filtros), encoding="utf-8")
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-copyts", *entradas,
                "-filter_complex_script", str(script),
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-crf", "18", "-preset", "faster", "-pix_fmt", "yuv420p",
                "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out_path),
            ],
            check=True,
        )
    finally:
        script.unlink(missing_ok=True)


def _normal(p):
    return p.lower().strip(".,!?¿¡;:\"'()")


def props_remotion(reel, sub_words, duracion, nombre, inicios):
    lineas = [
        {
            "desde": round(l[0]["desde"], 3),
            "hasta": round(l[-1]["hasta"], 3),
            "palabras": [
                {"w": w["w"], "desde": round(w["desde"], 3), "hasta": round(w["hasta"], 3)} for w in l
            ],
        }
        for l in lineas_subtitulo(sub_words)
    ]
    destacadas = []
    for d in reel.get("destacadas", []):
        cerca = [sw for sw in sub_words if abs(sw["orig"] - d["t"]) < 3.0]
        if not cerca:
            print(f"  AVISO: destacada {d} fuera de los cortes del reel — se omite")
            continue
        con_texto = [sw for sw in cerca if _normal(sw["w"]) == _normal(d["palabra"].split()[-1])]
        sw = min(con_texto or cerca, key=lambda x: abs(x["orig"] - d["t"]))
        destacadas.append({"desde": round(sw["desde"], 3), "palabra": d["palabra"]})
    return {
        "video": f"{nombre}.mp4",
        "titulo": reel["titulo"],
        "tipo": reel.get("tipo", "problema"),
        "modo": reel.get("modo", "crop"),
        "duracion": round(duracion, 3),
        "cortes": inicios,
        "destacadas": sorted(destacadas, key=lambda x: x["desde"]),
        "lineas": lineas,
    }


def main(video, sesion_dir, out_dir="media_out", pantalla=None, poster=None, remotion=False,
         muletillas=True):
    sesion = pathlib.Path(sesion_dir)
    manifiesto = json.loads((sesion / "manifiesto_reels.json").read_text(encoding="utf-8-sig"))
    words = json.loads((sesion / "transcript.json").read_text(encoding="utf-8-sig"))["palabras"]
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    familia = font_family()
    offset_pantalla = float(manifiesto.get("offset_pantalla", 0))
    print(
        f"Fuente para subtítulos: {familia}"
        + (f" · pantalla: {pantalla} (offset {offset_pantalla}s)" if pantalla else "")
        + (f" · poster: {poster}" if poster else "")
    )

    for reel in manifiesto["reels"]:
        nombre = f"reel_{reel['n']}_{reel['slug']}"
        print(f"\n== {nombre} ({reel.get('tipo')}, tesis {reel.get('tesis')}, modo {reel.get('modo')}) ==")
        intervalos, sub_words, duracion, inicios, tramos = cortes_sin_silencio(
            reel, words, muletillas=muletillas
        )
        if not intervalos:
            raise ValueError(f"{nombre}: sin intervalos válidos")
        print(
            f"  {len(intervalos)} cortes ({'silencios y muletillas' if muletillas else 'silencios'}"
            f" quitados), duración final {duracion:.1f}s"
            + (f"  ⚠ PASA DE {DURACION_MAX}s" if duracion > DURACION_MAX else "")
        )
        ass_path = out / f"{nombre}.ass"
        if remotion:
            props = props_remotion(reel, sub_words, duracion, nombre, inicios)
            (out / f"{nombre}.props.json").write_text(
                json.dumps(props, ensure_ascii=False, indent=1), encoding="utf-8"
            )
        else:
            escribir_ass(ass_path, reel, sub_words, duracion, familia)
        zonas = reel.get("zonas") or manifiesto.get("zonas")
        zonas_personas = reel.get("zonas_personas") or manifiesto.get("zonas_personas")
        render(
            video, reel, intervalos, ass_path, out / f"{nombre}.mp4",
            pantalla=pantalla, poster=poster, offset_pantalla=offset_pantalla,
            brand=not remotion, zonas=zonas, zonas_personas=zonas_personas, tramos=tramos,
        )
        print(f"  OK → {out / (nombre + '.mp4')}")


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("sesion_dir")
    parser.add_argument("out_dir", nargs="?", default="media_out")
    parser.add_argument("--pantalla")
    parser.add_argument("--poster")
    parser.add_argument("--remotion", action="store_true")
    parser.add_argument("--muletillas", choices=("on", "off"), default="on")
    args = parser.parse_args()
    main(
        args.video, args.sesion_dir, args.out_dir,
        pantalla=args.pantalla, poster=args.poster, remotion=args.remotion,
        muletillas=args.muletillas == "on",
    )


if __name__ == "__main__":
    cli()
