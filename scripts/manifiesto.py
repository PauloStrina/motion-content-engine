#!/usr/bin/env python3
"""Contrato único del Motion Content Engine. Estructura del manifiesto por episodio + helpers.
NINGÚN componente adivina nada: todo sale de acá."""
import json, os, glob
MANIF_DIR = "manifiestos"
CANALES = ["linkedin_paulo", "linkedin_motion", "x_paulo", "instagram", "instagram_newsletter"]

# Modelo editorial de 8 semanas: el TIPO define el FORMATO del episodio.
# carousel  → problema/resultados → canales: linkedin_paulo (PDF), instagram (HEM), x_paulo (hilo), linkedin_motion
# newsletter→ metodo/conexion     → canales: instagram_newsletter (carrusel news), x_paulo (hilo) + newsletter .md (manual)
CAROUSEL_TIPOS = ("problema", "resultados")
NEWSLETTER_TIPOS = ("metodo", "conexion")
CANALES_POR_FORMATO = {
    "carousel": ["linkedin_paulo", "instagram", "x_paulo", "linkedin_motion"],
    "newsletter": ["instagram_newsletter", "x_paulo"],
}
def formato(tipo):
    if tipo in CAROUSEL_TIPOS: return "carousel"
    if tipo in NEWSLETTER_TIPOS: return "newsletter"
    return None
# semana (1-8) → (episodio carousel, episodio newsletter)
SEMANA_EPISODIOS = {
    1: ("ep1-1","ep1-2"), 2: ("ep1-3","ep1-4"),
    3: ("ep2-1","ep2-2"), 4: ("ep2-3","ep2-4"),
    5: ("ep3-1","ep3-2"), 6: ("ep3-3","ep3-4"),
    7: ("ep4-1","ep4-2"), 8: ("ep4-3","ep4-4"),
}
def ruta(ep): return os.path.join(MANIF_DIR, f"manifiesto_{ep}.json")
def escribir(m):
    os.makedirs(MANIF_DIR, exist_ok=True)
    p = ruta(m["episodio"])
    json.dump(m, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return p
def leer(ep): return json.load(open(ruta(ep), encoding="utf-8"))
def mas_reciente():
    fs = sorted(glob.glob(os.path.join(MANIF_DIR,"manifiesto_*.json")), key=os.path.getmtime, reverse=True)
    return json.load(open(fs[0], encoding="utf-8")) if fs else None
def pieza(m, canal):
    c = m.get("canales",{}).get(canal)
    return c if (c and c.get("activo")) else None
def validar(m):
    e=[]
    if not m.get("episodio"): e.append("falta 'episodio'")
    for canal,c in m.get("canales",{}).items():
        if not c.get("activo"): continue
        f=c.get("formato")
        if f=="post" and not c.get("texto"): e.append(f"{canal}: post sin texto")
        if f=="hilo" and not c.get("hilo"): e.append(f"{canal}: hilo sin hilo")
        if f=="carrusel":
            caption_key = "texto" if canal == "linkedin_paulo" else "caption"
            for k in (caption_key,"carrusel","carrusel_slides"):
                if not c.get(k): e.append(f"{canal}: carrusel sin {k}")
    return e
