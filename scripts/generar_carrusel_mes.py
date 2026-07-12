#!/usr/bin/env python3
"""Renderiza los carruseles del manifiesto mensual sin reescribir el copy."""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mes as MES

TEXT_TYPES = {"futura", "lam", "eco", "lyon", "lyont"}


def inject_copy(spec: dict, copy_slides: list[dict]) -> dict:
    design_slides = spec.get("slides", [])
    if len(design_slides) != len(copy_slides):
        raise ValueError(
            f"diseño tiene {len(design_slides)} slides y el manifiesto {len(copy_slides)}"
        )
    for index, (design_slide, copy_slide) in enumerate(zip(design_slides, copy_slides), 1):
        lines = copy_slide.get("lineas", [])
        text_blocks = [
            block for block in design_slide.get("blocks", []) if block.get("type") in TEXT_TYPES
        ]
        if len(text_blocks) != len(lines):
            raise ValueError(
                f"slide {index}: {len(text_blocks)} bloques de texto y {len(lines)} líneas"
            )
        for block, line in zip(text_blocks, lines):
            block["text"] = line
    return spec


def merged(spec_path: Path, out_dir: Path, copy_slides: list[dict]) -> Path:
    with spec_path.open(encoding="utf-8") as fh:
        spec = json.load(fh)
    inject_copy(spec, copy_slides)
    destination = out_dir / f"_merged_{spec_path.name}"
    with destination.open("w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=2)
    return destination


def main(month: str, out_dir_raw: str, render_py_raw: str, slides_dir_raw: str) -> int:
    manifest = MES.leer(month)
    errors = MES.validar(manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    out_dir = Path(out_dir_raw)
    render_py = Path(render_py_raw)
    slides_dir = Path(slides_dir_raw)
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0

    for week in manifest["semanas"]:
        for day_key in MES.DIAS:
            day = week["dias"][day_key]
            if day["formato"] not in {"carousel_news", "post_carousel", "faltante_video"}:
                continue
            base = day["carrusel"]
            spec_path = slides_dir / f"{base}.json"
            if not spec_path.exists():
                print(f"ERROR: falta {spec_path}")
                return 1
            try:
                merged_path = merged(spec_path, out_dir, day["slides"])
            except (ValueError, json.JSONDecodeError) as exc:
                print(f"ERROR en {spec_path}: {exc}")
                return 1

            subprocess.run(
                ["python", str(render_py), str(merged_path), str(out_dir), "--png"],
                check=True,
            )
            merged_base = merged_path.stem
            pngs = sorted(
                glob.glob(str(out_dir / f"{merged_base}-*.png")),
                key=lambda path: int(path.rsplit("-", 1)[1].split(".")[0]),
            )
            for index, filename in enumerate(pngs, 1):
                destination = out_dir / f"{base}-{index}.png"
                source = Path(filename)
                if source != destination:
                    source.rename(destination)
            count = len(list(out_dir.glob(f"{base}-*.png")))
            if count != day["carrusel_slides"]:
                print(f"ERROR: {base} produjo {count} PNG; se esperaban {day['carrusel_slides']}")
                return 1
            print(f"✓ {base}: {count} PNG")
            total += 1

    print(f"\n✓ {total} carruseles renderizados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
