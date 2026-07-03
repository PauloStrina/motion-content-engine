import json, sys

d = json.load(open("transcript.json"))
W = d["palabras"]
print("duracion", d["duracion"], "n_palabras", len(W))

def around(t0, t1):
    # print words whose desde in [t0,t1]
    out = []
    for i, w in enumerate(W):
        if t0 <= w["desde"] <= t1:
            out.append((i, round(w["desde"],2), round(w["hasta"],2), w["w"]))
    return out

# Print a compact index: for each word, i, desde, w  -- but only ranges we care about
ranges = [
    (30, 90),     # transformacion continua good take
    (103, 140),   # cultura sistema operativo
    (165, 232),   # orquestadores
    (236, 326),   # prospeccion futuro
    (366, 452),   # diseno comportamientos
    (519, 588),   # service as a software
    (601, 672),   # kpi liderazgo
]
for (a,b) in ranges:
    print("\n===== %s - %s =====" % (a,b))
    for (i,ds,hs,w) in around(a,b):
        print(i, ds, hs, w)
