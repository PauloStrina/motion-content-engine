#!/usr/bin/env python3
"""Valida especificaciones visuales de todo el ciclo o de una semana."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import mes as MES

TEXT_TYPES = {"futura", "lam", "eco", "lyon", "lyont"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", required=True)
    parser.add_argument("--semana", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--slides-dir", default="design-system/slides")
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    manifest = MES.leer(args.mes)
    errors = MES.validar(
        manifest,
        exigir_aprobado=args.require_approved,
        semana=args.semana,
    )
    slides_dir = Path(args.slides_dir)

    try:
        weeks = MES.seleccionar_semanas(manifest, args.semana)
    except ValueError as exc:
        errors.append(str(exc))
        weeks = []

    for week in weeks:
        for day_key in MES.DIAS:
            day = week.get("dias", {}).get(day_key, {})
            if day.get("formato") not in {"carousel_news", "post_carousel", "faltante_video"}:
                continue
            base = day.get("carrusel")
            path = slides_dir / f"{base}.json"
            if not path.exists():
                errors.append(f"falta {path}")
                continue
            try:
                spec = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{path}: JSON inválido: {exc}")
                continue
            design_slides = spec.get("slides", [])
            copy_slides = day.get("slides", [])
            if len(design_slides) != len(copy_slides):
                errors.append(
                    f"{path}: {len(design_slides)} slides de diseño vs {len(copy_slides)} de copy"
                )
                continue
            for index, (design_slide, copy_slide) in enumerate(zip(design_slides, copy_slides), 1):
                text_blocks = [
                    block for block in design_slide.get("blocks", []) if block.get("type") in TEXT_TYPES
                ]
                lines = copy_slide.get("lineas", [])
                if len(text_blocks) != len(lines):
                    errors.append(
                        f"{path} slide {index}: {len(text_blocks)} bloques de texto vs {len(lines)} líneas"
                    )

    if errors:
        print("Assets inválidos:")
        for error in errors:
            print(f" - {error}")
        return 1
    scope = f"semana {args.semana}" if args.semana else "mes completo"
    print(f"✓ Assets de {args.mes} · {scope} válidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
