#!/usr/bin/env python3
"""Publicador MOTION — lee el manifiesto y manda a cada canal SU pieza.
Hosting de imágenes: subida directa a Blotato (POST /v2/media con archivo). Sin hosting externo.
Modos: --dry (no toca Blotato) · --solo <canal> (un canal) · (sin flags) todos los activos.
Requiere: BLOTATO_API_KEY. accountId/platform desde config.yaml."""
import os, sys, json, re, base64, urllib.request, datetime as dt, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M

API = "https://backend.blotato.com/v2"
DRY = "--dry" in sys.argv
BLOTATO_DELAY_SECONDS = 5
BLOTATO_MAX_INTENTOS = 3

def key():
    return os.environ["BLOTATO_API_KEY"]

def _post(path, body):
    if DRY:
        print(f"  [DRY] POST {path}: {json.dumps(body, ensure_ascii=False)[:140]}")
        return {"id": "dry"}

    for intento in range(1, BLOTATO_MAX_INTENTOS + 1):
        req = urllib.request.Request(
            API + path,
            data=json.dumps(body).encode(),
            headers={
                "blotato-api-key": key(),
                "Content-Type": "application/json"
            }
        )

        try:
            with urllib.request.urlopen(req) as r:
                response = json.load(r)

            print(f"  Blotato response: {json.dumps(response, ensure_ascii=False)[:500]}")

            # Espera entre acciones contra Blotato para no sobrecargar la API
            time.sleep(BLOTATO_DELAY_SECONDS)

            return response

        except urllib.error.HTTPError as e:
            detalle = e.read().decode(errors="replace")[:500]

            if e.code in (429, 500, 502, 503, 504) and intento < BLOTATO_MAX_INTENTOS:
                espera = BLOTATO_DELAY_SECONDS * intento
                print(f"  ⚠ Blotato HTTP {e.code}. Reintento {intento}/{BLOTATO_MAX_INTENTOS} en {espera}s...")
                time.sleep(espera)
                continue

            raise RuntimeError(f"Blotato HTTP {e.code}: {detalle}")

        except Exception as e:
            if intento < BLOTATO_MAX_INTENTOS:
                espera = BLOTATO_DELAY_SECONDS * intento
                print(f"  ⚠ Error temporal en Blotato. Reintento {intento}/{BLOTATO_MAX_INTENTOS} en {espera}s...")
                print(f"  Detalle: {e}")
                time.sleep(espera)
                continue

            raise RuntimeError(f"Error llamando a Blotato: {e}")

def _validar_respuesta_blotato(response):
    if response is None:
        raise RuntimeError("Respuesta vacía de Blotato")

    if response == {}:
        raise RuntimeError("Respuesta vacía de Blotato")

    response_text = json.dumps(response, ensure_ascii=False).lower()

    errores = [
        "error",
        "failed",
        "invalid",
        "unauthorized",
        "forbidden",
        "rate limit",
        "too many requests"
    ]

    for err in errores:
        if err in response_text:
            raise RuntimeError(f"Respuesta inválida de Blotato: {response}")

    return True

def subir_imagen(path_png):
    """Sube un PNG local a Blotato y devuelve la URL validada. Endpoint /v2/media con base64."""
    if DRY:
        print(f"  [DRY] subir media: {os.path.basename(path_png)}")
        return f"blotato://dry/{os.path.basename(path_png)}"

    data = base64.b64encode(open(path_png, "rb").read()).decode()
    r = _post("/media", {"file": data, "fileName": os.path.basename(path_png)})
    _validar_respuesta_blotato(r)

    url = r.get("url")
    if not url:
        raise RuntimeError(f"Blotato no devolvió URL para la imagen: {r}")

    return url

# ── config.yaml: canal -> {account, platform} ──
def load_cfg(cfg="config.yaml"):
    chans = {}
    if not os.path.exists(cfg):
        return chans

    for ln in open(cfg):
        m = re.match(
            r'\s*(\w+):\s*\{account:\s*(\w+),\s*platform:\s*(\w+)(?:.*?pageid:\s*(\w+))?',
            ln
        )
        if m:
            chans[m.group(1)] = {
                "account": m.group(2),
                "platform": m.group(3),
                "pageid": m.group(4)
            }

    return chans

DOW = {
    "lun": 0,
    "mar": 1,
    "mie": 2,
    "jue": 3,
    "vie": 4,
    "sab": 5,
    "dom": 6
}

