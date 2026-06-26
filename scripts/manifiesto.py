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
    """Arma la pieza por canal desde los BLOQUES de contenido (carousel / institucional / newsletter).
    Cada bloque agrupa su cabecera (post/caption/hilo) JUNTO con sus slides, para revisarlo en conjunto.
    Devuelve el dict que espera el publicador (formato + texto/caption/hilo + carrusel/carrusel_slides)."""
    C = m.get("carousel", {}); N = m.get("newsletter", {}); I = m.get("institucional", {})
    if canal == "linkedin_paulo":
        t = C.get("post_linkedin")
        return {"formato":"carrusel","texto":t,"carrusel":C.get("carrusel"),"carrusel_slides":C.get("carrusel_slides")} if t else None
    if canal == "instagram":
        cap = C.get("caption_instagram")
        return {"formato":"carrusel","caption":cap,"carrusel":C.get("carrusel"),"carrusel_slides":C.get("carrusel_slides")} if cap else None
    if canal == "x_paulo_hem":
        h = C.get("hilo_twitter")
        return {"formato":"hilo","hilo":h} if h else None
    if canal == "linkedin_motion":
        t = I.get("post_linkedin_motion")
        return {"formato":"post","texto":t} if t else None
    if canal == "instagram_newsletter":
        cap = N.get("caption_instagram")
        return {"formato":"carrusel","caption":cap,"carrusel":N.get("carrusel"),"carrusel_slides":N.get("carrusel_slides")} if cap else None
    if canal == "x_paulo_news":
        h = N.get("hilo_twitter")
        return {"formato":"hilo","hilo":h} if h else None
    return None
def validar(m):
    e=[]
    if not m.get("fecha_inicio"): e.append("falta 'fecha_inicio' (YYYY-MM-DD del lunes de la semana)")
    C = m.get("carousel", {}); N = m.get("newsletter", {})
    if not C.get("slides"): e.append("carousel: falta 'slides' (copy de las 8 slides)")
    if not N.get("slides"): e.append("newsletter: falta 'slides' (copy de las 8 slides)")
    if not C.get("post_linkedin"): e.append("carousel: falta 'post_linkedin' (cabecera del carrusel en LinkedIn)")
    if not C.get("caption_instagram"): e.append("carousel: falta 'caption_instagram'")
    if not N.get("caption_instagram"): e.append("newsletter: falta 'caption_instagram'")
    return e
