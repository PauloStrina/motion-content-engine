#!/usr/bin/env python3
"""Publicador MENSUAL — programa en Blotato el mes completo (4 semanas × 4 días × 2 canales).
Canales del esquema mensual: linkedin_paulo + instagram (cada uno su pieza, cada día).
Formatos por día:
  video          → mismo reel en ambos canales (presigned upload a Blotato CDN desde el clone
                   local de motion-media; fallback: URL pública de Pages), caption propio.
  carousel_news  → carrusel PNGs en ambos (LinkedIn: Blotato arma el documento). El newsletter
                   de ese día es MANUAL (Blotato no soporta newsletters de LinkedIn).
  post_carousel  → LinkedIn: post largo solo texto · Instagram: carrusel PNGs.
  faltante_video → publica su fallback como post_carousel y avisa.
Al programar un día video, marca el reel como "publicado" en banco/reels/catalogo.json
(el workflow commitea el catálogo).
Modos: --dry (no toca Blotato) · --mes YYYY-MM (requerido).
Requiere: BLOTATO_API_KEY, config.yaml, y REELS_DIR (dir local con los MP4, ej media_repo/reels)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mes as MES
import publicador as P

HORA = {"linkedin_paulo": "09:00", "instagram": "12:00"}


def _media_video(reel, reels_dir):
    """Devuelve la URL del video para Blotato: presigned upload del archivo local si existe,
    sino la URL pública de motion-media Pages."""
    local = os.path.join(reels_dir, reel["archivo"]) if reels_dir else None
    if local and os.path.exists(local):
        if P.DRY:
            print(f"  [DRY] presigned upload de {local}")
            return reel["url"]
        return P._upload_presigned(local)
    print(f"  ⚠ {reel['archivo']} no está local — uso URL de Pages ({reel['url']})")
    return reel["url"]


def publicar_mes(m, cfg, reels_dir):
    fallos, publicados_reels = [], []
    media_base = os.environ.get("MEDIA_BASE", "https://ops-motionco.github.io/motion-media/carruseles")
    cat = MES.leer_catalogo()
    for semana in m["semanas"]:
        fi = semana["fecha_inicio"]
        for d in MES.DIAS:
            dia = semana["dias"].get(d)
            if not dia: continue
            fmt = dia["formato"]
            if fmt == "faltante_video":
                print(f"\n⚠ {fi}/{d}: video FALTANTE (grabar: {dia.get('grabar','?')}) — publico el fallback")
                fmt = "post_carousel"
            video_url = None
            if fmt == "video":
                reel = MES.reel_por_id(cat, dia["reel_id"])
                if not reel:
                    print(f"\n✗ {fi}/{d}: reel_id {dia['reel_id']} no está en el catálogo")
                    fallos.append(f"{fi}/{d}"); continue
                video_url = _media_video(reel, reels_dir)
            for canal in ("linkedin_paulo", "instagram"):
                if canal not in cfg: print(f"  ⏭ {canal}: sin config"); continue
                acc, plat = cfg[canal]["account"], cfg[canal]["platform"]
                if acc in ("PENDIENTE", ""): print(f"  ⏭ {canal}: accountId PENDIENTE"); continue
                when = MES.fecha_dia(fi, d, HORA[canal])
                texto = dia["texto_linkedin"] if canal == "linkedin_paulo" else dia["caption_instagram"]
                name = f"mes{m['mes']}_{fi}_{d}_{canal}"
                print(f"\n▶ {fi}/{d} [{dia['tipo']}/{fmt}] {canal} → {when}")
                try:
                    if fmt == "video":
                        P._programar_raw(acc, plat, texto, when, media=[video_url],
                                         page_id=cfg[canal].get("pageid"), name=name)
                    elif fmt == "post_carousel" and canal == "linkedin_paulo":
                        P._programar_raw(acc, plat, texto, when,
                                         page_id=cfg[canal].get("pageid"), name=name)
                    else:  # carrusel PNGs (carousel_news ambos canales; post_carousel solo IG)
                        base = dia["carrusel"]; n = dia["carrusel_slides"]
                        urls = [f"{media_base}/{base}-{i}.png" for i in range(1, n + 1)]
                        P._programar_raw(acc, plat, texto, when, media=urls,
                                         page_id=cfg[canal].get("pageid"), name=name)
                    print("  ✓ programado")
                except Exception as e:
                    print(f"  ✗ ERROR {fi}/{d}/{canal}: {e}"); fallos.append(f"{fi}/{d}/{canal}")
            if fmt == "video" and f"{fi}/{d}" not in fallos:
                publicados_reels.append(dia["reel_id"])
    # marcar reels programados como publicados
    if publicados_reels and not P.DRY:
        for r in cat["reels"]:
            if r["id"] in publicados_reels:
                r["estado"] = "publicado"
        MES.escribir_catalogo(cat)
        print(f"\nCatálogo: {len(publicados_reels)} reels marcados como publicados.")
    return fallos


if __name__ == "__main__":
    if "--mes" not in sys.argv:
        print("Uso: publicador_mes.py --mes YYYY-MM [--dry]"); sys.exit(1)
    mes_id = sys.argv[sys.argv.index("--mes") + 1]
    try:
        m = MES.leer(mes_id)
    except Exception:
        print(f"No existe manifiesto mensual para {mes_id}"); sys.exit(1)
    errs = MES.validar(m)
    if errs:
        print("Manifiesto mensual inválido:")
        for e in errs: print(" -", e)
        sys.exit(1)
    cfg = P.load_cfg()
    reels_dir = os.environ.get("REELS_DIR", "media_repo/reels")
    print(f"Publicador mensual — {'DRY' if P.DRY else 'LIVE'} — mes {mes_id}")
    print("Modo revisión: todo PROGRAMADO y editable en https://my.blotato.com/queue/calendar")
    fallos = publicar_mes(m, cfg, reels_dir)
    if fallos:
        print(f"\n⚠ {len(fallos)} pieza(s) con error: {fallos}"); sys.exit(1)
    print("\n✓ Mes completo programado sin errores.")
