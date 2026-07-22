#!/usr/bin/env python3
"""Ensambla un spec de carrusel desde archivos JSON de placas."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle")
    parser.add_argument("output")
    args = parser.parse_args()

    repo_root = Path(".").resolve()
    bundle_path = Path(args.bundle)
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

    slide_files = bundle.get("slide_files")
    if not isinstance(slide_files, list) or not slide_files:
        raise ValueError("slide_files debe ser una lista no vacía")

    slides = []
    for raw_path in slide_files:
        path = (repo_root / raw_path).resolve()
        path.relative_to(repo_root)
        slide = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(slide, dict):
            raise ValueError(f"Placa inválida: {raw_path}")
        slides.append(slide)

    spec = {
        "episodio": bundle.get("episodio", bundle_path.stem),
        "slides": slides,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK: {output_path} · {len(slides)} placas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
