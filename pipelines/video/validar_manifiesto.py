#!/usr/bin/env python3
"""Valida manifiesto_reels.json contra transcript.json.

Falla con código distinto de cero cuando el editor no generó un manifiesto utilizable.
Se usa después del agente editorial y nuevamente antes del render.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from typing import Any

TIPOS = {"problema", "metodo", "resultados", "conexion"}
MODOS = {"auto", "crop", "marco", "split", "zonas", "poster"}


def cargar_json(path: pathlib.Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        raise ValueError(f"no existe {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}: {exc}") from None


def numero(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def validar_zona(zona: Any, nombre: str, errores: list[str]) -> None:
    if not isinstance(zona, dict):
        errores.append(f"{nombre}: debe ser un objeto x,y,w,h")
        return
    faltan = [k for k in ("x", "y", "w", "h") if not numero(zona.get(k))]
    if faltan:
        errores.append(f"{nombre}: faltan valores numéricos {', '.join(faltan)}")
        return
    x, y, w, h = (float(zona[k]) for k in ("x", "y", "w", "h"))
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > 1.0001 or y + h > 1.0001:
        errores.append(f"{nombre}: coordenadas fuera del rango 0-1 ({x},{y},{w},{h})")


def existe_cerca(valor: float, candidatos: list[float], tolerancia: float = 0.025) -> bool:
    return any(abs(valor - c) <= tolerancia for c in candidatos)


def validar(sesion: pathlib.Path, stage: str, min_s: float, max_s: float) -> list[str]:
    errores: list[str] = []
    try:
        manifiesto = cargar_json(sesion / "manifiesto_reels.json")
        transcript = cargar_json(sesion / "transcript.json")
    except ValueError as exc:
        return [str(exc)]

    if not isinstance(manifiesto, dict):
        return ["manifiesto_reels.json debe ser un objeto JSON"]
    palabras = transcript.get("palabras") if isinstance(transcript, dict) else None
    if not isinstance(palabras, list) or not palabras:
        errores.append("transcript.json no contiene una lista no vacía en 'palabras'")
        palabras = []

    inicios = [float(w["desde"]) for w in palabras if isinstance(w, dict) and numero(w.get("desde"))]
    finales = [float(w["hasta"]) for w in palabras if isinstance(w, dict) and numero(w.get("hasta"))]

    reels = manifiesto.get("reels")
    if not isinstance(reels, list) or not reels:
        errores.append("'reels' debe ser una lista no vacía")
        return errores

    vistos_n: set[int] = set()
    vistos_slug: set[str] = set()
    zonas_raiz = manifiesto.get("zonas")

    for i, reel in enumerate(reels, start=1):
        pref = f"reel[{i}]"
        if not isinstance(reel, dict):
            errores.append(f"{pref}: debe ser un objeto")
            continue

        n = reel.get("n")
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
            errores.append(f"{pref}.n: debe ser entero positivo")
        elif n in vistos_n:
            errores.append(f"{pref}.n: duplicado ({n})")
        else:
            vistos_n.add(n)

        slug = reel.get("slug")
        if not isinstance(slug, str) or not slug.strip():
            errores.append(f"{pref}.slug: requerido")
        elif slug in vistos_slug:
            errores.append(f"{pref}.slug: duplicado ({slug})")
        else:
            vistos_slug.add(slug)

        titulo = reel.get("titulo")
        if not isinstance(titulo, str) or not titulo.strip():
            errores.append(f"{pref}.titulo: requerido")
        elif len(titulo) > 42:
            errores.append(f"{pref}.titulo: demasiado largo ({len(titulo)} caracteres; máximo 42)")

        if reel.get("tesis") not in {1, 2, 3, 4}:
            errores.append(f"{pref}.tesis: debe ser 1, 2, 3 o 4")
        if reel.get("tipo") not in TIPOS:
            errores.append(f"{pref}.tipo: debe ser uno de {sorted(TIPOS)}")

        modo = reel.get("modo", "auto")
        if modo not in MODOS:
            errores.append(f"{pref}.modo: valor no soportado '{modo}'")
        if stage == "render" and modo == "auto":
            errores.append(f"{pref}.modo: quedó en 'auto'; resolver_layout.py no lo resolvió")

        zonas = reel.get("zonas") or zonas_raiz
        if modo == "zonas":
            if not isinstance(zonas, dict):
                errores.append(f"{pref}: modo zonas sin coordenadas")
            else:
                validar_zona(zonas.get("pantalla"), f"{pref}.zonas.pantalla", errores)
                validar_zona(zonas.get("camara"), f"{pref}.zonas.camara", errores)

        segmentos = reel.get("segmentos")
        if not isinstance(segmentos, list) or not segmentos:
            errores.append(f"{pref}.segmentos: lista no vacía requerida")
            continue

        duracion = 0.0
        ultimo_hasta = -1.0
        for j, seg in enumerate(segmentos, start=1):
            sp = f"{pref}.segmentos[{j}]"
            if not isinstance(seg, dict) or not numero(seg.get("desde")) or not numero(seg.get("hasta")):
                errores.append(f"{sp}: requiere desde/hasta numéricos")
                continue
            desde, hasta = float(seg["desde"]), float(seg["hasta"])
            if desde < 0 or hasta <= desde:
                errores.append(f"{sp}: rango inválido {desde}-{hasta}")
                continue
            if desde < ultimo_hasta - 0.01:
                errores.append(f"{sp}: segmentos fuera de orden o superpuestos")
            ultimo_hasta = hasta
            duracion += hasta - desde
            if inicios and not existe_cerca(desde, inicios):
                errores.append(f"{sp}.desde={desde} no coincide con inicio de palabra del transcript")
            if finales and not existe_cerca(hasta, finales):
                errores.append(f"{sp}.hasta={hasta} no coincide con final de palabra del transcript")

        if duracion < min_s or duracion > max_s:
            errores.append(f"{pref}: duración hablada {duracion:.2f}s fuera de {min_s:.0f}-{max_s:.0f}s")

        caption = reel.get("caption_instagram")
        if not isinstance(caption, str) or len(caption.strip()) < 40:
            errores.append(f"{pref}.caption_instagram: requerido y debe tener contenido sustantivo")

    return errores


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sesion_dir", type=pathlib.Path)
    parser.add_argument("--stage", choices=("guion", "render"), default="guion")
    parser.add_argument("--min-seconds", type=float, default=20)
    parser.add_argument("--max-seconds", type=float, default=62)
    args = parser.parse_args()

    errores = validar(args.sesion_dir, args.stage, args.min_seconds, args.max_seconds)
    if errores:
        print("MANIFIESTO INVÁLIDO:", file=sys.stderr)
        for error in errores:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.sesion_dir / 'manifiesto_reels.json'} validado para etapa {args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
