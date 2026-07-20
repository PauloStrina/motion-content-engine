#!/usr/bin/env python3
"""Genera, edita o reutiliza un recurso conceptual aprobado."""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any

REPO_ROOT = Path('.').resolve()
CONCEPT_ROOT = (REPO_ROOT / 'design-system/concepts').resolve()
GENERATED_ROOT = (REPO_ROOT / 'design-system/generated').resolve()
ALLOWED_STATUS = {'approved', 'generated', 'final'}
ALLOWED_EXECUTION = {'openai', 'hybrid', 'reuse'}


def inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def load_contract(path: Path) -> dict[str, Any]:
    if not inside(path, CONCEPT_ROOT):
        raise ValueError('El contrato debe vivir bajo design-system/concepts/')
    contract = json.loads(path.read_text(encoding='utf-8'))
    if contract.get('schema_version') not in {1, 2}:
        raise ValueError('schema_version debe ser 1 o 2')
    if contract.get('status') not in ALLOWED_STATUS:
        raise ValueError('El contrato debe estar aprobado antes de generar')
    if contract.get('execution') not in ALLOWED_EXECUTION:
        raise ValueError('Este script solo procesa openai, hybrid o reuse')
    return contract


def resolve_repo_path(raw: str, allowed_root: Path | None = None) -> Path:
    path = (REPO_ROOT / raw).resolve()
    if not inside(path, REPO_ROOT):
        raise ValueError(f'Ruta fuera del repositorio: {raw}')
    if allowed_root and not inside(path, allowed_root):
        raise ValueError(f'Ruta fuera de {allowed_root}: {raw}')
    return path


def decode_result(result: Any) -> bytes:
    data = getattr(result, 'data', None)
    if not data:
        raise RuntimeError('OpenAI no devolvió datos de imagen')
    encoded = getattr(data[0], 'b64_json', None)
    if not encoded:
        raise RuntimeError('OpenAI no devolvió b64_json')
    return base64.b64decode(encoded)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--concept', required=True)
    parser.add_argument('--out')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    concept_path = resolve_repo_path(args.concept, CONCEPT_ROOT)
    contract = load_contract(concept_path)
    execution = contract['execution']
    generation = contract.get('generation') or {}

    raw_output = args.out or generation.get('output')
    if not raw_output:
        raise ValueError('Falta output en el contrato o --out')
    output = resolve_repo_path(raw_output, GENERATED_ROOT)
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists() and not args.force:
        print(f'✓ Recurso existente: {output}')
        return 0

    approved_preview = contract.get('approved_preview')
    if execution == 'reuse':
        if not approved_preview:
            raise ValueError('execution=reuse exige approved_preview')
        source = resolve_repo_path(approved_preview)
        if source != output:
            shutil.copy2(source, output)
        mode = 'reuse'
        model = None
        prompt = None
    else:
        if not os.environ.get('OPENAI_API_KEY'):
            raise RuntimeError('Falta OPENAI_API_KEY')
        prompt = generation.get('prompt')
        if not prompt:
            raise ValueError('Falta generation.prompt')

        from openai import OpenAI
        client = OpenAI()
        model = generation.get('model', 'gpt-image-2-2026-04-21')
        params = {
            'model': model,
            'prompt': prompt,
            'size': generation.get('size', '1024x1536'),
            'quality': generation.get('quality', 'high'),
            'background': generation.get('background', 'opaque'),
            'output_format': generation.get('output_format', 'png'),
        }
        reference = generation.get('reference_image')
        if reference:
            reference_path = resolve_repo_path(reference)
            with reference_path.open('rb') as image_file:
                edit_params = dict(params)
                edit_params['image'] = image_file
                if generation.get('input_fidelity'):
                    edit_params['input_fidelity'] = generation['input_fidelity']
                result = client.images.edit(**edit_params)
            mode = 'edit'
        else:
            result = client.images.generate(**params)
            mode = 'generate'
        output.write_bytes(decode_result(result))

    metadata = {
        'piece_id': contract.get('piece_id'),
        'concept_path': str(concept_path.relative_to(REPO_ROOT)),
        'output': str(output.relative_to(REPO_ROOT)),
        'execution': execution,
        'mode': mode,
        'model': model,
        'prompt_sha256': hashlib.sha256((prompt or '').encode('utf-8')).hexdigest() if prompt else None,
        'reference_image': generation.get('reference_image') if generation else None,
        'approved_preview': approved_preview,
        'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    metadata_path = output.with_suffix(output.suffix + '.json')
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'✓ Recurso conceptual: {output}')
    print(f'✓ Metadatos: {metadata_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
