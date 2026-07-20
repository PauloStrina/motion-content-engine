#!/usr/bin/env python3
"""Valida contratos visuales asociados a un manifiesto mensual.

Compatibilidad:
- Sin contrato_visual_version: manifiesto legacy, no exige visuales.
- contrato_visual_version=1: admite contratos visuales v1.
- contrato_visual_version=2: exige familia visual única y contrato v2.
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
FAMILY_CONFIG_PATH = Path("design-system/visual-language/FAMILIAS_VISUALES.json")


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


def _load_families(errors: list[str]) -> dict[str, Any]:
    raw = _read_json(FAMILY_CONFIG_PATH, errors, "familias visuales")
    if raw is None:
        return {}
    families = raw.get("families")
    if not isinstance(families, dict) or not families:
        errors.append("familias visuales: falta objeto families")
        return {}
    return families


def _validate_generation(
    contract: dict[str, Any], execution: str, label: str, errors: list[str]
) -> None:
    if execution not in {"openai", "hybrid"}:
        return
    generation = contract.get("generation")
    if not isinstance(generation, dict):
        errors.append(f"{label}: {execution} exige bloque generation")
        return
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


def _validate_v2(
    contract: dict[str, Any],
    execution: str,
    label: str,
    families: dict[str, Any],
    errors: list[str],
) -> None:
    family_id = contract.get("visual_family")
    if family_id not in families:
        errors.append(f"{label}: visual_family inválida {family_id!r}")
        return
    family = families[family_id]

    if contract.get("family_lock") is not True:
        errors.append(f"{label}: family_lock debe ser true")

    rationale = contract.get("conceptual_rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append(f"{label}: falta conceptual_rationale")

    resources = contract.get("visual_resources")
    if not isinstance(resources, list) or not resources:
        errors.append(f"{label}: visual_resources debe ser una lista no vacía")
        resources = []
    allowed = set(family.get("allowed_resources", []))
    forbidden = set(family.get("forbidden_resources", []))
    unknown = sorted(set(resources) - allowed)
    contamination = sorted(set(resources) & forbidden)
    if unknown:
        errors.append(
            f"{label}: recursos no admitidos para {family_id}: {', '.join(unknown)}"
        )
    if contamination:
        errors.append(
            f"{label}: contaminación de familia detectada: {', '.join(contamination)}"
        )

    exclusions = contract.get("exclusions")
    if not isinstance(exclusions, list) or not exclusions:
        errors.append(f"{label}: exclusions debe declarar recursos excluidos")

    if contract.get("quality_target") != "reference_grade":
        errors.append(f"{label}: quality_target debe ser 'reference_grade'")

    checks = contract.get("quality_checks")
    required_checks = {
        "single_family",
        "single_dominant_idea",
        "mobile_legibility",
        "reference_consistency",
    }
    if not isinstance(checks, dict):
        errors.append(f"{label}: falta quality_checks")
    else:
        missing = sorted(key for key in required_checks if checks.get(key) is not True)
        if missing:
            errors.append(
                f"{label}: quality_checks incompletos: {', '.join(missing)}"
            )

    allowed_executions = set(family.get("allowed_executions", []))
    if execution not in allowed_executions:
        errors.append(
            f"{label}: execution={execution} no está admitido para {family_id}"
        )

    refs = contract.get("references", [])
    reference_root = family.get("reference_root")
    if not isinstance(refs, list) or not refs:
        errors.append(f"{label}: references debe incluir una referencia de familia")
    elif reference_root:
        wrong = [ref for ref in refs if not isinstance(ref, str) or not ref.startswith(reference_root)]
        if wrong:
            errors.append(
                f"{label}: todas las referencias deben vivir bajo {reference_root}"
            )


def validate_contract(
    contract: dict[str, Any],
    contract_path: Path,
    visual: dict[str, Any],
    label: str,
    require_approved: bool,
    expected_schema: int,
    families: dict[str, Any],
    errors: list[str],
) -> None:
    schema_version = contract.get("schema_version")
    if schema_version != expected_schema:
        errors.append(
            f"{label}: schema_version debe ser {expected_schema} para este manifiesto"
        )

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
        if not contract.get("approved_preview"):
            errors.append(f"{label}: un contrato aprobado exige approved_preview")

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

    if isinstance(execution, str):
        _validate_generation(contract, execution, label, errors)

    refs = contract.get("references", [])
    if refs is not None and not isinstance(refs, list):
        errors.append(f"{label}: references debe ser una lista")

    if expected_schema == 2 and isinstance(execution, str):
        _validate_v2(contract, execution, label, families, errors)

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
    if version not in {1, 2}:
        print(f"ERROR: contrato_visual_version no soportado: {version!r}")
        return 1

    errors: list[str] = []
    families = _load_families(errors) if version == 2 else {}
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
                    version,
                    families,
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
