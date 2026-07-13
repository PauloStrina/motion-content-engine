import json, sys
BASE='/home/runner/work/motion-content-engine/motion-content-engine/pipelines/video/reels/2026-07-13-CCU-transformacion-video1/'
d = json.load(open(BASE+'transcript.json'))
W = d['palabras']
print("DURACION", d['duracion'], "NWORDS", len(W))
def show(a, b):
    print(f"\n=== {a}-{b} ===")
    for x in W:
        if x['hasta'] >= a and x['desde'] <= b:
            print(f"{x['desde']:.2f} {x['hasta']:.2f} {x['w']}")
for pair in sys.argv[1:]:
    a,b = pair.split(':')
    show(float(a), float(b))
