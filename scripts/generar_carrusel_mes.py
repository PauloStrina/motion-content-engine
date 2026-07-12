#!/usr/bin/env python3
"""Renderiza TODOS los carruseles del mes (días carousel_news, post_carousel y fallbacks de
faltante_video), inyectando el copy de las slides desde el manifiesto mensual.
Uso: python generar_carrusel_mes.py <mes YYYY-MM> <salida_dir> <ruta_render.py> <dir_slides>"""
import glob, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mes as MES
from generar_carrusel import inject_hem, _merged


def main(mes_id, out_dir, render_py, slides_dir):
    m = MES.leer(mes_id)
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for semana in m["semanas"]:
        for d in MES.DIAS:
            dia = semana["dias"].get(d, {})
            if dia.get("formato") not in ("carousel_news", "post_carousel", "faltante_video"):
                continue
            base = dia["carrusel"]
            spec = os.path.join(slides_dir, f"{base}.json")
            if not os.path.exists(spec):
                print(f"⚠ Falta {spec} (el Diseñador debía generarlo). Abortando."); sys.exit(1)
            merged = _merged(spec, out_dir, dia.get("slides", []), inject_hem)
            subprocess.run(["python", render_py, merged, out_dir, "--png"], check=True)
            spec_base = os.path.splitext(os.path.basename(merged))[0]
            pngs = sorted(glob.glob(os.path.join(out_dir, f"{spec_base}-*.png")),
                          key=lambda x: int(x.rsplit("-", 1)[1].split(".")[0]))
            for i, f in enumerate(pngs, 1):
                dest = os.path.join(out_dir, f"{base}-{i}.png")
                if f != dest: os.rename(f, dest)
            n = len(glob.glob(os.path.join(out_dir, f"{base}-*.png")))
            if n != dia.get("carrusel_slides", n):
                print(f"⚠ {base}: manifiesto dice {dia.get('carrusel_slides')} slides, render produjo {n}")
            print(f"✓ {base}: {n} PNG")
            total += 1
    print(f"\n{total} carruseles del mes renderizados.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
