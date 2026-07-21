#!/usr/bin/env python3
"""Valida paquetes de revisión de versiones de diseño.

El paquete de revisión es previo a la aprobación visual. No habilita publicación.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_STATUS = {
    "awaiting_selection",
    "selected",
    "approved",
    "rejected",
    "invalidated_reference_mismatch",
}
ALLOWED_FAMILIES = {"line_system", "conceptual_art"}
ALLOWED_CANDIDATE_STATUS = {None, "valid", "invalid", "rejected", "selected"}


def validate_spec(
    spec_path: Path,
    repo_root: Path,
    label: str,
    errors: list[str],
) -> None:
    try:
        spec_json = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: JSON inválido: {exc}")
        return

    if spec_path.name.endswith(".bundle.json"):
        slide_files = spec_json.get("slide_files")
        if not isinstance(slide_files, list) or not slide_files:
            errors.append(f"{label}: el bundle no contiene slide_files")
            return
        for index, raw_path in enumerate(slide_files, 1):
            if not isinstance(raw_path, str) or not raw_path:
                errors.append(f"{label}: slide_files[{index}] inválido")
                continue
            slide_path = (repo_root / raw_path).resolve()
            try:
                slide_path.relative_to(repo_root)
            except ValueError:
                errors.append(f"{label}: placa sale del repositorio: {raw_path}")
                continue
            if not slide_path.exists():
                errors.append(f"{label}: no existe la placa {raw_path}")
                continue
            try:
                slide = json.loads(slide_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{label}: placa JSON inválida {raw_path}: {exc}")
                continue
            if not isinstance(slide, dict) or not isinstance(slide.get("layers"), list):
                errors.append(f"{label}: placa inválida {raw_path}")
        return

    slides = spec_json.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append(f"{label}: el spec no contiene slides")


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
    status = review.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(f"status inválido: {status!r}")

    if status in {"awaiting_selection", "selected", "invalidated_reference_mismatch"}:
        if review.get("publication_blocked") is not True:
            errors.append(f"status={status} exige publication_blocked=true")

    if status == "invalidated_reference_mismatch" and not review.get("invalidation_reason"):
        errors.append("una revisión invalidada exige invalidation_reason")

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

        if status == "invalidated_reference_mismatch":
            if piece.get("candidate_set_status") != "invalid":
                errors.append(f"{piece_id}: candidate_set_status debe ser invalid")
            if not piece.get("candidate_set_reason"):
                errors.append(f"{piece_id}: falta candidate_set_reason")

        candidates = piece.get("candidates")
        if not isinstance(candidates, list) or len(candidates) < 2:
            errors.append(f"{piece_id}: se requieren al menos dos candidatos")
            candidates = []

        versions: set[str] = set()
        candidate_by_version: dict[str, dict] = {}
        for candidate in candidates:
            version = candidate.get("version")
            if not version or version in versions:
                errors.append(f"{piece_id}: versión faltante o duplicada {version!r}")
                continue
            versions.add(version)
            candidate_by_version[version] = candidate

            candidate_status = candidate.get("status")
            if candidate_status not in ALLOWED_CANDIDATE_STATUS:
                errors.append(
                    f"{piece_id}/{version}: status de candidato inválido {candidate_status!r}"
                )
            if status == "invalidated_reference_mismatch" and candidate_status != "invalid":
                errors.append(f"{piece_id}/{version}: debe estar marcado invalid")

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
            validate_spec(spec_path, repo_root, f"{piece_id}/{version}", errors)

        selected = piece.get("selected_version")
        if selected is not None and selected not in versions:
            errors.append(f"{piece_id}: selected_version no existe: {selected!r}")
        if status in {"selected", "approved"} and selected is None:
            errors.append(f"{piece_id}: falta selected_version para status={status}")
        if status == "selected" and selected is not None:
            selected_candidate = candidate_by_version.get(selected, {})
            if selected_candidate.get("status") != "selected":
                errors.append(f"{piece_id}: el candidato seleccionado debe tener status=selected")
        if status == "invalidated_reference_mismatch" and selected is not None:
            errors.append(f"{piece_id}: una revisión invalidada no puede tener selected_version")

    if errors:
        print("Revisión de diseño inválida:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"✓ Revisión de diseño válida: {review_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
