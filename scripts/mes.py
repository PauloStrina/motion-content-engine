#!/usr/bin/env python3
"""Contrato y validación del manifiesto mensual de Motion.

Un manifiesto contiene 4 semanas × 4 días y el copy final aprobado para
LinkedIn de Paulo e Instagram de Motion. El repositorio no completa ni
reescribe campos faltantes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

MANIF_DIR = Path("manifiestos")
CATALOGO = Path("banco/reels/catalogo.json")
DIAS = ["lun", "mar", "mie", "jue"]
TIPO_ESPERADO = {
    "lun": "problema",
    "mar": "metodo",
    "mie": "resultados",
    "jue": "conexion",
}
FORMATOS = {"video", "carousel_news", "post_carousel", "faltante_video"}
ESTADOS = {"borrador_para_aprobacion", "aprobado", "programado", "publicado"}
DEFAULT_TIMEZONE = "America/Argentina/Buenos_Aires"


def ruta(mes: str) -> Path:
    return MANIF_DIR / f"mes_{mes}.json"


def leer(mes: str) -> dict[str, Any]:
    with ruta(mes).open(encoding="utf-8-sig") as fh:
        return json.load(fh)


def escribir(m: dict[str, Any]) -> Path:
    MANIF_DIR.mkdir(parents=True, exist_ok=True)
    path = ruta(m["mes"])
    with path.open("w", encoding="utf-8") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return path


def leer_catalogo() -> dict[str, Any]:
    with CATALOGO.open(encoding="utf-8-sig") as fh:
        return json.load(fh)


def escribir_catalogo(cat: dict[str, Any]) -> None:
    with CATALOGO.open("w", encoding="utf-8") as fh:
        json.dump(cat, fh, ensure_ascii=False, indent=1)


def reel_por_id(cat: dict[str, Any], reel_id: str) -> dict[str, Any] | None:
    for reel in cat.get("reels", []):
        if reel.get("id") == reel_id:
            return reel
    return None


def fecha_dia(
    fecha_inicio_iso: str,
    dia: str,
    hhmm: str = "09:00",
    timezone_name: str | None = None,
) -> str:
    """Convierte día/hora editorial local a timestamp UTC ISO 8601."""
    if dia not in DIAS:
        raise ValueError(f"día inválido: {dia}")
    base = dt.date.fromisoformat(fecha_inicio_iso)
    lunes = base - dt.timedelta(days=base.weekday())
    target = lunes + dt.timedelta(days=DIAS.index(dia))
    hour, minute = map(int, hhmm.split(":"))
    tz_name = timezone_name or os.environ.get("MOTION_TIMEZONE", DEFAULT_TIMEZONE)
    local_dt = dt.datetime(target.year, target.month, target.day, hour, minute, tzinfo=ZoneInfo(tz_name))
    return local_dt.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _validar_iso8601(value: str) -> bool:
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (TypeError, ValueError):
        return False


def validar(m: dict[str, Any], exigir_aprobado: bool = False) -> list[str]:
    errors: list[str] = []

    mes = m.get("mes")
    if not mes:
        errors.append("falta 'mes' (YYYY-MM)")
    elif len(mes) != 7 or mes[4] != "-":
        errors.append(f"'mes' inválido: {mes!r}")

    if not m.get("primer_lunes"):
        errors.append("falta 'primer_lunes'")
    else:
        try:
            first = dt.date.fromisoformat(m["primer_lunes"])
            if first.weekday() != 0:
                errors.append("'primer_lunes' debe ser lunes")
        except ValueError:
            errors.append("'primer_lunes' no es una fecha ISO válida")

    estado = m.get("estado")
    if estado not in ESTADOS:
        errors.append(f"estado inválido: {estado!r}")
    if exigir_aprobado and estado not in {"aprobado", "programado", "publicado"}:
        errors.append("el manifiesto debe estar aprobado para esta operación")
    if estado in {"aprobado", "programado", "publicado"}:
        if not m.get("aprobado_por"):
            errors.append("falta 'aprobado_por'")
        approved_at = m.get("aprobado_en")
        if not approved_at:
            errors.append("falta 'aprobado_en'")
        elif not _validar_iso8601(approved_at):
            errors.append("'aprobado_en' debe ser ISO 8601")

    weeks = m.get("semanas", [])
    if len(weeks) != 4:
        errors.append(f"se esperan 4 semanas, hay {len(weeks)}")

    expected_first: dt.date | None = None
    try:
        expected_first = dt.date.fromisoformat(m.get("primer_lunes", ""))
    except ValueError:
        pass

    for index, week in enumerate(weeks):
        start = week.get("fecha_inicio")
        label = start or f"semana_{index + 1}"
        if not start:
            errors.append(f"{label}: falta 'fecha_inicio'")
        else:
            try:
                start_date = dt.date.fromisoformat(start)
                if start_date.weekday() != 0:
                    errors.append(f"{label}: fecha_inicio debe ser lunes")
                if expected_first and start_date != expected_first + dt.timedelta(weeks=index):
                    errors.append(f"{label}: fecha_inicio no coincide con la secuencia mensual")
            except ValueError:
                errors.append(f"{label}: fecha_inicio inválida")

        days = week.get("dias", {})
        videos = 0
        for day_key in DIAS:
            day = days.get(day_key)
            if not day:
                errors.append(f"{label}: falta el día '{day_key}'")
                continue

            fmt = day.get("formato")
            if fmt not in FORMATOS:
                errors.append(f"{label}/{day_key}: formato inválido {fmt!r}")
            if day.get("tipo") != TIPO_ESPERADO[day_key]:
                errors.append(
                    f"{label}/{day_key}: tipo {day.get('tipo')!r}; se esperaba {TIPO_ESPERADO[day_key]!r}"
                )
            if not day.get("tema"):
                errors.append(f"{label}/{day_key}: falta 'tema'")
            if not day.get("texto_linkedin"):
                errors.append(f"{label}/{day_key}: falta 'texto_linkedin'")
            if not day.get("caption_instagram"):
                errors.append(f"{label}/{day_key}: falta 'caption_instagram'")

            if fmt == "video":
                videos += 1
                if not day.get("reel_id"):
                    errors.append(f"{label}/{day_key}: formato video sin 'reel_id'")

            if fmt in {"carousel_news", "post_carousel", "faltante_video"}:
                slides = day.get("slides")
                slide_count = day.get("carrusel_slides")
                if not day.get("carrusel"):
                    errors.append(f"{label}/{day_key}: falta 'carrusel'")
                if not isinstance(slides, list) or not slides:
                    errors.append(f"{label}/{day_key}: faltan 'slides'")
                elif slide_count != len(slides):
                    errors.append(
                        f"{label}/{day_key}: carrusel_slides={slide_count} pero hay {len(slides)} slides"
                    )
                for slide_index, slide in enumerate(slides or [], 1):
                    lines = slide.get("lineas") if isinstance(slide, dict) else None
                    if not isinstance(lines, list) or not lines or not all(isinstance(x, str) and x.strip() for x in lines):
                        errors.append(f"{label}/{day_key}: slide {slide_index} sin líneas válidas")

            if fmt == "carousel_news" and not day.get("newsletter"):
                errors.append(f"{label}/{day_key}: carousel_news sin ruta de newsletter")

            if fmt == "faltante_video":
                videos += 1
                if not day.get("grabar"):
                    errors.append(f"{label}/{day_key}: faltante_video sin instrucción 'grabar'")

        if videos != 2:
            errors.append(f"{label}: videos + faltantes = {videos}; deben ser exactamente 2")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un manifiesto mensual")
    parser.add_argument("--mes", required=True, help="Mes YYYY-MM")
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    try:
        manifest = leer(args.mes)
    except FileNotFoundError:
        print(f"ERROR: no existe {ruta(args.mes)}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON inválido en {ruta(args.mes)}: {exc}")
        return 1

    errors = validar(manifest, exigir_aprobado=args.require_approved)
    if errors:
        print("Manifiesto mensual inválido:")
        for error in errors:
            print(f" - {error}")
        return 1

    status = "aprobado" if args.require_approved else "válido"
    print(f"✓ {ruta(args.mes)} {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
