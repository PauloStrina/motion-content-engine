#!/usr/bin/env python3
"""Descarga el video largo desde Google Drive (link de archivo o de carpeta) y lo deja en <destino>/input.mp4.
Uso: python descargar.py <url_drive> <carpeta_destino>
El link debe estar compartido como "cualquiera con el enlace"."""
import pathlib, shutil, sys
import gdown

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".m4v", ".webm"}


def main(url, destino):
    dest = pathlib.Path(destino)
    dl = dest / "dl"
    dl.mkdir(parents=True, exist_ok=True)
    if "/folders/" in url:
        gdown.download_folder(url=url, output=str(dl), quiet=False, use_cookies=False)
    else:
        gdown.download(url=url, output=str(dl) + "/", quiet=False, fuzzy=True, use_cookies=False)

    files = [p for p in dl.rglob("*") if p.is_file()]
    if not files:
        sys.exit("ERROR: no se descargó nada. ¿El link está compartido como 'cualquiera con el enlace'?")
    vids = [p for p in files if p.suffix.lower() in VIDEO_EXTS] or files
    video = max(vids, key=lambda p: p.stat().st_size)
    shutil.move(str(video), dest / "input.mp4")
    mb = (dest / "input.mp4").stat().st_size / 1e6
    print(f"OK: {video.name} → {dest / 'input.mp4'} ({mb:.0f} MB)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
