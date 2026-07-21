#!/usr/bin/env python3
"""Valida paquetes de revisión de versiones de diseño.

El paquete de revisión es previo a la aprobación visual. No habilita publicación.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_STATUS = {"awaiting_selection", "selected", "approved", "rejected"}
ALLOWED_FAMILIES = {"line_system", "conceptual_art"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", help="Ruta a review.json")
    args = parser.parse_args()

    review_path = Path(args.review)
    repo_root = Path(".").resolve()
    errors: list[str] = []

    if not review_path.exists():
        print(f"ERROR: no existe {review_path}")
        return 1

    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON inválido: {exc}")
        return 1

    if review.get("schema_version") != 1:
        errors.append("schema_version debe ser 1")
    if review.get("status") not in ALLOWED_STATUS:
        errors.append(f"status inválido: {review.get('status')!r}")

    pieces = review.get("pieces")
    if not isinstance(pieces, list) or not pieces:
        errors.append("pieces debe ser una lista no vacía")
        pieces = []

    piece_ids: set[str] = set()
    for piece in pieces:
        piece_id = piece.get("piece_id")
        if not piece_id or piece_id in piece_ids:
            errors.append(f"piece_id faltante o duplicado: {piece_id!r}")
            continue
        piece_ids.add(piece_id)

        family = piece.get("visual_family")
        if family not in ALLOWED_FAMILIES:
            errors.append(f"{piece_id}: visual_family inválida {family!r}")

        candidates = piece.get("candidates")
        if not isinstance(candidates, list) or len(candidates) < 2:
            errors.append(f"{piece_id}: se requieren al menos dos candidatos")
            candidates = []

        versions: set[str] = set()
        for candidate in candidates:
            version = candidate.get("version")
            if not version or version in versions:
                errors.append(f"{piece_id}: versión faltante o duplicada {version!r}")
                continue
            versions.add(version)
            spec = candidate.get("spec")
            if not isinstance(spec, str) or not spec:
                errors.append(f"{piece_id}/{version}: falta spec")
                continue
            spec_path = (repo_root / spec).resolve()
            try:
                spec_path.relative_to(repo_root)
            except ValueError:
                errors.append(f"{piece_id}/{version}: spec sale del repositorio")
                continue
            if not spec_path.exists():
                errors.append(f"{piece_id}/{version}: no existe {spec}")
                continue
            try:
                spec_json = json.loads(spec_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{piece_id}/{version}: JSON inválido: {exc}")
                continue
            slides = spec_json.get("slides")
            if not isinstance(slides, list) or not slides:
                errors.append(f"{piece_id}/{version}: el spec no contiene slides")

        selected = piece.get("selected_version")
        if selected is not None and selected not in versions:
            errors.append(f"{piece_id}: selected_version no existe: {selected!r}")
        if review.get("status") in {"selected", "approved"} and selected is None:
            errors.append(f"{piece_id}: falta selected_version para status={review.get('status')}")

    if errors:
        print("Revisión de diseño inválida:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"✓ Revisión de diseño válida: {review_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
