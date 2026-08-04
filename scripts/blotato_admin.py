#!/usr/bin/env python3
"""Utilidades de mantenimiento sobre posts programados en Blotato.

    python scripts/blotato_admin.py listar
    python scripts/blotato_admin.py borrar --prefijo semana2026-08-04
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://backend.blotato.com/v2"


def _key() -> str:
    key = os.environ.get("BLOTATO_API_KEY")
    if not key:
        raise RuntimeError("Falta BLOTATO_API_KEY")
    return key


def _call(path: str, method: str = "GET") -> object:
    headers = {"blotato-api-key": _key()}
    if method not in ("GET", "DELETE"):
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(API + path, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode()
        return json.loads(body) if body.strip() else {"status": response.status}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:600]
        return {"_http_error": exc.code, "_detail": detail, "_path": path}


def _posts(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "posts", "data", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("accion", choices=("listar", "borrar"))
    parser.add_argument("--prefijo", default="")
    parser.add_argument("--ids", default="")
    parser.add_argument("--endpoint", default="/posts")
    args = parser.parse_args()

    payload = _call(args.endpoint)
    if isinstance(payload, dict) and payload.get("_http_error"):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    posts = _posts(payload)
    print(f"{len(posts)} post(s) devueltos por {args.endpoint}")
    for post in posts:
        pid = post.get("id") or post.get("postId") or post.get("_id")
        name = post.get("name", "")
        when = post.get("scheduledTime") or post.get("scheduled_time") or ""
        print(f"  {pid}  {when}  {name}")

    if args.accion == "listar":
        print("--- crudo ---")
        for post in posts:
            print(json.dumps(post, ensure_ascii=False)[:700])
        if not posts:
            print(json.dumps(payload, ensure_ascii=False)[:1500])
        return 0

    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    if not ids and not args.prefijo:
        print("borrar exige --ids o --prefijo")
        return 1

    fallos = 0
    for post in posts:
        pid = str(post.get("id") or post.get("postId") or post.get("_id"))
        name = post.get("name", "")
        if ids:
            if pid not in ids:
                continue
        elif not name.startswith(args.prefijo):
            continue
        result = _call(f"/posts/{pid}", method="DELETE")
        if isinstance(result, dict) and result.get("_http_error"):
            print(f"  ✗ {pid} {name}: HTTP {result['_http_error']} {result['_detail'][:200]}")
            fallos += 1
        else:
            print(f"  ✓ borrado {pid} {name}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
