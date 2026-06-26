#!/usr/bin/env python3
"""Contrato único del Motion Content Engine — MANIFIESTO SEMANAL.
Un manifiesto = toda la publicación automática de UNA semana (todas las redes, todos los días).
Se identifica por la FECHA del lunes de esa semana (YYYY-MM-DD). El newsletter va aparte
(newsletters/newsletter_<fecha>.md, Paulo lo publica manual).
NINGÚN componente adivina nada: todo sale de acá."""
import json, os, glob
MANIF_DIR = "manifiestos"

# Canales del manifiesto semanal (Blotato). Twitter aparece 2 veces (misma cuenta, distinto día):
#   x_paulo_hem  = hilo del carrusel HEM (martes)
#   x_paulo_news = hilo derivado del newsletter (jueves)
CANALES = ["linkedin_paulo", "instagram", "x_paulo_hem", "linkedin_motion",
           "instagram_newsletter", "x_paulo_news"]

# Plan editorial (el contenido lo define CALENDARIO_EDITORIAL.md; esto es referencia rápida).
# semana → (tesis, tipo carousel, tipo newsletter)
SEMANAS = {
    1: ("Cambio ≠ Transformación", "problema", "metodo"),
    2: ("Cambio ≠ Transformación", "resultados", "conexion"),
    3: ("Cultura = sistema operativo", "problema", "metodo"),
    4: ("Cultura = sistema operativo", "resultados", "conexion"),
    5: ("Transformación Continua®", "problema", "metodo"),
    6: ("Transformación Continua®", "resultados", "conexion"),
    7: ("Tecnología es commodity", "problema", "metodo"),
    8: ("Tecnología es commodity", "resultados", "conexion"),
}

def ruta(clave): return os.path.join(MANIF_DIR, f"manifiesto_{clave}.json")
def escribir(m):
    os.makedirs(MANIF_DIR, exist_ok=True)
    p = ruta(m["fecha_inicio"])
    json.dump(m, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return p
def leer(clave): return json.load(open(ruta(clave), encoding="utf-8"))
def mas_reciente():
    fs = sorted(glob.glob(os.path.join(MANIF_DIR,"manifiesto_*.json")), key=os.path.getmtime, reverse=True)
    return json.load(open(fs[0], encoding="utf-8")) if fs else None
def pieza(m, canal):
    c = m.get("canales",{}).get(canal)
    return c if (c and c.get("activo")) else None
def validar(m):
    e=[]
    if not m.get("fecha_inicio"): e.append("falta 'fecha_inicio' (YYYY-MM-DD del lunes de la semana)")
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
