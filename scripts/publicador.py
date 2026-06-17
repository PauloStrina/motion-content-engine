#!/usr/bin/env python3
"""Publicador MOTION — lee el manifiesto y manda a cada canal SU pieza.
Hosting de imágenes: subida directa a Blotato (POST /v2/media con archivo). Sin hosting externo.
Modos: --dry (no toca Blotato) · --solo <canal> (un canal) · (sin flags) todos los activos.
Requiere: BLOTATO_API_KEY. accountId/platform desde config.yaml."""
import os, sys, json, re, base64, urllib.request, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M

API = "https://backend.blotato.com/v2"
DRY = "--dry" in sys.argv
def key(): return os.environ["BLOTATO_API_KEY"]

def _post(path, body):
    if DRY:
        print(f"  [DRY] POST {path}: {json.dumps(body, ensure_ascii=False)[:140]}")
        return {"id":"dry"}
    req = urllib.request.Request(API+path, data=json.dumps(body).encode(),
        headers={"blotato-api-key":key(),"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:300]
        raise RuntimeError(f"Blotato HTTP {e.code}: {detalle}")

def subir_imagen(path_png):
    """Sube un PNG local a Blotato y devuelve la URL validada. Endpoint /v2/media con base64."""
    if DRY:
        print(f"  [DRY] subir media: {os.path.basename(path_png)}")
        return f"blotato://dry/{os.path.basename(path_png)}"
    data = base64.b64encode(open(path_png,"rb").read()).decode()
    r = _post("/media", {"file": data, "fileName": os.path.basename(path_png)})
    return r.get("url")

# ── config.yaml: canal -> {account, platform} ──
def load_cfg(cfg="config.yaml"):
    chans={}
    if not os.path.exists(cfg): return chans
    for ln in open(cfg):
        m=re.match(r'\s*(\w+):\s*\{account:\s*(\w+),\s*platform:\s*(\w+)', ln)
        if m: chans[m.group(1)]={"account":m.group(2),"platform":m.group(3)}
    return chans

DOW={"lun":0,"mar":1,"mie":2,"jue":3,"vie":4,"sab":5,"dom":6}
def fecha(dia, hhmm, buf=48):
    now=dt.datetime.now(dt.UTC)+dt.timedelta(hours=buf); h,mm=map(int,hhmm.split(":")); d=now
    for _ in range(8):
        if d.weekday()==DOW[dia]: break
        d+=dt.timedelta(days=1)
    return d.replace(hour=h,minute=mm,second=0,microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

def _programar_raw(account, platform, text, when, media=None, hilo=None):
    post={"accountId":str(account),
          "content":{"text":text,"mediaUrls":media or [],"platform":platform},
          "target":{"targetType":platform}}
    if hilo: post["additionalPosts"]=[{"text":t,"mediaUrls":[]} for t in hilo]
    return _post("/posts", {"post":post,"scheduledTime":when})

# Programación por canal (día/hora) — coherente con config
HORARIOS={"linkedin_paulo":("jue","09:00"),"linkedin_motion":("mie","11:00"),
          "x_paulo":("mar","08:30"),"instagram":("vie","12:00")}

def publicar(m, cfg, png_dir, solo=None):
    fallos = []
    for canal in M.CANALES:
        if solo and canal!=solo: continue
        p = M.pieza(m, canal)
        if not p: continue
        if canal not in cfg:
            print(f"  ⏭  {canal}: sin accountId en config (omitido)"); continue
        acc, plat = cfg[canal]["account"], cfg[canal]["platform"]
        if acc in ("PENDIENTE",""): 
            print(f"  ⏭  {canal}: accountId PENDIENTE (omitido)"); continue
        dia,hora = HORARIOS.get(canal, ("jue","09:00"))
        when = fecha(dia, hora)
        fmt = p["formato"]
        print(f"\n▶ {canal} ({plat}, acc {acc}) → {when}")
        try:
            if fmt=="post":
                print(f"  texto: {p['texto'][:70]}...")
                _programar_raw(acc, plat, p["texto"], when)
            elif fmt=="hilo":
                print(f"  hilo de {len(p['hilo'])} tweets")
                _programar_raw(acc, plat, p["hilo"][0], when, hilo=p["hilo"][1:])
            elif fmt=="carrusel":
                n=p["carrusel_slides"]; base=p["carrusel"]
                print(f"  carrusel {base}: {n} slides → subiendo imágenes...")
                urls=[]
                ok=True
                for i in range(1,n+1):
                    png=os.path.join(png_dir, f"{base}-{i}.png")
                    if not os.path.exists(png):
                        print(f"  ⚠ falta {png} — abortando carrusel"); ok=False; break
                    urls.append(subir_imagen(png))
                if not ok:
                    fallos.append(canal); continue
                print(f"  caption: {p['caption'][:60]}...")
                _programar_raw(acc, plat, p["caption"], when, media=urls)
            print("  ✓ programado (editable en calendario Blotato)")
        except Exception as e:
            print(f"  ✗ ERROR en {canal}: {e}")
            fallos.append(canal)
    return fallos

if __name__=="__main__":
    solo=None
    if "--solo" in sys.argv: solo=sys.argv[sys.argv.index("--solo")+1]
    m=M.mas_reciente()
    if not m: print("No hay manifiesto."); sys.exit(0)
    errs=M.validar(m)
    if errs: print("Manifiesto inválido:",errs); sys.exit(1)
    cfg=load_cfg()
    png_dir=os.environ.get("PNG_DIR","media_out")
    print(f"Publicador — {'DRY' if DRY else 'LIVE'} — episodio {m['episodio']}")
    print(f"Modo revisión: todo queda PROGRAMADO y editable en https://my.blotato.com/queue/calendar")
    fallos = publicar(m, cfg, png_dir, solo)
    if fallos:
        print(f"\n⚠ {len(fallos)} canal(es) con error: {fallos}")
        print("Los demás se programaron OK. Revisá esos canales en Blotato.")
    else:
        print("\n✓ Todos los canales activos se programaron sin errores.")
