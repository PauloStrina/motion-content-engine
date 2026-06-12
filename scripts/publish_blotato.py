#!/usr/bin/env python3
"""Publicación/programación vía Blotato. SOLO publica desde queue/approved/.
TODO al hacer setup: completar BASE_URL y formato de payload según la documentación oficial de Blotato API
(verificar endpoint de creación de posts y mapeo de cuentas conectadas). API key: variable de entorno BLOTATO_API_KEY."""
import os, sys, json, pathlib, urllib.request

BASE_URL = "TODO_SEGUN_DOCS_BLOTATO"   # p.ej. https://backend.blotato.com/v2/posts — VERIFICAR
API_KEY = os.environ["BLOTATO_API_KEY"]

def schedule(text, channel, when, media=None):
    payload = {"channel": channel, "text": text, "scheduledTime": when, "media": media or []}  # TODO: ajustar a schema real
    req = urllib.request.Request(BASE_URL, data=json.dumps(payload).encode(),
        headers={"blotato-api-key": API_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

if __name__ == "__main__":
    # El Agente Publicador invoca: publish_blotato.py <pieza.json>  (pieza ya mapeada a canal+horario por config.yaml)
    piece = json.load(open(sys.argv[1]))
    print(schedule(piece["text"], piece["channel"], piece["when"], piece.get("media")))
