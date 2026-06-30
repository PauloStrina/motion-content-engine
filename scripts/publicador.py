#!/usr/bin/env python3
"""Publicador MOTION — lee el manifiesto y manda a cada canal SU pieza.
Modos:
  --dry              : no toca Blotato
  --solo <canal>     : un solo canal
  --fecha <YYYY-MM-DD>: elige la semana a publicar (default: el manifiesto más reciente)
Requiere: BLOTATO_API_KEY. accountId/platform/pageid desde config.yaml."""
import os, sys, json, re, base64, urllib.request, datetime as dt, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M

API = "https://backend.blotato.com/v2"
DRY = "--dry" in sys.argv
BLOTATO_DELAY_SECONDS = 5
BLOTATO_MAX_INTENTOS = 3
def key(): return os.environ["BLOTATO_API_KEY"]

def _upload_presigned(local_path):
    """Upload local file to Blotato via presigned URL. Returns publicUrl."""
    filename = os.path.basename(local_path)
    r = _post("/media/uploads", {"filename": filename})
    presigned_url = r["presignedUrl"]; public_url = r["publicUrl"]
    ext = filename.rsplit(".", 1)[-1].lower()
    ct = {"pdf":"application/pdf","png":"image/png","jpg":"image/jpeg","mp4":"video/mp4"}.get(ext,"application/octet-stream")
    with open(local_path, "rb") as f: data = f.read()
    req = urllib.request.Request(presigned_url, data=data, method="PUT", headers={"Content-Type": ct})
    urllib.request.urlopen(req)
    print(f"  ✓ uploaded to Blotato CDN: {public_url}")
    return public_url

