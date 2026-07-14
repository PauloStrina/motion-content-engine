import json, sys
d = json.load(open("transcript.json"))
W = d["palabras"]
print("DURACION", d["duracion"], "NWORDS", len(W))

def show(a, b):
    print(f"\n=== window {a}-{b} ===")
    for w in W:
        if w["hasta"] >= a and w["desde"] <= b:
            print(f'{w["desde"]:8.2f} {w["hasta"]:8.2f}  {w["w"]}')

for a, b in [(145, 190), (505, 600)]:
    show(a, b)
