#!/usr/bin/env python3
"""Genera los PNG del carrusel de un episodio, con nombres derivados del MANIFIESTO.
Garantiza que el nombre y la cantidad coincidan con lo que el publicador espera.
Uso: python generar_carrusel.py <epX-Y> <salida_dir> <ruta_render.py> <dir_slides>"""
import os, sys, json, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M

def main(ep, out_dir, render_py, slides_dir):
    m = M.leer(ep)
    ig = M.pieza(m, "instagram")
    if not ig or ig["formato"] != "carrusel":
        print(f"El episodio {ep} no tiene carrusel activo."); return
    base = ig["carrusel"]; n_esperado = ig["carrusel_slides"]
    spec = os.path.join(slides_dir, f"{base}_carrusel.json")
    if not os.path.exists(spec):
        print(f"⚠ No existe {spec}. El Diseñador debe generarlo primero."); sys.exit(1)
    # contar slides reales del JSON
    n_real = len(json.load(open(spec))["slides"])
    if n_real != n_esperado:
        print(f"⚠ Manifiesto dice {n_esperado} slides pero el JSON tiene {n_real}. Alineá ambos."); 
        # actualizar manifiesto para que coincida (fuente: el JSON real)
        ig["carrusel_slides"] = n_real; M.escribir(m)
        print(f"  → Manifiesto actualizado a {n_real} slides.")
    os.makedirs(out_dir, exist_ok=True)
    # render a PNG
    subprocess.run(["python", render_py, spec, out_dir, "--png"], check=True)
    # renombrar al nombre del carrusel (base-1.png ...)
    spec_base = os.path.splitext(os.path.basename(spec))[0]
    pngs = sorted(glob.glob(os.path.join(out_dir, f"{spec_base}-*.png")),
                  key=lambda x: int(x.rsplit("-",1)[1].split(".")[0]))
    for i, f in enumerate(pngs, 1):
        dest = os.path.join(out_dir, f"{base}-{i}.png")
        if f != dest: os.rename(f, dest)
    final = sorted(glob.glob(os.path.join(out_dir, f"{base}-*.png")))
    print(f"✓ {len(final)} PNG generados como {base}-N.png (coincide con el publicador)")
    for f in final: print(f"   {os.path.basename(f)}")
    # PDF para LinkedIn carrusel (WeasyPrint sin --png)
    lkp = M.pieza(m, "linkedin_paulo")
    if lkp and lkp.get("formato") == "carrusel":
        pdf_dst = os.path.join(out_dir, f"{base}.pdf")
        subprocess.run(["python", render_py, spec, pdf_dst], check=True)
        print(f"✓ PDF generado: {base}.pdf")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
