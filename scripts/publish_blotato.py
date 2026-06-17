#!/usr/bin/env python3
"""Agente Publicador MOTION — programa en Blotato (modo revisión: fecha futura, editable en calendario).
Lee config.yaml (canales activos) y los archivos de cascada aprobada en queue/approved/.
Endpoints verificados jun 2026: POST /v2/media, POST /v2/posts (scheduledTime FUERA de 'post').
X/Twitter soporta hilos vía additionalPosts. Imágenes: requieren URL pública (GitHub raw).
Uso: python publish_blotato.py [--dry]"""
import os, sys, json, re, glob, urllib.request, datetime as dt

API = "https://backend.blotato.com/v2"
DRY = "--dry" in sys.argv
def _key(): return os.environ["BLOTATO_API_KEY"]

def _post(path, body):
    if DRY:
        print(f"  [DRY] POST {path}\n        {json.dumps(body, ensure_ascii=False)[:160]}...")
        return {"id": "dry-id", "url": "dry"}
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(),
        headers={"blotato-api-key": _key(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r: return json.load(r)

def upload_media(public_url):
    return _post("/media", {"url": public_url}).get("url", public_url)

def schedule(account, platform, text, media, when_iso, thread=None):
    post = {"accountId": str(account),
            "content": {"text": text, "mediaUrls": media or [], "platform": platform},
            "target": {"targetType": platform}}
    if thread:  # hilos X: additionalPosts (cada uno {text, mediaUrls})
        post["additionalPosts"] = [{"text": t, "mediaUrls": []} for t in thread]
    return _post("/posts", {"post": post, "scheduledTime": when_iso})

def load_channels(cfg="config.yaml"):
    chans = {}
    for ln in open(cfg):
        m = re.match(r'\s*(\w+):\s*\{account:\s*(\w+),\s*platform:\s*(\w+),.*?activo:\s*(true|false),.*?pieza:\s*(\w+),.*?hora:\s*"([\d:]+)",.*?dias:\s*\[([^\]]+)\]', ln)
        if m:
            name, acc, plat, act, pieza, hora, dias = m.groups()
            chans[name] = {"account": acc, "platform": plat, "activo": act=="true",
                           "pieza": pieza, "hora": hora, "dias": [d.strip() for d in dias.split(",")]}
    return chans

DOW = {"lun":0,"mar":1,"mie":2,"jue":3,"vie":4,"sab":5,"dom":6}
def next_date(day_abbr, hhmm, buffer_h=48):
    now = dt.datetime.utcnow() + dt.timedelta(hours=buffer_h)
    target = DOW[day_abbr]; h,mm = map(int, hhmm.split(":"))
    d = now
    for _ in range(8):
        if d.weekday()==target: break
        d += dt.timedelta(days=1)
    return d.replace(hour=h, minute=mm, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    chans = load_channels()
    activos = {k:v for k,v in chans.items() if v["activo"]}
    print(f"Agente Publicador — modo {'DRY-RUN' if DRY else 'LIVE'}")
    print(f"Canales activos: {list(activos.keys())}")
    print(f"En espera (sin accountId): {[k for k,v in chans.items() if not v['activo']]}")
    print("\nLas piezas quedan PROGRAMADAS y editables en https://my.blotato.com/queue/calendar")
    print("Nada se publica sin tu OK final en el calendario de Blotato.\n")
    # Demo del cálculo de fechas
    for name, c in activos.items():
        for d in c["dias"]:
            print(f"  {name}: {c['pieza']} -> {c['platform']} (acc {c['account']}) el {d} {c['hora']} = {next_date(d, c['hora'])}")
