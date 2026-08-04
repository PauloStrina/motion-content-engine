#!/usr/bin/env python3
"""Programa en Blotato la semana del 2026-08-04.

Pieza puntual: el calendario de esta semana se corrio un dia respecto del
documento editorial, y el jueves usa el copy madre en lugar de un caption
propio, asi que no encaja en el contrato de `mes.py`. Se publica desde aca
en vez de desde `publicador_mes.py`.

Uso:
    python scripts/publicar_semana_2026_08_04.py --dry
    python scripts/publicar_semana_2026_08_04.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import blotato_client as B

COPYS = Path("manifiestos/_copys_2026-08-04.json")
MEDIA_BASE = os.environ.get(
    "MEDIA_BASE", "https://ops-motionco.github.io/motion-media/carruseles"
)
TZ = ZoneInfo(os.environ.get("MOTION_TIMEZONE", "America/Argentina/Buenos_Aires"))
CANALES = ["linkedin_paulo", "instagram"]


def cuando(fecha: str, hhmm: str) -> str:
    hour, minute = map(int, hhmm.split(":"))
    day = dt.date.fromisoformat(fecha)
    local = dt.datetime(day.year, day.month, day.day, hour, minute, tzinfo=TZ)
    return local.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


MAX_CARRUSEL = 10


def medias(day: dict, canal: str) -> list[str]:
    if canal == "linkedin_paulo" and day.get("linkedin_media"):
        return [f"{MEDIA_BASE}/{name}" for name in day["linkedin_media"]]
    base = day["carrusel"]
    count = day["carrusel_slides"]
    if canal == "instagram" and day.get("instagram_slides"):
        count = day["instagram_slides"]
    return [f"{MEDIA_BASE}/{base}-{index}.png" for index in range(1, count + 1)]


def pdf_documento(client: B.BlotatoClient, day: dict, urls: list[str]) -> str:
    """Arma un PDF con las placas y lo sube al CDN de Blotato.

    LinkedIn acepta hasta 10 imagenes en un carrusel, pero admite documentos
    PDF de mas paginas. Los carruseles largos van por esta via.
    """
    import io
    import urllib.request as _req

    from PIL import Image

    paginas = []
    for url in urls:
        with _req.urlopen(url) as response:
            paginas.append(Image.open(io.BytesIO(response.read())).convert("RGB"))

    destino = Path(f"/tmp/{day['carrusel']}.pdf")
    paginas[0].save(destino, save_all=True, append_images=paginas[1:], format="PDF")
    print(f"  PDF armado: {destino} ({len(paginas)} paginas)")
    return client.upload_presigned(str(destino))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--dia", choices=("mar", "mie", "jue"))
    parser.add_argument("--canal", choices=("linkedin_paulo", "instagram"))
    args = parser.parse_args()

    spec = json.loads(COPYS.read_text(encoding="utf-8"))
    config = B.load_config()
    client = B.BlotatoClient(dry=args.dry)

    ahora = dt.datetime.now(dt.timezone.utc)
    fallos: list[str] = []
    dias = [args.dia] if args.dia else ["mar", "mie", "jue"]

    print(f"Publicador semana 2026-08-04 — {'DRY' if args.dry else 'LIVE'}")

    for key in dias:
        day = spec["dias"][key]
        for canal in ([args.canal] if args.canal else CANALES):
            if canal not in config:
                fallos.append(f"{key}/{canal}: falta configuracion")
                continue
            hora = day["hora_linkedin"] if canal == "linkedin_paulo" else day["hora_instagram"]
            when = cuando(day["fecha"], hora)
            if dt.datetime.fromisoformat(when.replace("Z", "+00:00")) <= ahora:
                fallos.append(f"{key}/{canal}: horario {when} ya paso")
                continue
            text = day["texto_linkedin"] if canal == "linkedin_paulo" else day["caption_instagram"]
            urls = medias(day, canal)
            if canal == "linkedin_paulo" and len(urls) > MAX_CARRUSEL:
                if args.dry:
                    print(f"  [DRY] {len(urls)} placas → PDF para LinkedIn")
                    urls = [f"dry://{day['carrusel']}.pdf"]
                else:
                    urls = [pdf_documento(client, day, urls)]
            name = f"semana2026-08-04_{day['fecha']}_{key}_{canal}"
            print(f"\n▶ {day['fecha']} {key} [{day['tema']}] {canal} → {when} ({len(urls)} img)")
            try:
                client.schedule(
                    config[canal]["account"],
                    config[canal]["platform"],
                    text,
                    when,
                    media=urls,
                    page_id=config[canal].get("pageid"),
                    name=name,
                )
                print("  ✓ programado")
            except Exception as exc:
                print(f"  ✗ {exc}")
                fallos.append(f"{key}/{canal}: {exc}")

    if fallos:
        print(f"\n⚠ {len(fallos)} error(es):")
        for fallo in fallos:
            print(f" - {fallo}")
        return 1
    print("\n✓ semana programada sin errores")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
