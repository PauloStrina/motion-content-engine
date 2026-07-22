#!/usr/bin/env python3
"""Valida specs visuales para una semana o mes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import mes as MES

TEXT_TYPES = {"futura", "lam", "eco", "lyon", "lyont", "gotham"}
REPO_ROOT = Path(".").resolve()


def load_spec(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if path.name.endswith(".bundle.json"):
        slides = []
        for raw in data.get("slide_files", []):
            slide_path = (REPO_ROOT / raw).resolve()
            slide_path.relative_to(REPO_ROOT)
            slides.append(json.loads(slide_path.read_text(encoding="utf-8")))
        return {"slides": slides}
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", required=True)
    parser.add_argument("--semana", type=int, choices=(1,2,3,4))
    parser.add_argument("--slides-dir", default="design-system/slides")
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    manifest = MES.leer(args.mes)
    errors = MES.validar(manifest, exigir_aprobado=args.require_approved, semana=args.semana)
    slides_dir = Path(args.slides_dir)

    for week in MES.seleccionar_semanas(manifest, args.semana):
        for day_key in MES.DIAS:
            day = week.get("dias", {}).get(day_key, {})
            static_spec = day.get("imagen_linkedin_spec")
            if day.get("imagen_linkedin") and not static_spec:
                errors.append(f"semana {week.get('numero')}/{day_key}: falta imagen_linkedin_spec")
            if static_spec:
                path = Path(static_spec)
                if not path.exists():
                    errors.append(f"falta {path}")
                else:
                    try:
                        if len(load_spec(path).get("slides", [])) != 1:
                            errors.append(f"{path}: la imagen de LinkedIn debe tener una placa")
                    except (json.JSONDecodeError, ValueError) as exc:
                        errors.append(f"{path}: {exc}")

            if day.get("formato") not in {"carousel_news", "post_carousel", "faltante_video"}:
                continue
            base = day.get("carrusel")
            path = Path(day.get("visual_spec")) if day.get("visual_spec") else slides_dir / f"{base}.json"
            if not path.exists():
                errors.append(f"falta {path}")
                continue
            try:
                spec = load_spec(path)
            except (json.JSONDecodeError, ValueError) as exc:
                errors.append(f"{path}: {exc}")
                continue
            design_slides = spec.get("slides", [])
            copy_slides = day.get("slides", [])
            if len(design_slides) != len(copy_slides):
                errors.append(f"{path}: {len(design_slides)} slides de diseño vs {len(copy_slides)} de copy")
                continue
            if day.get("copy_locked", False):
                continue
            for index, (design_slide, copy_slide) in enumerate(zip(design_slides, copy_slides), 1):
                text_blocks = [b for b in design_slide.get("blocks", []) if b.get("type") in TEXT_TYPES]
                lines = copy_slide.get("lineas", [])
                if len(text_blocks) != len(lines):
                    errors.append(f"{path} slide {index}: {len(text_blocks)} bloques de texto vs {len(lines)} líneas")

    if errors:
        print("Assets mensuales inválidos:")
        for error in errors:
            print(f" - {error}")
        return 1
    scope = f"semana {args.semana}" if args.semana else "mes completo"
    print(f"✓ Assets de {args.mes} · {scope} válidos")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
