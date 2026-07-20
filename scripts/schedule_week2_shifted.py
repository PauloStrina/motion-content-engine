#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blotato_client as B
import mes as MES

SCHEDULE = Path("content/2026-07-week2/schedule.json")
RESULTS = Path("content/2026-07-week2/scheduled.json")


def utc_iso(value: str) -> str:
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"scheduled_at sin zona horaria: {value}")
    return parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry", action="store_true")
    args = parser.parse_args()

    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    config = B.load_config()
    catalog = MES.leer_catalogo()
    reels = {item["id"]: item for item in catalog.get("reels", [])}
    media_base = schedule["media_base"].rstrip("/")
    client = B.BlotatoClient(dry=args.dry)
    now = dt.datetime.now(dt.timezone.utc)
    results = []

    for post in schedule["posts"]:
        channel = post["channel"]
        if channel not in config:
            raise RuntimeError(f"Falta configuración para {channel}")
        when = utc_iso(post["scheduled_at"])
        if not args.dry and dt.datetime.fromisoformat(when.replace("Z", "+00:00")) <= now:
            raise RuntimeError(f"La fecha ya pasó para {post['id']}: {when}")

        media_urls: list[str] = []
        if post.get("media"):
            media_urls = [f"{media_base}/{name}" for name in post["media"]]
        elif post.get("reel_id"):
            reel = reels.get(post["reel_id"])
            if not reel:
                raise RuntimeError(f"Reel inexistente: {post['reel_id']}")
            media_urls = [reel["url"]]

        cfg = config[channel]
        print(f"▶ {post['id']} → {channel} → {when}")
        result = client.schedule(
            cfg["account"],
            cfg["platform"],
            post["text"],
            when,
            media=media_urls,
            page_id=cfg.get("pageid"),
            name=post["id"],
        )
        results.append({
            "id": post["id"],
            "channel": channel,
            "scheduled_at": when,
            "media": media_urls,
            "blotato": result,
        })

    if not args.dry:
        RESULTS.write_text(json.dumps({"scheduled_at": now.isoformat(), "posts": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {len(results)} publicaciones {'simuladas' if args.dry else 'programadas'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
