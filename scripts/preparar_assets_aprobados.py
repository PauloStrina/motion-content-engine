#!/usr/bin/env python3
"""Descarga, valida y prepara masters visuales aprobados e inmutables."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from PIL import Image


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} debe contener un objeto JSON")
    return value


def download_drive(file_id: str, output: Path) -> None:
    try:
        import gdown
    except ImportError as exc:
        raise RuntimeError("Falta gdown; instalá la dependencia antes de preparar assets") from exc

    result = gdown.download(id=file_id, output=str(output), quiet=False, fuzzy=False)
    if not result or not output.exists():
        raise RuntimeError(f"No se pudo descargar el paquete público de Drive: {file_id}")


def safe_extract(archive: Path, destination: Path) -> None:
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            try:
                target.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"Ruta insegura dentro del ZIP: {member.filename}") from exc
        bundle.extractall(destination)


def validate_internal_manifest(root: Path) -> dict[str, dict[str, Any]]:
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        raise ValueError("El paquete aprobado no contiene manifest.json")
    manifest = read_json(manifest_path)
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("manifest.json no contiene una lista de assets")

    indexed: dict[str, dict[str, Any]] = {}
    for item in assets:
        if not isinstance(item, dict) or not isinstance(item.get("file"), str):
            raise ValueError("Asset inválido en manifest.json")
        relative = item["file"]
        path = (root / relative).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError as exc:
            raise ValueError(f"Asset fuera del paquete: {relative}") from exc
        if not path.is_file():
            raise ValueError(f"Falta asset declarado: {relative}")
        if path.suffix.lower() != ".png":
            raise ValueError(f"El asset publicable debe ser PNG: {relative}")
        actual_sha = sha256(path)
        if actual_sha != item.get("sha256"):
            raise ValueError(f"SHA-256 inválido para {relative}")
        if path.stat().st_size != item.get("bytes"):
            raise ValueError(f"Tamaño inválido para {relative}")
        with Image.open(path) as image:
            dimensions = list(image.size)
        if dimensions != item.get("dimensions"):
            raise ValueError(f"Dimensiones inválidas para {relative}: {dimensions}")
        indexed[relative] = item
    return indexed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    config_path = Path(args.config)
    config = read_json(config_path)
    if config.get("status") != "approved":
        raise ValueError("El paquete no está aprobado")
    if not config.get("approved_by") or not config.get("approved_at"):
        raise ValueError("El paquete aprobado no tiene autor y fecha")

    source = config.get("source")
    mappings = config.get("mappings")
    expected_count = config.get("expected_png_count")
    if not isinstance(source, dict) or not source.get("file_id"):
        raise ValueError("Falta source.file_id")
    if not isinstance(mappings, list) or len(mappings) != expected_count:
        raise ValueError("La cantidad de mappings no coincide con expected_png_count")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old_png in out_dir.glob("*.png"):
        old_png.unlink()

    with tempfile.TemporaryDirectory(prefix="motion-approved-") as tmp_raw:
        tmp = Path(tmp_raw)
        zip_path = tmp / "package.zip"
        extracted = tmp / "extracted"
        extracted.mkdir()

        download_drive(str(source["file_id"]), zip_path)
        if zip_path.stat().st_size != source.get("zip_bytes"):
            raise ValueError("El tamaño del ZIP descargado no coincide con el aprobado")
        actual_zip_sha = sha256(zip_path)
        if actual_zip_sha != source.get("zip_sha256"):
            raise ValueError("El SHA-256 del ZIP descargado no coincide con el aprobado")

        safe_extract(zip_path, extracted)
        indexed = validate_internal_manifest(extracted)
        if len(indexed) != expected_count:
            raise ValueError(
                f"El manifiesto interno contiene {len(indexed)} assets; se esperaban {expected_count}"
            )

        outputs: list[dict[str, Any]] = []
        seen_targets: set[str] = set()
        for mapping in mappings:
            if not isinstance(mapping, dict):
                raise ValueError("Mapping inválido")
            source_name = mapping.get("source")
            target_name = mapping.get("target")
            if source_name not in indexed:
                raise ValueError(f"El mapping referencia un source no aprobado: {source_name}")
            if not isinstance(target_name, str) or not target_name.endswith(".png"):
                raise ValueError(f"Target inválido: {target_name!r}")
            if Path(target_name).name != target_name or target_name in seen_targets:
                raise ValueError(f"Target inseguro o duplicado: {target_name}")
            seen_targets.add(target_name)

            source_path = extracted / source_name
            target_path = out_dir / target_name
            shutil.copyfile(source_path, target_path)
            source_sha = indexed[source_name]["sha256"]
            if sha256(target_path) != source_sha:
                raise ValueError(f"La copia alteró el master: {target_name}")
            outputs.append(
                {
                    "source": source_name,
                    "target": target_name,
                    "sha256": source_sha,
                    "bytes": target_path.stat().st_size,
                    "dimensions": indexed[source_name]["dimensions"],
                }
            )

    generated = sorted(out_dir.glob("*.png"))
    if len(generated) != expected_count:
        raise ValueError(f"Se prepararon {len(generated)} PNG; se esperaban {expected_count}")

    report = {
        "package_id": config.get("package_id"),
        "status": "validated_and_reused",
        "approved_by": config.get("approved_by"),
        "approved_at": config.get("approved_at"),
        "zip_sha256": source.get("zip_sha256"),
        "asset_count": len(outputs),
        "assets": outputs,
    }
    report_path = out_dir / "approved-package-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {len(outputs)} masters aprobados validados y copiados sin rediseño")
    print(f"✓ Reporte: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
