#!/usr/bin/env python3
"""Agente Publicador MOTION — programa en Blotato (modo revisión: fecha futura, editable en calendario).
Lee config.yaml + extrae el texto real de queue/approved/. Endpoints verificados jun 2026.
Modos:
  --dry           : muestra qué haría, sin tocar Blotato
  --solo-prueba   : programa UNA sola pieza (post LinkedIn personal) — para el primer test en vivo
  (sin flags)     : programa todas las piezas activas
"""
import os, sys, json, re, glob, urllib.request, datetime as dt

API = "https://backend.blotato.com/v2"
DRY = "--dry" in sys.argv
SOLO = "--solo-prueba" in sys.argv
def _key(): return os.environ["BLOTATO_API_KEY"]

def _post(path, body):
    if DRY:
        print(f"  [DRY] POST {path}: {json.dumps(body, ensure_ascii=False)[:200]}")
        return {"id":"dry","url":"dry"}
    req = urllib.request.Request(API+path, data=json.dumps(body).encode(),
        headers={"blotato-api-key":_key(),"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as r: return json.load(r)

def schedule(account, platform, text, when_iso, thread=None, media=None):
    post = {"accountId":str(account),
            "content":{"text":text,"mediaUrls":media or [],"platform":platform},
            "target":{"targetType":platform}}
    if thread: post["additionalPosts"]=[{"text":t,"mediaUrls":[]} for t in thread]
    return _post("/posts", {"post":post, "scheduledTime":when_iso})

DOW={"lun":0,"mar":1,"mie":2,"jue":3,"vie":4,"sab":5,"dom":6}
def next_date(day, hhmm, buf=48):
    now=dt.datetime.now(dt.UTC)+dt.timedelta(hours=buf)
    h,mm=map(int,hhmm.split(":")); d=now
    for _ in range(8):
        if d.weekday()==DOW[day]: break
        d+=dt.timedelta(days=1)
    return d.replace(hour=h,minute=mm,second=0,microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Extraer el texto del post de LinkedIn personal desde la cascada aprobada ──
def extraer_post_linkedin(md_text):
    """Toma el bloque 'POST LINKEDIN — PERFIL PAULO' (variante A) de la cascada."""
    # busca desde el encabezado del post hasta el siguiente encabezado de sección (##, ---, o "##")
    m = re.search(r'POST LINKEDIN.*?PERFIL.*?\n(.*?)(?:\n##|\n---|\n\d\s·|POST LINKEDIN — P[ÁA]GINA)', md_text, re.S|re.I)
    if not m: return None
    bloque = m.group(1)
    # quitar subtítulos de variante y quedarse con el cuerpo de la variante A
    bloque = re.sub(r'###?\s*Variante [AB].*?\n', '', bloque)
    bloque = re.split(r'###?\s*Variante B', bloque)[0]
    return bloque.strip()

def cascada_mas_reciente():
    files = sorted(glob.glob("queue/approved/*.md"), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


# ── Carrusel de imágenes para Instagram/LinkedIn (URLs públicas vía GitHub Pages) ──
# PAGES_BASE se completa con la URL que GitHub te da al activar Pages.
PAGES_BASE = os.environ.get("PAGES_BASE", "https://ops-motionco.github.io/motion-media")

def carrusel_urls(rel_dir, base_name, n_slides):
    """Construye las URLs públicas de los PNG del carrusel (1..n)."""
    return [f"{PAGES_BASE}/{rel_dir}/{base_name}-{i}.png" for i in range(1, n_slides+1)]

def schedule_carrusel(account, platform, caption, image_urls, when_iso):
    post = {"accountId": str(account),
            "content": {"text": caption, "mediaUrls": image_urls, "platform": platform},
            "target": {"targetType": platform}}
    return _post("/posts", {"post": post, "scheduledTime": when_iso})


if __name__=="__main__":
    if "--carrusel-instagram" in sys.argv:
        import glob as _g
        # detectar cuántos PNG hay (asumimos base ejemplo_ep1-1 o el más reciente)
        # las URLs apuntan a motion-media/carruseles/<base>-N.png
        base = os.environ.get("CARRUSEL_BASE", "ejemplo_ep1-1")
        n = int(os.environ.get("CARRUSEL_SLIDES", "8"))
        urls = [f"{PAGES_BASE}/carruseles/{base}-{i}.png" for i in range(1, n+1)]
        # caption: extrae el post de Motion o usa un fallback
        casc = cascada_mas_reciente()
        caption = "Cambio y transformación no son sinónimos. Y distinguirlos lo define todo. #LoComplejoSimple"
        if casc:
            t = extraer_post_linkedin(open(casc, encoding="utf-8").read())
            if t: caption = t
        when = next_date("vie", "12:00")
        print(f"Carrusel Instagram: {len(urls)} slides")
        for u in urls: print("  ", u)
        print(f"Caption:\n{caption}\n")
        print(f"Programado para: {when}")
        if not DRY:
            r = schedule_carrusel(53650, "instagram", caption, urls, when)
            print(f"OK Blotato: {json.dumps(r, ensure_ascii=False)[:160]}")
        sys.exit(0)

    print(f"Agente Publicador — modo {'DRY' if DRY else ('SOLO-PRUEBA' if SOLO else 'LIVE')}\n")
    casc = cascada_mas_reciente()
    if not casc:
        print("No hay cascada en queue/approved/ (.md). Nada para publicar."); sys.exit(0)
    print(f"Cascada fuente: {casc}")
    texto = extraer_post_linkedin(open(casc, encoding='utf-8').read())
    if not texto:
        print("No pude extraer el post de LinkedIn personal de la cascada. Reviso el formato del .md."); sys.exit(1)
    print(f"\n--- TEXTO A PROGRAMAR (LinkedIn personal) ---\n{texto}\n--- fin ---\n")
    when = next_date("jue","09:00")
    print(f"Se programará para: {when} (editable en https://my.blotato.com/queue/calendar)\n")
    if SOLO or not DRY:
        r = schedule(25264, "linkedin", texto, when)
        print(f"OK programado. Respuesta Blotato: {json.dumps(r, ensure_ascii=False)[:160]}")
    else:
        print("(DRY-RUN: no se programó nada)")

