#!/usr/bin/env python3
"""Contrato único del Motion Content Engine. Estructura del manifiesto por episodio + helpers.
NINGÚN componente adivina nada: todo sale de acá."""
import json, os, glob
MANIF_DIR = "manifiestos"
CANALES = ["linkedin_paulo", "linkedin_motion", "x_paulo", "instagram", "instagram_newsletter"]
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