def _post(path, body):
    if DRY:
        print(f"  [DRY] POST {path}: {json.dumps(body, ensure_ascii=False)[:140]}")
        return {"id": "dry"}
    for intento in range(1, BLOTATO_MAX_INTENTOS + 1):
        req = urllib.request.Request(API + path, data=json.dumps(body).encode(),
            headers={"blotato-api-key": key(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                response = json.load(r)
            print(f"  Blotato response: {json.dumps(response, ensure_ascii=False)[:300]}")
            time.sleep(BLOTATO_DELAY_SECONDS)
            return response
        except urllib.error.HTTPError as e:
            detalle = e.read().decode(errors="replace")[:500]
            if e.code in (429,500,502,503,504) and intento < BLOTATO_MAX_INTENTOS:
                espera = BLOTATO_DELAY_SECONDS * intento
                print(f"  ⚠ Blotato HTTP {e.code}. Reintento {intento}/{BLOTATO_MAX_INTENTOS} en {espera}s...")
                time.sleep(espera); continue
            raise RuntimeError(f"Blotato HTTP {e.code}: {detalle}")
        except Exception as e:
            if intento < BLOTATO_MAX_INTENTOS:
                espera = BLOTATO_DELAY_SECONDS * intento
                print(f"  ⚠ Error temporal. Reintento {intento}/{BLOTATO_MAX_INTENTOS} en {espera}s..."); 
                time.sleep(espera); continue
            raise RuntimeError(f"Error llamando a Blotato: {e}")

def _validar(r):
    if not r: raise RuntimeError("Respuesta vacía de Blotato")
    t = json.dumps(r, ensure_ascii=False).lower()
    for err in ("error","failed","invalid","unauthorized","forbidden","rate limit","too many requests"):
        if err in t: raise RuntimeError(f"Respuesta inválida de Blotato: {r}")
    return True

def load_cfg(cfg="config.yaml"):
    chans = {}
    if not os.path.exists(cfg): return chans
    for ln in open(cfg):
        m = re.match(r'\s*(\w+):\s*\{account:\s*(\w+),\s*platform:\s*(\w+)(?:.*?pageid:\s*(\w+))?', ln)
        if m: chans[m.group(1)] = {"account":m.group(2),"platform":m.group(3),"pageid":m.group(4)}
    return chans

DOW = {"lun":0,"mar":1,"mie":2,"jue":3,"vie":4,"sab":5,"dom":6}
def fecha_en_semana(fecha_inicio_iso, dia, hhmm):
    """Fecha/hora del 'dia' (mar/mie/jue) en la semana de fecha_inicio_iso.
    Normaliza al lunes de esa semana ISO, así sirve cualquier día que ponga Paulo."""
    base = dt.date.fromisoformat(fecha_inicio_iso)
    lunes = base - dt.timedelta(days=base.weekday())
    target = lunes + dt.timedelta(days=DOW[dia])
    h,mm = map(int, hhmm.split(":"))
    return dt.datetime(target.year,target.month,target.day,h,mm).strftime("%Y-%m-%dT%H:%M:%SZ")

def _programar_raw(account, platform, text, when, media=None, hilo=None, page_id=None, name=None):
    target = {"targetType": platform}
    if page_id: target["pageId"] = str(page_id)
    post = {"accountId":str(account),"content":{"text":text,"mediaUrls":media or [],"platform":platform},"target":target}
    if name: post["name"] = name
    if hilo: post["additionalPosts"] = [{"text":t,"mediaUrls":[]} for t in hilo]
    r = _post("/posts", {"post":post,"scheduledTime":when})
    _validar(r); return r

# Día y hora fijos por canal dentro de la semana (martes carousel · miércoles motion · jueves newsletter)
CANAL_SCHEDULE = {
    "linkedin_paulo":       ("mar","09:00"),
    "instagram":            ("mar","12:00"),
    "x_paulo_hem":          ("mar","08:30"),
    "linkedin_motion":      ("mie","11:00"),
    "instagram_newsletter": ("jue","12:00"),
    "x_paulo_news":         ("jue","08:30"),
}

def publicar(m, cfg, solo=None):
    fallos = []
    media_base = os.environ.get("MEDIA_BASE","https://ops-motionco.github.io/motion-media/carruseles")
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M")
    run_name = f"{m['fecha_inicio']}_{stamp}"
    for canal in M.CANALES:
        if solo and canal!=solo: continue
        p = M.pieza(m, canal)
        if not p: continue
        if canal not in cfg: print(f"  ⏭  {canal}: sin config"); continue
        acc, plat = cfg[canal]["account"], cfg[canal]["platform"]
        if acc in ("PENDIENTE",""): print(f"  ⏭  {canal}: accountId PENDIENTE"); continue
        dia,hora = CANAL_SCHEDULE.get(canal,("mar","09:00")); when = fecha_en_semana(m["fecha_inicio"],dia,hora); fmt = p["formato"]
        print(f"\n▶ {canal} ({plat}, acc {acc}) → {when}")
        try:
            if fmt=="post":
                print(f"  texto: {p['texto'][:70]}...")
                _programar_raw(acc, plat, p["texto"], when, page_id=cfg[canal].get("pageid"), name=f"{run_name}_{canal}")
            elif fmt=="hilo":
                print(f"  hilo de {len(p['hilo'])} tweets")
                _programar_raw(acc, plat, p["hilo"][0], when, hilo=p["hilo"][1:], name=f"{run_name}_{canal}")
            elif fmt=="carrusel":
                # Carrusel = imágenes PNG en TODOS los canales (incluido LinkedIn).
                # El PDF de LinkedIn falla en Blotato ("failed to read media metadata"): se sigue
                # generando y queda en motion-media para publicar a mano, pero Blotato usa los PNG.
                base = p["carrusel"]; n = p["carrusel_slides"]
                urls = [f"{media_base}/{base}-{i}.png" for i in range(1, n+1)]
                texto = p.get("texto") or p.get("caption")
                print(f"  carrusel {base}: {n} imágenes")
                print(f"  texto: {texto[:60]}...")
                _programar_raw(acc, plat, texto, when, media=urls, page_id=cfg[canal].get("pageid"), name=f"{run_name}_{canal}")
            else:
                raise RuntimeError(f"Formato no soportado: {fmt}")
            print("  ✓ programado confirmado por Blotato")
        except Exception as e:
            print(f"  ✗ ERROR en {canal}: {e}"); fallos.append(canal)
    return fallos

if __name__ == "__main__":
    solo = None
    if "--solo" in sys.argv: solo = sys.argv[sys.argv.index("--solo")+1]
    # SELECCIÓN DE SEMANA: --fecha YYYY-MM-DD (lunes), o el manifiesto más reciente por defecto
    if "--fecha" in sys.argv:
        clave = sys.argv[sys.argv.index("--fecha")+1]
        try: m = M.leer(clave)
        except Exception: print(f"No existe manifiesto para {clave}"); sys.exit(1)
    else:
        m = M.mas_reciente()
    if not m: print("No hay manifiesto."); sys.exit(0)
    errs = M.validar(m)
    if errs: print("Manifiesto inválido:", errs); sys.exit(1)
    cfg = load_cfg()
    print(f"Publicador — {'DRY' if DRY else 'LIVE'} — semana {m['fecha_inicio']}")
    print("Modo revisión: todo PROGRAMADO y editable en https://my.blotato.com/queue/calendar")
    fallos = publicar(m, cfg, solo)
    if fallos:
        print(f"\n⚠ {len(fallos)} canal(es) con error: {fallos}"); sys.exit(1)
    print("\n✓ Todos los canales activos se programaron sin errores.")
