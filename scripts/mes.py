#!/usr/bin/env python3
"""Contrato del ESQUEMA MENSUAL — manifiestos/mes_<YYYY-MM>.json.
Un manifiesto mensual = 4 semanas (una tesis por semana) × 4 días (lun problema · mar metodo ·
mié resultados · jue conexion). Cada día una pieza por canal (LinkedIn + Instagram).
Formatos por día: video · carousel_news · post_carousel · faltante_video (publica su fallback).
El detalle del modelo vive en scripts/PROMPT_mes.md y CALENDARIO_EDITORIAL.md."""
import json, os
import datetime as dt

MANIF_DIR = "manifiestos"
CATALOGO = "banco/reels/catalogo.json"
DIAS = ["lun", "mar", "mie", "jue"]
TIPO_ESPERADO = {"lun": "problema", "mar": "metodo", "mie": "resultados", "jue": "conexion"}
FORMATOS = {"video", "carousel_news", "post_carousel", "faltante_video"}


def ruta(mes): return os.path.join(MANIF_DIR, f"mes_{mes}.json")
def leer(mes): return json.load(open(ruta(mes), encoding="utf-8-sig"))
def escribir(m):
    os.makedirs(MANIF_DIR, exist_ok=True)
    p = ruta(m["mes"])
    json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return p


def leer_catalogo():
    return json.load(open(CATALOGO, encoding="utf-8-sig"))


def escribir_catalogo(cat):
    json.dump(cat, open(CATALOGO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def reel_por_id(cat, reel_id):
    for r in cat["reels"]:
        if r["id"] == reel_id: return r
    return None


def fecha_dia(fecha_inicio_iso, dia, hhmm="09:00"):
    """Fecha/hora ISO del día (lun/mar/mie/jue) en la semana que arranca en fecha_inicio_iso."""
    base = dt.date.fromisoformat(fecha_inicio_iso)
    lunes = base - dt.timedelta(days=base.weekday())
    target = lunes + dt.timedelta(days=DIAS.index(dia))
    h, mm = map(int, hhmm.split(":"))
    return dt.datetime(target.year, target.month, target.day, h, mm).strftime("%Y-%m-%dT%H:%M:%SZ")


def validar(m):
    e = []
    if not m.get("mes"): e.append("falta 'mes' (YYYY-MM)")
    semanas = m.get("semanas", [])
    if len(semanas) != 4: e.append(f"se esperan 4 semanas, hay {len(semanas)}")
    for s in semanas:
        fi = s.get("fecha_inicio", "?")
        if not s.get("fecha_inicio"): e.append("semana sin 'fecha_inicio'")
        dias = s.get("dias", {})
        videos = 0
        for d in DIAS:
            dia = dias.get(d)
            if not dia: e.append(f"{fi}: falta el día '{d}'"); continue
            fmt = dia.get("formato")
            if fmt not in FORMATOS: e.append(f"{fi}/{d}: formato inválido '{fmt}'")
            if dia.get("tipo") != TIPO_ESPERADO[d]:
                e.append(f"{fi}/{d}: tipo '{dia.get('tipo')}' — se esperaba '{TIPO_ESPERADO[d]}'")
            if fmt == "video":
                videos += 1
                if not dia.get("reel_id"): e.append(f"{fi}/{d}: formato video sin 'reel_id'")
            if fmt in ("carousel_news", "post_carousel", "faltante_video"):
                if not dia.get("slides"): e.append(f"{fi}/{d}: falta 'slides' del carrusel")
                if not dia.get("carrusel"): e.append(f"{fi}/{d}: falta nombre 'carrusel'")
            if not dia.get("texto_linkedin"): e.append(f"{fi}/{d}: falta 'texto_linkedin'")
            if not dia.get("caption_instagram"): e.append(f"{fi}/{d}: falta 'caption_instagram'")
        faltantes = sum(1 for d in DIAS if dias.get(d, {}).get("formato") == "faltante_video")
        if videos + faltantes != 2:
            e.append(f"{fi}: la semana tiene {videos} videos y {faltantes} faltantes — deben sumar exactamente 2")
    return e
