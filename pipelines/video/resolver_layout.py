#!/usr/bin/env python3
"""Resuelve el layout visual por reel sin coordenadas manuales."""
from __future__ import annotations

import argparse
import json
import pathlib
from statistics import median
from typing import Any

import cv2
import numpy as np

BASE = pathlib.Path(__file__).resolve().parents[2]
MODOS = {"auto_per_reel", "zones_single_file", "camera_only", "split_two_files", "keep_manifest"}


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def tiempos_representativos(reel: dict[str, Any], max_frames: int = 7) -> list[float]:
    tiempos: list[float] = []
    for seg in reel.get("segmentos", []):
        a, b = float(seg["desde"]), float(seg["hasta"])
        tiempos.append((a + b) / 2)
        if b - a >= 12:
            tiempos.extend((a + 2.0, b - 2.0))
    unicos: list[float] = []
    for t in sorted(tiempos):
        if not unicos or abs(t - unicos[-1]) > 1.0:
            unicos.append(t)
    if len(unicos) <= max_frames:
        return unicos
    indices = np.linspace(0, len(unicos) - 1, max_frames).round().astype(int)
    return [unicos[i] for i in indices]


def leer_frame(cap: cv2.VideoCapture, segundo: float) -> np.ndarray | None:
    cap.set(cv2.CAP_PROP_POS_MSEC, segundo * 1000)
    ok, frame = cap.read()
    return frame if ok else None


