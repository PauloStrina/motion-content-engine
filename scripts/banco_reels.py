#!/usr/bin/env python3
"""Ingreso de reels al BANCO (corre en CI, workflow 5-banco-reels).
Toma los MP4 del render (media_out/) + el manifiesto de la sesión (tesis/tipo/título/caption
por reel), copia los aprobados a motion-media/reels/ (clonado en media_repo/) y registra la
metadata en banco/reels/catalogo.json.
Uso: python banco_reels.py <slug_sesion> <dir_mp4s> <dir_media_repo> [--reels 1,3,5|todos]
"""
import json, os, re, shutil, subprocess, sys

CATALOGO = "banco/reels/catalogo.json"
MEDIA_URL_BASE = "https://ops-motionco.github.io/motion-media/reels"


def duracion_video(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
            capture_output=True, text=True, check=True).stdout.strip()
        return round(float(out), 1)
    except Exception:
        return None


def main(slug, dir_mp4, dir_media, seleccion="todos"):
    manif = json.load(open(f"pipelines/video/reels/{slug}/manifiesto_reels.json", encoding="utf-8-sig"))
    cat = json.load(open(CATALOGO, encoding="utf-8-sig"))
    ids_existentes = {r["id"] for r in cat["reels"]}
    aprobados = None if seleccion == "todos" else {int(x) for x in seleccion.split(",")}

    destino = os.path.join(dir_media, "reels")
    os.makedirs(destino, exist_ok=True)
    nuevos = 0
    for reel in manif["reels"]:
        if aprobados is not None and reel["n"] not in aprobados:
            continue
        nombre = f"reel_{reel['n']}_{reel['slug']}"
        origen = os.path.join(dir_mp4, f"{nombre}.mp4")
        if not os.path.exists(origen):
            print(f"  ⏭ {nombre}: no está en {dir_mp4} — se omite")
            continue
        reel_id = f"{slug}_{reel['n']}"
        if reel_id in ids_existentes:
            print(f"  ⏭ {reel_id}: ya está en el banco")
            continue
        archivo = f"{reel_id}.mp4"
        shutil.copy(origen, os.path.join(destino, archivo))
        cat["reels"].append({
            "id": reel_id,
            "sesion": slug,
            "archivo": archivo,
            "url": f"{MEDIA_URL_BASE}/{archivo}",
            "tesis": reel.get("tesis"),
            "tipo": reel.get("tipo"),
            "titulo": reel.get("titulo"),
            "duracion": duracion_video(origen),
            "caption_sugerido": reel.get("caption_instagram", ""),
            "estado": "disponible",
            "reservado_para": None,
        })
        ids_existentes.add(reel_id)
        nuevos += 1
        print(f"  ✓ {reel_id} → banco (tesis {reel.get('tesis')}, tipo {reel.get('tipo')})")

    json.dump(cat, open(CATALOGO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nBanco actualizado: {nuevos} reels nuevos, {len(cat['reels'])} totales.")
    # resumen de stock por tesis+tipo (para saber qué falta grabar)
    stock = {}
    for r in cat["reels"]:
        if r["estado"] == "disponible":
            k = f"T{r['tesis']}/{r['tipo']}"
            stock[k] = stock.get(k, 0) + 1
    print("Stock disponible:", json.dumps(stock, ensure_ascii=False) if stock else "vacío")


if __name__ == "__main__":
    sel = "todos"
    args = sys.argv[1:]
    if "--reels" in args:
        i = args.index("--reels"); sel = args[i + 1]; args = args[:i] + args[i + 2:]
    main(args[0], args[1], args[2], sel)
