#!/usr/bin/env python3
"""Programa una semana o mes aprobado en LinkedIn e Instagram."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

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


def publicar(manifest: dict, cfg: dict, reels_dir: str, dry: bool, semana: int | None) -> tuple[list[str], list[dict]]:
    failures: list[str] = []
    plan: list[dict] = []
    client = B.BlotatoClient(dry=dry)
    media_base = os.environ.get("MEDIA_BASE", "https://ops-motionco.github.io/motion-media/carruseles")
    catalog = MES.leer_catalogo()

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
                text = day["texto_linkedin"] if channel == "linkedin_paulo" else day["caption_instagram"]
                name = f"mes{manifest['mes']}_{start}_{day_key}_{channel}"
                media: list[str] = []
                if fmt == "video":
                    media = [video_url]
                elif channel == "linkedin_paulo" and day.get("imagen_linkedin"):
                    media = [f"{media_base}/{day['imagen_linkedin']}-1.png"]
                elif not (fmt == "post_carousel" and channel == "linkedin_paulo"):
                    base = day["carrusel"]
                    media = [f"{media_base}/{base}-{i}.png" for i in range(1, day["carrusel_slides"] + 1)]

                item = {
                    "week": week.get("numero"), "day": day_key, "channel": channel,
                    "type": day["tipo"], "format": fmt, "scheduledTime": when,
                    "account": account, "platform": platform, "name": name,
                    "text": text, "media": media,
                }
                plan.append(item)
                print(f"\n▶ {start}/{day_key} [{day['tipo']}/{fmt}] {channel} → {when}")
                print(f"  media: {len(media)}")
                try:
                    client.schedule(account, platform, text, when, media=media, page_id=cfg[channel].get("pageid"), name=name)
                    print("  ✓ programado" if not dry else "  ✓ dry validado")
                except Exception as exc:
                    print(f"  ✗ {exc}")
                    failures.append(f"{start}/{day_key}/{channel}")
    return failures, plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", required=True)
    parser.add_argument("--semana", type=int, choices=(1,2,3,4))
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
    failures, plan = publicar(manifest, cfg, os.environ.get("REELS_DIR", "media_repo/reels"), args.dry, args.semana)
    if args.plan_output:
        Path(args.plan_output).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        print(f"\n⚠ {len(failures)} error(es): {failures}")
        return 1
    print(f"\n✓ {'Semana '+str(args.semana) if args.semana else 'Mes completo'} procesada sin errores")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
