#!/usr/bin/env python3
"""Programa un manifiesto mensual aprobado en LinkedIn e Instagram."""
from __future__ import annotations

import argparse
import os
import sys

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
    print(f"  ⚠ {reel['archivo']} no está local; uso URL de Pages")
    return reel["url"]


def publicar_mes(manifest: dict, cfg: dict, reels_dir: str, dry: bool) -> list[str]:
    failures: list[str] = []
    client = B.BlotatoClient(dry=dry)
    media_base = os.environ.get(
        "MEDIA_BASE", "https://ops-motionco.github.io/motion-media/carruseles"
    )
    catalog = MES.leer_catalogo()

    for week in manifest["semanas"]:
        start = week["fecha_inicio"]
        for day_key in MES.DIAS:
            day = week["dias"][day_key]
            fmt = day["formato"]
            if fmt == "faltante_video":
                print(f"\n⚠ {start}/{day_key}: video faltante; se usa fallback")
                fmt = "post_carousel"

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
                text = day["texto_linkedin"] if channel == "linkedin_paulo" else day["caption_instagram"]
                name = f"mes{manifest['mes']}_{start}_{day_key}_{channel}"
                print(f"\n▶ {start}/{day_key} [{day['tipo']}/{fmt}] {channel} → {when}")
                try:
                    if fmt == "video":
                        client.schedule(
                            account,
                            platform,
                            text,
                            when,
                            media=[video_url],
                            page_id=cfg[channel].get("pageid"),
                            name=name,
                        )
                    elif fmt == "post_carousel" and channel == "linkedin_paulo":
                        client.schedule(
                            account,
                            platform,
                            text,
                            when,
                            page_id=cfg[channel].get("pageid"),
                            name=name,
                        )
                    else:
                        base = day["carrusel"]
                        count = day["carrusel_slides"]
                        urls = [f"{media_base}/{base}-{index}.png" for index in range(1, count + 1)]
                        client.schedule(
                            account,
                            platform,
                            text,
                            when,
                            media=urls,
                            page_id=cfg[channel].get("pageid"),
                            name=name,
                        )
                    print("  ✓ programado")
                except Exception as exc:
                    print(f"  ✗ {exc}")
                    failures.append(f"{start}/{day_key}/{channel}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", required=True)
    parser.add_argument("--dry", action="store_true")
    args = parser.parse_args()

    try:
        manifest = MES.leer(args.mes)
    except (FileNotFoundError, ValueError):
        print(f"No existe manifiesto mensual para {args.mes}")
        return 1

    errors = MES.validar(manifest, exigir_aprobado=not args.dry)
    if errors:
        print("Manifiesto mensual inválido:")
        for error in errors:
            print(f" - {error}")
        return 1

    config = B.load_config()
    reels_dir = os.environ.get("REELS_DIR", "media_repo/reels")
    print(f"Publicador mensual — {'DRY' if args.dry else 'LIVE'} — {args.mes}")
    failures = publicar_mes(manifest, config, reels_dir, args.dry)
    if failures:
        print(f"\n⚠ {len(failures)} error(es): {failures}")
        return 1
    print("\n✓ Mes completo procesado sin errores")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
