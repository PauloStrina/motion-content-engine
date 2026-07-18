#!/usr/bin/env python3
"""Valida contratos visuales asociados a un manifiesto mensual.

Compatibilidad:
- Si el manifiesto no declara contrato_visual_version, no exige visuales.
- Si declara contrato_visual_version=1, cada pieza no-video del alcance debe
  apuntar a un contrato visual aprobado.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mes as MES

ALLOWED_EXECUTIONS = {"code", "openai", "hybrid", "reuse"}
ALLOWED_REPRESENTATIONS = {
    "single_concept",
    "concept_map",
    "diagram",
    "typographic",
    "photo_intervention",
    "hybrid",
    "motion",
}
APPROVED_STATES = {"approved", "generated", "final"}
VISUAL_APPROVED_STATES = {"aprobado", "programado", "publicado"}
CONCEPT_ROOT = Path("design-system/concepts").resolve()
REPO_ROOT = Path(".").resolve()


def _iso(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _read_json(path: Path, errors: list[str], label: str) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"{label}: no existe {path}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: JSON inválido en {path}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label}: el contrato debe ser un objeto JSON")
        return None
    return value


def validate_contract(
    contract: dict[str, Any],
    contract_path: Path,
    visual: dict[str, Any],
    label: str,
    require_approved: bool,
    errors: list[str],
) -> None:
    if contract.get("schema_version") != 1:
        errors.append(f"{label}: schema_version debe ser 1")

    piece_id = contract.get("piece_id")
    if not isinstance(piece_id, str) or not piece_id.strip():
        errors.append(f"{label}: falta piece_id")

    status = contract.get("status")
    if status not in {"draft", "approved", "generated", "final"}:
        errors.append(f"{label}: status inválido {status!r}")
    if require_approved and status not in APPROVED_STATES:
        errors.append(f"{label}: contrato visual no aprobado")

    if status in APPROVED_STATES:
        if not contract.get("approved_by"):
            errors.append(f"{label}: falta approved_by")
        if not _iso(contract.get("approved_at")):
            errors.append(f"{label}: approved_at debe ser ISO 8601")

    if not isinstance(contract.get("visual_message"), str) or not contract["visual_message"].strip():
        errors.append(f"{label}: falta visual_message")
    if not isinstance(contract.get("concept"), str) or not contract["concept"].strip():
        errors.append(f"{label}: falta concept")

    representation = contract.get("representation")
    if representation not in ALLOWED_REPRESENTATIONS:
        errors.append(f"{label}: representation inválida {representation!r}")

    execution = contract.get("execution")
    if execution not in ALLOWED_EXECUTIONS:
        errors.append(f"{label}: execution inválida {execution!r}")
    if visual.get("execution") and execution != visual.get("execution"):
        errors.append(
            f"{label}: execution del manifiesto ({visual.get('execution')}) "
            f"no coincide con el contrato ({execution})"
        )

    preview = contract.get("approved_preview")
    if execution == "reuse":
        if not isinstance(preview, str) or not preview:
            errors.append(f"{label}: execution=reuse exige approved_preview")
        else:
            preview_path = (REPO_ROOT / preview).resolve()
            if not _inside(preview_path, REPO_ROOT) or not preview_path.exists():
                errors.append(f"{label}: approved_preview no existe o sale del repositorio: {preview}")

    if execution in {"openai", "hybrid"}:
        generation = contract.get("generation")
        if not isinstance(generation, dict):
            errors.append(f"{label}: {execution} exige bloque generation")
        else:
            if not generation.get("prompt"):
                errors.append(f"{label}: generation.prompt es obligatorio")
            if not generation.get("output"):
                errors.append(f"{label}: generation.output es obligatorio")
            model = generation.get("model", "gpt-image-2-2026-04-21")
            if not isinstance(model, str) or not model.startswith("gpt-image-2"):
                errors.append(f"{label}: modelo de imagen no admitido {model!r}")

            ref = generation.get("reference_image")
            if ref:
                ref_path = (REPO_ROOT / ref).resolve()
                if not _inside(ref_path, REPO_ROOT) or not ref_path.exists():
                    errors.append(f"{label}: reference_image no existe o sale del repositorio: {ref}")

    refs = contract.get("references", [])
    if refs is not None and not isinstance(refs, list):
        errors.append(f"{label}: references debe ser una lista")

    if not _inside(contract_path, CONCEPT_ROOT):
        errors.append(f"{label}: contract_path debe vivir bajo design-system/concepts/")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", required=True)
    parser.add_argument("--semana", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    try:
        manifest = MES.leer(args.mes)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERROR: no se pudo leer el manifiesto: {exc}")
        return 1

    version = manifest.get("contrato_visual_version")
    if version is None:
        print("✓ Manifiesto legacy: contrato visual no exigido")
        return 0
    if version != 1:
        print(f"ERROR: contrato_visual_version no soportado: {version!r}")
        return 1

    errors: list[str] = []
    try:
        weeks = MES.seleccionar_semanas(manifest, args.semana)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    for week in weeks:
        number = week.get("numero", "?")
        for day_key in MES.DIAS:
            day = week.get("dias", {}).get(day_key, {})
            if day.get("formato") == "video":
                continue

            label = f"semana {number}/{day_key}"
            visual = day.get("visual")
            if not isinstance(visual, dict):
                errors.append(f"{label}: falta bloque visual")
                continue

            state = visual.get("estado")
            if state not in {"borrador_para_aprobacion", "aprobado", "programado", "publicado"}:
                errors.append(f"{label}: estado visual inválido {state!r}")
            if args.require_approved and state not in VISUAL_APPROVED_STATES:
                errors.append(f"{label}: visual debe estar aprobado")
            if state in VISUAL_APPROVED_STATES:
                if not visual.get("aprobado_por"):
                    errors.append(f"{label}: falta visual.aprobado_por")
                if not _iso(visual.get("aprobado_en")):
                    errors.append(f"{label}: visual.aprobado_en debe ser ISO 8601")

            execution = visual.get("execution")
            if execution not in ALLOWED_EXECUTIONS:
                errors.append(f"{label}: execution visual inválida {execution!r}")

            raw_path = visual.get("concept_path")
            if not isinstance(raw_path, str) or not raw_path:
                errors.append(f"{label}: falta visual.concept_path")
                continue
            contract_path = (REPO_ROOT / raw_path).resolve()
            if not _inside(contract_path, CONCEPT_ROOT):
                errors.append(f"{label}: concept_path debe vivir bajo design-system/concepts/")
                continue

            contract = _read_json(contract_path, errors, label)
            if contract is not None:
                validate_contract(
                    contract,
                    contract_path,
                    visual,
                    label,
                    args.require_approved,
                    errors,
                )

    if errors:
        print("Conceptos visuales inválidos:")
        for error in errors:
            print(f" - {error}")
        return 1

    scope = f"semana {args.semana}" if args.semana else "mes completo"
    print(f"✓ Conceptos visuales de {args.mes} · {scope} válidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
