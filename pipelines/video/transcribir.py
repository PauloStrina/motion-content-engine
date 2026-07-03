#!/usr/bin/env python3
"""Transcribe un video con timestamps por palabra (faster-whisper, corre en CI).
Uso: python transcribir.py <video.mp4> <carpeta de la sesión>
Genera en la carpeta: transcript.json (palabras con tiempos, lo usa cortar.py)
                    + transcript.md (legible, lo lee el Editor de Video)."""
import json, sys, pathlib


def main(video, outdir):
    from faster_whisper import WhisperModel
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    segments, info = model.transcribe(video, language="es", word_timestamps=True, vad_filter=True)

    words, lines = [], []
    for seg in segments:
        for w in seg.words or []:
            words.append({"w": w.word.strip(), "desde": round(w.start, 2), "hasta": round(w.end, 2)})
        m, s = divmod(int(seg.start), 60)
        lines.append(f"[{m:02d}:{s:02d} — {seg.start:.1f}s] {seg.text.strip()}")

    data = {"duracion": round(info.duration, 2), "palabras": words}
    (out / "transcript.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "transcript.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: {len(words)} palabras, {info.duration:.0f}s de video → {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
