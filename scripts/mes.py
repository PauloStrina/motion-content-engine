#!/usr/bin/env python3
"""Contrato y validación del manifiesto mensual progresivo de Motion.

La unidad estratégica sigue siendo el mes. El archivo puede completarse y
aprobarse semana por semana. Una operación semanal valida y procesa únicamente
la semana seleccionada; una operación mensual exige las cuatro semanas.
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
        fh.write("\n")
    return path


def leer_catalogo() -> dict[str, Any]:
    with CATALOGO.open(encoding="utf-8-sig") as fh:
        return json.load(fh)


def escribir_catalogo(cat: dict[str, Any]) -> None:
    with CATALOGO.open("w", encoding="utf-8") as fh:
        json.dump(cat, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def reel_por_id(cat: dict[str, Any], reel_id: str) -> dict[str, Any] | None:
    for reel in cat.get("reels", []):
        if reel.get("id") == reel_id:
            return reel
    return None


def numero_semana(week: dict[str, Any], index: int) -> int:
    """Devuelve el número explícito o, por compatibilidad, la posición 1-4."""
    value = week.get("numero", index)
    return value if isinstance(value, int) and not isinstance(value, bool) else -1


def seleccionar_semanas(m: dict[str, Any], semana: int | None = None) -> list[dict[str, Any]]:
    weeks = m.get("semanas", [])
    if not isinstance(weeks, list):
        return []
    if semana is None:
        return weeks
    for index, week in enumerate(weeks, start=1):
        if isinstance(week, dict) and numero_semana(week, index) == semana:
            return [week]
    raise ValueError(f"no existe la semana {semana} en el manifiesto")


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


def _validar_iso8601(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _validar_aprobacion(
    node: dict[str, Any],
    label: str,
    errors: list[str],
    exigir_aprobado: bool,
) -> None:
    estado = node.get("estado")
    if estado not in ESTADOS:
        errors.append(f"{label}: estado inválido {estado!r}")
        return
    if exigir_aprobado and estado not in {"aprobado", "programado", "publicado"}:
        errors.append(f"{label}: debe estar aprobado para esta operación")
    if estado in {"aprobado", "programado", "publicado"}:
        if not node.get("aprobado_por"):
            errors.append(f"{label}: falta 'aprobado_por'")
        approved_at = node.get("aprobado_en")
        if not approved_at:
            errors.append(f"{label}: falta 'aprobado_en'")
        elif not _validar_iso8601(approved_at):
            errors.append(f"{label}: 'aprobado_en' debe ser ISO 8601")


def validar(
    m: dict[str, Any],
    exigir_aprobado: bool = False,
    semana: int | None = None,
) -> list[str]:
    errors: list[str] = []

    mes = m.get("mes")
    if not mes:
        errors.append("falta 'mes' (YYYY-MM)")
    elif not isinstance(mes, str) or len(mes) != 7 or mes[4] != "-":
        errors.append(f"'mes' inválido: {mes!r}")

    first: dt.date | None = None
    if not m.get("primer_lunes"):
        errors.append("falta 'primer_lunes'")
    else:
        try:
            first = dt.date.fromisoformat(m["primer_lunes"])
            if first.weekday() != 0:
                errors.append("'primer_lunes' debe ser lunes")
        except (TypeError, ValueError):
            errors.append("'primer_lunes' no es una fecha ISO válida")

    _validar_aprobacion(m, "manifiesto", errors, exigir_aprobado and semana is None)

    weeks = m.get("semanas", [])
    if not isinstance(weeks, list):
        errors.append("'semanas' debe ser una lista")
        return errors
    if semana is None and len(weeks) != 4:
        errors.append(f"se esperan 4 semanas para operar el mes completo, hay {len(weeks)}")
    if semana is not None and not 1 <= semana <= 4:
        errors.append("'semana' debe ser 1, 2, 3 o 4")
        return errors

    seen_numbers: set[int] = set()
    for index, week in enumerate(weeks, start=1):
        if not isinstance(week, dict):
            errors.append(f"semana_{index}: debe ser un objeto")
            continue
        number = numero_semana(week, index)
        if number not in {1, 2, 3, 4}:
            errors.append(f"semana_{index}: 'numero' debe ser 1, 2, 3 o 4")
        elif number in seen_numbers:
            errors.append(f"semana_{index}: número de semana duplicado ({number})")
        else:
            seen_numbers.add(number)

    try:
        selected = seleccionar_semanas(m, semana)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    for week in selected:
        index = weeks.index(week) + 1
        number = numero_semana(week, index)
        start = week.get("fecha_inicio")
        label = f"semana {number}" if number > 0 else f"semana_{index}"

        _validar_aprobacion(week, label, errors, exigir_aprobado and semana is not None)

        if not start:
            errors.append(f"{label}: falta 'fecha_inicio'")
        else:
            try:
                start_date = dt.date.fromisoformat(start)
                if start_date.weekday() != 0:
                    errors.append(f"{label}: fecha_inicio debe ser lunes")
                if first and number in {1, 2, 3, 4}:
                    expected = first + dt.timedelta(weeks=number - 1)
                    if start_date != expected:
                        errors.append(f"{label}: fecha_inicio no coincide con la secuencia mensual")
            except (TypeError, ValueError):
                errors.append(f"{label}: fecha_inicio inválida")

        days = week.get("dias", {})
        if not isinstance(days, dict):
            errors.append(f"{label}: 'dias' debe ser un objeto")
            continue

        videos = 0
        for day_key in DIAS:
            day = days.get(day_key)
            day_label = f"{label}/{day_key}"
            if not isinstance(day, dict):
                errors.append(f"{label}: falta el día '{day_key}'")
                continue

            fmt = day.get("formato")
            if fmt not in FORMATOS:
                errors.append(f"{day_label}: formato inválido {fmt!r}")
            if day.get("tipo") != TIPO_ESPERADO[day_key]:
                errors.append(
                    f"{day_label}: tipo {day.get('tipo')!r}; se esperaba {TIPO_ESPERADO[day_key]!r}"
                )
            if not day.get("tema"):
                errors.append(f"{day_label}: falta 'tema'")
            if not day.get("texto_linkedin"):
                errors.append(f"{day_label}: falta 'texto_linkedin'")
            if not day.get("caption_instagram"):
                errors.append(f"{day_label}: falta 'caption_instagram'")

            if fmt == "video":
                videos += 1
                if not day.get("reel_id"):
                    errors.append(f"{day_label}: formato video sin 'reel_id'")

            if fmt in {"carousel_news", "post_carousel", "faltante_video"}:
                slides = day.get("slides")
                slide_count = day.get("carrusel_slides")
                if not day.get("carrusel"):
                    errors.append(f"{day_label}: falta 'carrusel'")
                if not isinstance(slides, list) or not slides:
                    errors.append(f"{day_label}: faltan 'slides'")
                elif slide_count != len(slides):
                    errors.append(
                        f"{day_label}: carrusel_slides={slide_count} pero hay {len(slides)} slides"
                    )
                for slide_index, slide in enumerate(slides or [], 1):
                    lines = slide.get("lineas") if isinstance(slide, dict) else None
                    if (
                        not isinstance(lines, list)
                        or not lines
                        or not all(isinstance(value, str) and value.strip() for value in lines)
                    ):
                        errors.append(f"{day_label}: slide {slide_index} sin líneas válidas")

            if fmt == "carousel_news" and not day.get("newsletter"):
                errors.append(f"{day_label}: carousel_news sin ruta de newsletter")

            if fmt == "faltante_video":
                videos += 1
                if not day.get("grabar"):
                    errors.append(f"{day_label}: faltante_video sin instrucción 'grabar'")

        if videos != 2:
            errors.append(f"{label}: videos + faltantes = {videos}; deben ser exactamente 2")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un manifiesto mensual o una semana")
    parser.add_argument("--mes", required=True, help="Mes/ciclo YYYY-MM")
    parser.add_argument("--semana", type=int, choices=(1, 2, 3, 4))
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

    errors = validar(
        manifest,
        exigir_aprobado=args.require_approved,
        semana=args.semana,
    )
    if errors:
        print("Manifiesto inválido:")
        for error in errors:
            print(f" - {error}")
        return 1

    scope = f"semana {args.semana}" if args.semana else "mes completo"
    status = "aprobado" if args.require_approved else "válido"
    print(f"✓ {ruta(args.mes)} · {scope} · {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
