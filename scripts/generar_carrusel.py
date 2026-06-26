#!/usr/bin/env python3
"""Genera los PNG/PDF de los carruseles de la SEMANA, con copy tomado del MANIFIESTO.
El copy de cada slide vive en el manifiesto (carousel.slides / newsletter.slides); el JSON
de slides solo aporta DISEÑO (tratamiento/color/fondo). Antes de renderizar, inyectamos el
copy del manifiesto en las slides, así Paulo edita el copy en UN solo lugar (el manifiesto).
Uso: python generar_carrusel.py <fecha> <salida_dir> <ruta_render.py> <dir_slides>"""
import os, sys, json, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M

TEXT_TYPES = {"futura", "lam", "eco", "lyon", "lyont"}

def inject_hem(spec, copy_slides):
    """Mapea, por orden, las líneas de copy del manifiesto a los bloques de texto de cada slide.
    Si la cantidad no coincide, deja el texto que puso el Diseñador (fallback seguro)."""
    for i, s in enumerate(spec.get("slides", [])):
        if i == 0: continue  # la PORTADA es diseño fijo: no se inyecta copy del manifiesto
        if i >= len(copy_slides): break
        lineas = copy_slides[i].get("lineas", [])
        tb = [b for b in s.get("blocks", []) if b.get("type") in TEXT_TYPES]
        if lineas and len(tb) == len(lineas):
            for b, txt in zip(tb, lineas): b["text"] = txt
        elif lineas:
            print(f"  ⚠ slide {i+1}: {len(tb)} bloques de texto vs {len(lineas)} líneas — copy del manifiesto NO inyectado (uso el del diseñador)")
    return spec

# Carrusel newsletter MONOCROMÁTICO (todas las slides el mismo color, lectura ágil):
#   conexion → naranja · metodo → aqua (verde claro Motion)
NEWS_BG = {"conexion": "naranja", "metodo": "aqua"}
def inject_news(spec, copy_slides, bg=None):
    """Carrusel newsletter: un texto por slide (líneas unidas con <br>) y un único color de fondo."""
    for i, s in enumerate(spec.get("slides", [])):
        if bg: s["bg"] = bg
        if i < len(copy_slides):
            lineas = copy_slides[i].get("lineas", [])
            if lineas: s["text"] = "<br>".join(lineas)
    return spec

def _merged(spec_path, out_dir, copy_slides, injector):
    spec = json.load(open(spec_path, encoding="utf-8"))
    injector(spec, copy_slides)
    dst = os.path.join(out_dir, "_merged_" + os.path.basename(spec_path))
    json.dump(spec, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
    return dst

def main(fecha, out_dir, render_py, slides_dir):
    m = M.leer(fecha)
    os.makedirs(out_dir, exist_ok=True)
    hizo_algo = False
    # CARRUSEL HEM — solo si instagram tiene carrusel activo (episodio con carousel)
    ig = M.pieza(m, "instagram")
    if ig and ig.get("formato") == "carrusel":
        hizo_algo = True
        base = ig["carrusel"]; n_esperado = ig["carrusel_slides"]
        spec = os.path.join(slides_dir, f"{base}_carrusel.json")
        if not os.path.exists(spec):
            print(f"⚠ No existe {spec}. El Diseñador debe generarlo primero."); sys.exit(1)
        copy_slides = m.get("carousel", {}).get("slides", [])
        merged = _merged(spec, out_dir, copy_slides, inject_hem)  # inyecta copy del manifiesto
        n_real = len(json.load(open(merged))["slides"])
        if n_real != n_esperado:
            print(f"⚠ Manifiesto dice {n_esperado} slides pero el JSON tiene {n_real}. Alineá ambos.")
            ig["carrusel_slides"] = n_real; M.escribir(m)
        subprocess.run(["python", render_py, merged, out_dir, "--png"], check=True)
        spec_base = os.path.splitext(os.path.basename(merged))[0]
        pngs = sorted(glob.glob(os.path.join(out_dir, f"{spec_base}-*.png")),
                      key=lambda x: int(x.rsplit("-",1)[1].split(".")[0]))
        for i, f in enumerate(pngs, 1):
            dest = os.path.join(out_dir, f"{base}-{i}.png")
            if f != dest: os.rename(f, dest)
        final = sorted(glob.glob(os.path.join(out_dir, f"{base}-*.png")))
        print(f"✓ {len(final)} PNG generados como {base}-N.png")
        # PDF para LinkedIn carrusel
        lkp = M.pieza(m, "linkedin_paulo")
        if lkp and lkp.get("formato") == "carrusel":
            pdf_dst = os.path.join(out_dir, f"{base}.pdf")
            subprocess.run(["python", render_py, merged, pdf_dst], check=True)
            print(f"✓ PDF generado: {base}.pdf")
    # CARRUSEL NEWSLETTER — si existe <fecha>_news.json
    news_spec = os.path.join(slides_dir, f"{fecha}_news.json")
    if os.path.exists(news_spec):
        hizo_algo = True
        copy_slides = m.get("newsletter", {}).get("slides", [])
        bg = NEWS_BG.get(m.get("newsletter", {}).get("tipo"))
        merged = _merged(news_spec, out_dir, copy_slides, lambda sp, cs: inject_news(sp, cs, bg))
        render_news_py = os.path.join(os.path.dirname(render_py), "render_newsletter.py")
        subprocess.run(["python", render_news_py, merged, out_dir, "--png"], check=True)
        news_pngs = sorted(glob.glob(os.path.join(out_dir, f"{fecha}-news*.png")))
        print(f"✓ {len(news_pngs)} slides del carrusel newsletter como {fecha}-news-N.png")
    if not hizo_algo:
        print(f"La semana {fecha} no tiene carrusel HEM ni carrusel newsletter para renderizar.")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
