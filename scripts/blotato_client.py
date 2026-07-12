#!/usr/bin/env python3
"""Cliente mínimo de Blotato compartido por el publicador mensual."""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API = "https://backend.blotato.com/v2"
BLOTATO_DELAY_SECONDS = 5
BLOTATO_MAX_INTENTOS = 3


class BlotatoClient:
    def __init__(self, dry: bool = False) -> None:
        self.dry = dry

    @staticmethod
    def _key() -> str:
        key = os.environ.get("BLOTATO_API_KEY")
        if not key:
            raise RuntimeError("Falta BLOTATO_API_KEY")
        return key

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if self.dry:
            print(f"  [DRY] POST {path}: {json.dumps(body, ensure_ascii=False)[:200]}")
            return {"id": "dry"}

        for attempt in range(1, BLOTATO_MAX_INTENTOS + 1):
            request = urllib.request.Request(
                API + path,
                data=json.dumps(body).encode(),
                headers={"blotato-api-key": self._key(), "Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(request) as response:
                    result = json.load(response)
                time.sleep(BLOTATO_DELAY_SECONDS)
                return result
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode(errors="replace")[:500]
                retryable = exc.code in {429, 500, 502, 503, 504}
                if retryable and attempt < BLOTATO_MAX_INTENTOS:
                    wait = BLOTATO_DELAY_SECONDS * attempt
                    print(f"  ⚠ Blotato HTTP {exc.code}; reintento en {wait}s")
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"Blotato HTTP {exc.code}: {detail}") from exc
            except Exception as exc:
                if attempt < BLOTATO_MAX_INTENTOS:
                    wait = BLOTATO_DELAY_SECONDS * attempt
                    print(f"  ⚠ Error temporal; reintento en {wait}s")
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"Error llamando a Blotato: {exc}") from exc
        raise RuntimeError("Blotato agotó los reintentos")

    @staticmethod
    def _validate(response: dict[str, Any]) -> None:
        if not response:
            raise RuntimeError("Respuesta vacía de Blotato")
        text = json.dumps(response, ensure_ascii=False).lower()
        for marker in ("error", "failed", "invalid", "unauthorized", "forbidden", "rate limit"):
            if marker in text:
                raise RuntimeError(f"Respuesta inválida de Blotato: {response}")

    def upload_presigned(self, local_path: str) -> str:
        filename = os.path.basename(local_path)
        upload = self._post("/media/uploads", {"filename": filename})
        if self.dry:
            return f"dry://{filename}"
        presigned_url = upload["presignedUrl"]
        public_url = upload["publicUrl"]
        extension = filename.rsplit(".", 1)[-1].lower()
        content_type = {
            "pdf": "application/pdf",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "mp4": "video/mp4",
        }.get(extension, "application/octet-stream")
        with open(local_path, "rb") as fh:
            data = fh.read()
        request = urllib.request.Request(
            presigned_url,
            data=data,
            method="PUT",
            headers={"Content-Type": content_type},
        )
        urllib.request.urlopen(request)
        print(f"  ✓ uploaded to Blotato CDN: {public_url}")
        return public_url

    def schedule(
        self,
        account: str,
        platform: str,
        text: str,
        when: str,
        media: list[str] | None = None,
        page_id: str | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        target: dict[str, Any] = {"targetType": platform}
        if page_id:
            target["pageId"] = str(page_id)
        post: dict[str, Any] = {
            "accountId": str(account),
            "content": {"text": text, "mediaUrls": media or [], "platform": platform},
            "target": target,
        }
        if name:
            post["name"] = name
        result = self._post("/posts", {"post": post, "scheduledTime": when})
        self._validate(result)
        return result


def load_config(path: str = "config.yaml") -> dict[str, dict[str, str | None]]:
    channels: dict[str, dict[str, str | None]] = {}
    config_path = Path(path)
    if not config_path.exists():
        return channels
    pattern = re.compile(
        r"\s*(\w+):\s*\{account:\s*(\w+),\s*platform:\s*(\w+)(?:.*?pageid:\s*(\w+))?"
    )
    for line in config_path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            channels[match.group(1)] = {
                "account": match.group(2),
                "platform": match.group(3),
                "pageid": match.group(4),
            }
    return channels