def fecha(dia, hhmm, buf=48):
    now = dt.datetime.now(dt.UTC) + dt.timedelta(hours=buf)
    h, mm = map(int, hhmm.split(":"))
    d = now

    for _ in range(8):
        if d.weekday() == DOW[dia]:
            break
        d += dt.timedelta(days=1)

    return d.replace(hour=h, minute=mm, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

def _programar_raw(account, platform, text, when, media=None, hilo=None, page_id=None):
    target = {"targetType": platform}

    if page_id:
        target["pageId"] = str(page_id)   # LinkedIn página de empresa

    post = {
        "accountId": str(account),
        "content": {
            "text": text,
            "mediaUrls": media or [],
            "platform": platform
        },
        "target": target
    }

    if hilo:
        post["additionalPosts"] = [
            {
                "text": t,
                "mediaUrls": []
            }
            for t in hilo
        ]

    response = _post("/posts", {"post": post, "scheduledTime": when})
    _validar_respuesta_blotato(response)

    return response

# Programación por canal (día/hora) — coherente con config
HORARIOS = {
    "linkedin_paulo": ("jue", "09:00"),
    "linkedin_motion": ("mie", "11:00"),
    "x_paulo": ("mar", "08:30"),
    "instagram": ("vie", "12:00")
}

def publicar(m, cfg, png_dir, solo=None):
    fallos = []

    for canal in M.CANALES:
        if solo and canal != solo:
            continue

        p = M.pieza(m, canal)

        if not p:
            continue

        if canal not in cfg:
            print(f"  ⏭  {canal}: sin accountId en config (omitido)")
            continue

        acc, plat = cfg[canal]["account"], cfg[canal]["platform"]

        if acc in ("PENDIENTE", ""):
            print(f"  ⏭  {canal}: accountId PENDIENTE (omitido)")
            continue

        dia, hora = HORARIOS.get(canal, ("jue", "09:00"))
        when = fecha(dia, hora)
        fmt = p["formato"]

        print(f"\n▶ {canal} ({plat}, acc {acc}) → {when}")

        try:
            if fmt == "post":
                print(f"  texto: {p['texto'][:70]}...")
                response = _programar_raw(
                    acc,
                    plat,
                    p["texto"],
                    when,
                    page_id=cfg[canal].get("pageid")
                )

            elif fmt == "hilo":
                print(f"  hilo de {len(p['hilo'])} tweets")
                response = _programar_raw(
                    acc,
                    plat,
                    p["hilo"][0],
                    when,
                    hilo=p["hilo"][1:]
                )

            elif fmt == "carrusel":
                n = p["carrusel_slides"]
                base = p["carrusel"]
                media_base = os.environ.get(
                    "MEDIA_BASE",
                    "https://ops-motionco.github.io/motion-media/carruseles"
                )
                urls = [
                    f"{media_base}/{base}-{i}.png"
                    for i in range(1, n + 1)
                ]

                print(f"  carrusel {base}: {n} slides (URLs públicas de motion-media)")
                print(f"  caption: {p['caption'][:60]}...")

                response = _programar_raw(
                    acc,
                    plat,
                    p["caption"],
                    when,
                    media=urls
                )

            else:
                raise RuntimeError(f"Formato no soportado: {fmt}")

            print("  ✓ programado confirmado por Blotato")

        except Exception as e:
            print(f"  ✗ ERROR en {canal}: {e}")
            fallos.append(canal)

    return fallos

if __name__ == "__main__":
    solo = None

    if "--solo" in sys.argv:
        solo = sys.argv[sys.argv.index("--solo") + 1]

    m = M.mas_reciente()

    if not m:
        print("No hay manifiesto.")
        sys.exit(0)

    errs = M.validar(m)

    if errs:
        print("Manifiesto inválido:", errs)
        sys.exit(1)

    cfg = load_cfg()
    png_dir = os.environ.get("PNG_DIR", "media_out")

    print(f"Publicador — {'DRY' if DRY else 'LIVE'} — episodio {m['episodio']}")
    print("Modo revisión: todo queda PROGRAMADO y editable en https://my.blotato.com/queue/calendar")

    fallos = publicar(m, cfg, png_dir, solo)

    if fallos:
        print(f"\n⚠ {len(fallos)} canal(es) con error: {fallos}")
        print("Los demás se programaron OK. Revisá esos canales en Blotato.")
        sys.exit(1)
    else:
        print("\n✓ Todos los canales activos se programaron sin errores.")
