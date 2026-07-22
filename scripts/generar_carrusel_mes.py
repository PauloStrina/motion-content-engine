#!/usr/bin/env python3
"""Renderiza los assets visuales de una semana o mes sin reescribir copy bloqueado."""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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
        return {"episodio": data.get("episodio", path.stem), "slides": slides}
    return data


def inject_copy(spec: dict, copy_slides: list[dict]) -> dict:
    design_slides = spec.get("slides", [])
    if len(design_slides) != len(copy_slides):
        raise ValueError(f"diseño tiene {len(design_slides)} slides y el manifiesto {len(copy_slides)}")
    for index, (design_slide, copy_slide) in enumerate(zip(design_slides, copy_slides), 1):
        lines = copy_slide.get("lineas", [])
        text_blocks = [b for b in design_slide.get("blocks", []) if b.get("type") in TEXT_TYPES]
        if len(text_blocks) != len(lines):
            raise ValueError(f"slide {index}: {len(text_blocks)} bloques de texto y {len(lines)} líneas")
        for block, line in zip(text_blocks, lines):
            block["text"] = line
    return spec


def write_temp(spec: dict, out_dir: Path, name: str) -> Path:
    path = out_dir / f"_spec_{name}.json"
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def render_pngs(render_py: Path, spec_path: Path, out_dir: Path, base: str, expected: int) -> None:
    subprocess.run(["python", str(render_py), str(spec_path), str(out_dir), "--png"], check=True)
    source_base = spec_path.stem
    pngs = sorted(
        glob.glob(str(out_dir / f"{source_base}-*.png")),
        key=lambda value: int(value.rsplit("-", 1)[1].split(".")[0]),
    )
    for index, filename in enumerate(pngs, 1):
        destination = out_dir / f"{base}-{index}.png"
        source = Path(filename)
        if source != destination:
            source.replace(destination)
    count = len(list(out_dir.glob(f"{base}-*.png")))
    if count != expected:
        raise ValueError(f"{base} produjo {count} PNG; se esperaban {expected}")
    print(f"✓ {base}: {count} PNG")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mes")
    parser.add_argument("out_dir")
    parser.add_argument("render_py")
    parser.add_argument("slides_dir")
    parser.add_argument("--semana", type=int, choices=(1, 2, 3, 4))
    args = parser.parse_args()

    manifest = MES.leer(args.mes)
    errors = MES.validar(manifest, semana=args.semana)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    out_dir = Path(args.out_dir)
    render_py = Path(args.render_py)
    slides_dir = Path(args.slides_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0

    for week in MES.seleccionar_semanas(manifest, args.semana):
        for day_key in MES.DIAS:
            day = week["dias"][day_key]

            static_spec_raw = day.get("imagen_linkedin_spec")
            static_base = day.get("imagen_linkedin")
            if static_spec_raw and static_base:
                static_path = Path(static_spec_raw)
                spec = load_spec(static_path)
                temp = write_temp(spec, out_dir, static_base)
                render_pngs(render_py, temp, out_dir, static_base, 1)
                total += 1

            if day["formato"] not in {"carousel_news", "post_carousel", "faltante_video"}:
                continue
            base = day["carrusel"]
            raw_spec = day.get("visual_spec")
            spec_path = Path(raw_spec) if raw_spec else slides_dir / f"{base}.json"
            if not spec_path.exists():
                print(f"ERROR: falta {spec_path}")
                return 1
            try:
                spec = load_spec(spec_path)
                if not day.get("copy_locked", False):
                    inject_copy(spec, day["slides"])
                temp = write_temp(spec, out_dir, base)
                render_pngs(render_py, temp, out_dir, base, day["carrusel_slides"])
            except (ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
                print(f"ERROR en {spec_path}: {exc}")
                return 1
            total += 1

    print(f"\n✓ {total} assets visuales renderizados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
