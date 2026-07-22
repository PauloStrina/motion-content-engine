#!/usr/bin/env python3
"""Programa una semana o mes aprobado en LinkedIn e Instagram."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blotato_client as B
import mes as MES

HORA = {"linkedin_paulo": "09:00", "instagram": "12:00"}


def media_video(client: B.BlotatoClient, reel: dict, reels_dir: str) -> str:
    local = os.path.join(reels_dir, reel["archivo"]) if reels_dir else ""
    if local and os.path.exists(local):
        if client.dry:
            print(f"  [DRY] upload de {local}")
            return reel["url"]
        return client.upload_presigned(local)
    print(f"  ⚠ {reel['archivo']} no está local; uso URL aprobada del banco")
    return reel["url"]


def response_id(result: dict[str, Any]) -> str | None:
    preferred = {
        "id",
        "postid",
        "post_id",
        "postsubmissionid",
        "submissionid",
        "submission_id",
    }

    def walk(value: Any) -> str | None:
        if isinstance(value, dict):
            for key, nested in value.items():
                if key.lower() in preferred and nested not in (None, ""):
                    return str(nested)
            for nested in value.values():
                found = walk(nested)
                if found:
                    return found
        elif isinstance(value, list):
            for nested in value:
                found = walk(nested)
                if found:
                    return found
        return None

    return walk(result)


def write_plan(path: str | None, plan: list[dict[str, Any]]) -> None:
    if not path:
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def prepare_image_media(
    client: B.BlotatoClient,
    media_dir: str,
) -> dict[str, str]:
    """Sube todos los PNG antes de crear el primer post y devuelve filename→URL."""
    if not media_dir:
        return {}
    root = Path(media_dir)
    if not root.is_dir():
        raise RuntimeError(f"MEDIA_DIR no existe: {root}")

    pngs = sorted(root.glob("*.png"))
    if not pngs:
        raise RuntimeError(f"MEDIA_DIR no contiene PNG: {root}")

    uploaded: dict[str, str] = {}
    print(f"\n▶ Preparando {len(pngs)} masters visuales en Blotato")
    for path in pngs:
        if client.dry:
            uploaded[path.name] = f"dry://{path.name}"
        else:
            uploaded[path.name] = client.upload_presigned(str(path))
    print(f"✓ {len(uploaded)} masters disponibles para programación")
    return uploaded


def image_urls(
    filenames: list[str],
    uploaded: dict[str, str],
    media_base: str,
) -> list[str]:
    urls: list[str] = []
    for filename in filenames:
        if uploaded:
            if filename not in uploaded:
                raise RuntimeError(f"Falta master local aprobado: {filename}")
            urls.append(uploaded[filename])
        else:
            urls.append(f"{media_base}/{filename}")
    return urls


def publicar(
    manifest: dict,
    cfg: dict,
    reels_dir: str,
    media_dir: str,
    dry: bool,
    semana: int | None,
    plan_output: str | None = None,
) -> tuple[list[str], list[dict[str, Any]]]:
    failures: list[str] = []
    plan: list[dict[str, Any]] = []
    client = B.BlotatoClient(dry=dry)
    media_base = os.environ.get(
        "MEDIA_BASE", "https://ops-motionco.github.io/motion-media/carruseles"
    )
    catalog = MES.leer_catalogo()

    # Carga atómica de medios: ningún post se crea hasta que los 21 masters
    # aprobados hayan sido cargados correctamente.
    uploaded_images = prepare_image_media(client, media_dir)

    for week in MES.seleccionar_semanas(manifest, semana):
        start = week["fecha_inicio"]
        for day_key in MES.DIAS:
            day = week["dias"][day_key]
            fmt = day["formato"]
            video_url = None
            if fmt == "video":
                reel = MES.reel_por_id(catalog, day["reel_id"])
                if not reel:
                    failures.append(f"{start}/{day_key}: reel inexistente")
                    continue
                video_url = media_video(client, reel, reels_dir)

            for channel in ("linkedin_paulo", "instagram"):
                if channel not in cfg:
                    failures.append(f"{start}/{day_key}/{channel}: falta configuración")
                    continue
                account = cfg[channel]["account"]
                platform = cfg[channel]["platform"]
                when = MES.fecha_dia(start, day_key, HORA[channel])
                text = (
                    day["texto_linkedin"]
                    if channel == "linkedin_paulo"
                    else day["caption_instagram"]
                )
                name = f"mes{manifest['mes']}_{start}_{day_key}_{channel}"
                media: list[str] = []

                if fmt == "video":
                    media = [video_url]
                elif channel == "linkedin_paulo" and day.get("imagen_linkedin"):
                    filename = f"{day['imagen_linkedin']}-1.png"
                    media = image_urls([filename], uploaded_images, media_base)
                elif not (fmt == "post_carousel" and channel == "linkedin_paulo"):
                    base = day["carrusel"]
                    filenames = [
                        f"{base}-{i}.png"
                        for i in range(1, day["carrusel_slides"] + 1)
                    ]
                    media = image_urls(filenames, uploaded_images, media_base)

                item: dict[str, Any] = {
                    "week": week.get("numero"),
                    "day": day_key,
                    "channel": channel,
                    "type": day["tipo"],
                    "format": fmt,
                    "scheduledTime": when,
                    "account": account,
                    "platform": platform,
                    "name": name,
                    "text": text,
                    "media": media,
                    "status": "pending",
                }
                plan.append(item)
                write_plan(plan_output, plan)

                print(f"\n▶ {start}/{day_key} [{day['tipo']}/{fmt}] {channel} → {when}")
                print(f"  media: {len(media)}")
                try:
                    result = client.schedule(
                        account,
                        platform,
                        text,
                        when,
                        media=media,
                        page_id=cfg[channel].get("pageid"),
                        name=name,
                    )
                    item["status"] = "dry_validated" if dry else "scheduled"
                    item["blotato_id"] = response_id(result)
                    item["blotato_response"] = result
                    write_plan(plan_output, plan)
                    if dry:
                        print("  ✓ dry validado")
                    else:
                        print(
                            "  ✓ programado · Blotato ID: "
                            f"{item['blotato_id'] or 'no informado'}"
                        )
                except Exception as exc:
                    item["status"] = "failed"
                    item["error"] = str(exc)
                    write_plan(plan_output, plan)
                    print(f"  ✗ {exc}")
                    failures.append(f"{start}/{day_key}/{channel}")
    return failures, plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", required=True)
    parser.add_argument("--semana", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--plan-output")
    args = parser.parse_args()

    try:
        manifest = MES.leer(args.mes)
    except (FileNotFoundError, ValueError):
        print(f"No existe manifiesto mensual para {args.mes}")
        return 1
    errors = MES.validar(manifest, exigir_aprobado=not args.dry, semana=args.semana)
    if errors:
        print("Manifiesto mensual inválido:")
        for error in errors:
            print(f" - {error}")
        return 1

    cfg = B.load_config()
    failures, plan = publicar(
        manifest,
        cfg,
        os.environ.get("REELS_DIR", ""),
        os.environ.get("MEDIA_DIR", ""),
        args.dry,
        args.semana,
        args.plan_output,
    )
    write_plan(args.plan_output, plan)
    if failures:
        print(f"\n⚠ {len(failures)} error(es): {failures}")
        return 1
    print(
        f"\n✓ {'Semana '+str(args.semana) if args.semana else 'Mes completo'} "
        "procesada sin errores"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
