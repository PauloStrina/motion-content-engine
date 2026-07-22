#!/usr/bin/env python3
"""Aplica una aprobación registrada al manifiesto de la ejecución en curso."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} debe contener un objeto JSON")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approval", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    approval_path = Path(args.approval)
    manifest_path = Path(args.manifest)
    approval = read_json(approval_path)
    manifest = read_json(manifest_path)

    if approval.get("status") != "approved_for_live":
        raise ValueError("La autorización no habilita live")
    if approval.get("live_authorized") is not True:
        raise ValueError("live_authorized debe ser true")
    if approval.get("content_approved") is not True or approval.get("visual_approved") is not True:
        raise ValueError("La aprobación editorial y visual debe estar completa")
    if approval.get("mes") != manifest.get("mes"):
        raise ValueError("La aprobación corresponde a otro mes")

    week_number = approval.get("semana")
    selected = None
    for week in manifest.get("semanas", []):
        if isinstance(week, dict) and week.get("numero") == week_number:
            selected = week
            break
    if selected is None:
        raise ValueError(f"No existe la semana {week_number} en el manifiesto")

    approved_by = approval.get("approved_by")
    approved_at = approval.get("approved_at")
    if not approved_by or not approved_at:
        raise ValueError("La aprobación debe registrar autor y fecha")

    selected["estado"] = "aprobado"
    selected["aprobado_por"] = approved_by
    selected["aprobado_en"] = approved_at

    for day_key, day in selected.get("dias", {}).items():
        if not isinstance(day, dict) or day.get("formato") == "video":
            continue
        visual = day.get("visual")
        if not isinstance(visual, dict):
            raise ValueError(f"La pieza {day_key} no contiene bloque visual")
        visual["estado"] = "aprobado"
        visual["aprobado_por"] = approved_by
        visual["aprobado_en"] = approved_at
        visual["execution"] = "reuse"

    write_json(manifest_path, manifest)
    print(
        f"✓ Aprobación {approval.get('approval_id')} aplicada a "
        f"{manifest.get('mes')} · semana {week_number}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