def union_caras(frame: np.ndarray, detector: cv2.CascadeClassifier) -> tuple[float, float, float, float] | None:
    h, w = frame.shape[:2]
    gris = cv2.equalizeHist(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    escala = 1.5
    grande = cv2.resize(gris, None, fx=escala, fy=escala, interpolation=cv2.INTER_LINEAR)
    minimo = max(28, int(min(h, w) * 0.035 * escala))
    caras = detector.detectMultiScale(
        grande,
        scaleFactor=1.08,
        minNeighbors=5,
        minSize=(minimo, minimo),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(caras) == 0:
        return None
    cajas = []
    for x, y, cw, ch in caras:
        x, y, cw, ch = (v / escala for v in (x, y, cw, ch))
        if cw * ch < w * h * 0.0007:
            continue
        cajas.append((x / w, y / h, cw / w, ch / h))
    if not cajas:
        return None
    x1 = min(x for x, _, _, _ in cajas)
    y1 = min(y for _, y, _, _ in cajas)
    x2 = max(x + cw for x, _, cw, _ in cajas)
    y2 = max(y + ch for _, y, _, ch in cajas)
    return x1, y1, x2 - x1, y2 - y1


def caja_mediana(cajas: list[tuple[float, float, float, float]]) -> tuple[float, float, float, float] | None:
    if not cajas:
        return None
    return tuple(float(median([c[i] for c in cajas])) for i in range(4))  # type: ignore[return-value]


def expandir_a_9_8(caja: tuple[float, float, float, float], frame_w: int, frame_h: int) -> dict[str, float]:
    x, y, w, h = caja
    cx, cy = x + w / 2, y + h / 2
    w *= 1.75
    h *= 2.05
    objetivo = 9 / 8
    aspecto = (w * frame_w) / max(h * frame_h, 1)
    if aspecto < objetivo:
        w *= objetivo / aspecto
    else:
        h *= aspecto / objetivo
    w, h = min(w, 0.9), min(h, 0.9)
    x = clamp(cx - w / 2, 0, 1 - w)
    y = clamp(cy - h / 2, 0, 1 - h)
    return {"x": round(x, 5), "y": round(y, 5), "w": round(w, 5), "h": round(h, 5)}


def contain(img: np.ndarray, out_w: int, out_h: int) -> np.ndarray:
    h, w = img.shape[:2]
    s = min(out_w / w, out_h / h)
    resized = cv2.resize(img, (max(1, round(w * s)), max(1, round(h * s))))
    canvas = np.zeros((out_h, out_w, 3), dtype=np.uint8)
    y, x = (out_h - resized.shape[0]) // 2, (out_w - resized.shape[1]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return canvas


def cover(img: np.ndarray, out_w: int, out_h: int) -> np.ndarray:
    h, w = img.shape[:2]
    s = max(out_w / w, out_h / h)
    resized = cv2.resize(img, (max(1, round(w * s)), max(1, round(h * s))))
    y, x = (resized.shape[0] - out_h) // 2, (resized.shape[1] - out_w) // 2
    return resized[y:y + out_h, x:x + out_w]


def crop_norm(frame: np.ndarray, zona: dict[str, float]) -> np.ndarray:
    h, w = frame.shape[:2]
    x1 = int(round(zona["x"] * w))
    y1 = int(round(zona["y"] * h))
    x2 = int(round((zona["x"] + zona["w"]) * w))
    y2 = int(round((zona["y"] + zona["h"]) * h))
    return frame[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]


def poster_o_fallback(path: pathlib.Path) -> np.ndarray:
    img = cv2.imread(str(path)) if path.exists() else None
    if img is not None:
        return img
    canvas = np.zeros((590, 1278, 3), dtype=np.uint8)
    cv2.putText(canvas, "MOTION", (430, 330), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 8)
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=pathlib.Path)
    parser.add_argument("sesion_dir", type=pathlib.Path)
    parser.add_argument("--mode", choices=sorted(MODOS), default="auto_per_reel")
    parser.add_argument("--poster", type=pathlib.Path, default=BASE / "design-system/assets/innpulso-fondo.png")
    parser.add_argument("--preview-dir", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, help="Salida resuelta; no modifica el manifiesto editorial")
    args = parser.parse_args()

    source_path = args.sesion_dir / "manifiesto_reels.json"
    output_path = args.output or (args.sesion_dir / "manifiesto_layout_resuelto.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifiesto = json.loads(source_path.read_text(encoding="utf-8-sig"))

    if args.mode == "keep_manifest":
        output_path.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Layout: se conserva el manifiesto sin cambios → {output_path}")
        return 0

    if args.mode == "split_two_files":
        for reel in manifiesto["reels"]:
            reel["modo"] = "split"
            reel.pop("zonas", None)
        output_path.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Layout: todos los reels configurados como split → {output_path}")
        return 0

    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened():
        raise SystemExit(f"No se pudo abrir el video: {args.video}")
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if detector.empty():
        raise SystemExit("No se pudo cargar Haar Cascade de OpenCV")

    preview_dir = args.preview_dir
    if preview_dir:
        preview_dir.mkdir(parents=True, exist_ok=True)
    poster = poster_o_fallback(args.poster)
    reporte: list[dict[str, Any]] = []

    for reel in manifiesto["reels"]:
        tiempos = tiempos_representativos(reel)
        frames: list[np.ndarray] = []
        cajas: list[tuple[float, float, float, float]] = []
        for t in tiempos:
            frame = leer_frame(cap, t)
            if frame is None:
                continue
            frames.append(frame)
            caja = union_caras(frame, detector)
            if caja:
                cajas.append(caja)

        representativo = frames[len(frames) // 2] if frames else None
        caja = caja_mediana(cajas)
        deteccion = len(cajas) / max(len(frames), 1)
        area = caja[2] * caja[3] if caja else 1.0
        centro_x = caja[0] + caja[2] / 2 if caja else 0.5
        centro_y = caja[1] + caja[3] / 2 if caja else 0.5
        en_borde = centro_x < 0.32 or centro_x > 0.68 or centro_y < 0.30 or centro_y > 0.70

        usar_zonas = (
            args.mode in {"auto_per_reel", "zones_single_file"}
            and caja is not None
            and deteccion >= 0.34
            and area <= 0.28
            and en_borde
        )
        if args.mode == "camera_only":
            usar_zonas = False

        if usar_zonas:
            camara = expandir_a_9_8(caja, frame_w, frame_h)
            reel["modo"] = "zonas"
            reel["zonas"] = {
                "pantalla": {"x": 0.0, "y": 0.0, "w": 1.0, "h": 1.0},
                "camara": camara,
            }
            decision = "zonas"
        else:
            reel["modo"] = "poster"
            reel.pop("zonas", None)
            decision = "poster"

        diag = {
            "reel": reel.get("n"),
            "slug": reel.get("slug"),
            "decision": decision,
            "frames_analizados": len(frames),
            "deteccion_rostros": round(deteccion, 3),
            "area_union_rostros": round(area, 4) if caja else None,
            "caja_mediana": [round(v, 5) for v in caja] if caja else None,
        }
        reporte.append(diag)
        print(json.dumps(diag, ensure_ascii=False))

        if preview_dir and representativo is not None:
            if decision == "zonas":
                arriba = contain(representativo, 1080, 960)
                abajo = cover(crop_norm(representativo, reel["zonas"]["camara"]), 1080, 960)
            else:
                arriba = cover(poster, 1080, 960)
                abajo = cover(representativo, 1080, 960)
            preview = np.vstack([arriba, abajo])
            cv2.imwrite(str(preview_dir / f"reel_{reel['n']}_{reel['slug']}.jpg"), preview, [cv2.IMWRITE_JPEG_QUALITY, 88])

    cap.release()
    manifiesto["layout_resuelto"] = {
        "modo_solicitado": args.mode,
        "poster": str(args.poster),
        "motor": "opencv-haar-v1",
    }
    output_path.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if preview_dir:
        (preview_dir / "layout_report.json").write_text(
            json.dumps(reporte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (preview_dir / "manifiesto_resuelto.json").write_text(
            json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
