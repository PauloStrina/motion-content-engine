#!/usr/bin/env python3
"""Genera los PNG del carrusel de un episodio, con nombres derivados del MANIFIESTO.
Garantiza que el nombre y la cantidad coincidan con lo que el publicador espera.
Uso: python generar_carrusel.py <epX-Y> <salida_dir> <ruta_render.py> <dir_slides>"""
import os, sys, json, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M

def main(ep, out_dir, render_py, slides_dir):
    m = M.leer(ep)
    os.makedirs(out_dir, exist_ok=True)
    hizo_algo = False
    # CARRUSEL HEM (episodios carousel: problema/resultados) — solo si instagram tiene carrusel activo
    ig = M.pieza(m, "instagram")
    if ig and ig.get("formato") == "carrusel":
        hizo_algo = True
        base = ig["carrusel"]; n_esperado = ig["carrusel_slides"]
        spec = os.path.join(slides_dir, f"{base}_carrusel.json")
        if not os.path.exists(spec):
            print(f"⚠ No existe {spec}. El Diseñador debe generarlo primero."); sys.exit(1)
        n_real = len(json.load(open(spec))["slides"])
        if n_real != n_esperado:
            print(f"⚠ Manifiesto dice {n_esperado} slides pero el JSON tiene {n_real}. Alineá ambos.")
            ig["carrusel_slides"] = n_real; M.escribir(m)
            print(f"  → Manifiesto actualizado a {n_real} slides.")
        subprocess.run(["python", render_py, spec, out_dir, "--png"], check=True)
        spec_base = os.path.splitext(os.path.basename(spec))[0]
        pngs = sorted(glob.glob(os.path.join(out_dir, f"{spec_base}-*.png")),
                      key=lambda x: int(x.rsplit("-",1)[1].split(".")[0]))
        for i, f in enumerate(pngs, 1):
            dest = os.path.join(out_dir, f"{base}-{i}.png")
            if f != dest: os.rename(f, dest)
        final = sorted(glob.glob(os.path.join(out_dir, f"{base}-*.png")))
        print(f"✓ {len(final)} PNG generados como {base}-N.png (coincide con el publicador)")
        # PDF para LinkedIn carrusel
        lkp = M.pieza(m, "linkedin_paulo")
        if lkp and lkp.get("formato") == "carrusel":
            pdf_dst = os.path.join(out_dir, f"{base}.pdf")
            subprocess.run(["python", render_py, spec, pdf_dst], check=True)
            print(f"✓ PDF generado: {base}.pdf")
    # CARRUSEL NEWSLETTER (episodios newsletter: metodo/conexion) — si existe <ep>_news.json
    news_spec = os.path.join(slides_dir, f"{ep}_news.json")
    if os.path.exists(news_spec):
        hizo_algo = True
        render_news_py = os.path.join(os.path.dirname(render_py), "render_newsletter.py")
        subprocess.run(["python", render_news_py, news_spec, out_dir, "--png"], check=True)
        news_pngs = sorted(glob.glob(os.path.join(out_dir, f"{ep}-news*.png")))
        print(f"✓ {len(news_pngs)} slides del carrusel newsletter como {ep}-news-N.png")
    if not hizo_algo:
        print(f"El episodio {ep} no tiene carrusel HEM ni carrusel newsletter para renderizar.")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
