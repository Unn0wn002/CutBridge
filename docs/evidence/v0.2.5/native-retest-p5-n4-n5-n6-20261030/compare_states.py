"""Compare retest state dumps and projections (scratch script, copied into the evidence folder)."""
import json
import sys
from pathlib import Path

w = Path(sys.argv[1])


def load(label):
    s = json.loads((w / f"state-{label}.json").read_text(encoding="utf-8"))
    s.pop("label")
    return s


def comp(state):
    return next(i for i in state["items"] if i["typeName"] == "Composition" and i["name"] == "C014_COMP")


def equal(a, b):
    same = load(a) == load(b)
    print(f"state {a} == {b}: {same}")
    return same


results = {}
results["N6 null: before == after refused Build"] = equal("04-before-rebuild-null", "05-after-rebuild-null")
results["N6 camera: before == after refused Build"] = equal("06-before-rebuild-camera", "07-after-rebuild-camera")
results["N5 older: after V003 == after V002 attempt"] = equal("09-after-revision-V003", "11-after-older-attempt")
results["N5 same: after V003 == after V003 attempt"] = equal("09-after-revision-V003", "12-after-same-attempt")

a, b = load("02-after-build"), load("08-restored")
extra = [i["name"] for i in b["items"] if i not in a["items"]]
print("02-after-build vs 08-restored, items only in 08:", extra)
results["restored differs from build only by the artist null's solid"] = comp(a) == comp(b) and all(n.startswith("Null") for n in extra) and len(extra) == 1

for label in ("02-after-build", "09-after-revision-V003"):
    print("==", label)
    for ly in comp(load(label))["layers"]:
        print(f"  [{ly['index']}] {ly['name']} {ly['kind']} 3D={ly['threeD']} comment={ly['comment']!r}")
        if ly["kind"] in ("Camera", "Null"):
            print("     position", ly["position"])
        if ly["kind"] == "Camera":
            print("     pointOfInterest", ly["pointOfInterest"], "\n     zoom", ly["zoom"])
c2, c9 = comp(load("02-after-build")), comp(load("09-after-revision-V003"))
for kind in ("Camera", "Null"):
    l2 = [l for l in c2["layers"] if l["kind"] == kind]
    l9 = [l for l in c9["layers"] if l["kind"] == kind]
    results[f"P5 one managed {kind} after build and after revision"] = len(l2) == 1 and len(l9) == 1 and "CUTBRIDGE|1|" in l2[0]["comment"] and "V003" in l9[0]["comment"]

blender = json.loads((w / "blender_projection_v001.json").read_text(encoding="utf-8"))
for label in ("03b-after-build", "13-after-revision"):
    ae = json.loads((w / f"ae_projection-{label}.json").read_text(encoding="utf-8"))
    worst = 0.0
    for bl, a_ in zip(blender, ae):
        d = max(abs(bl["x_px"] - a_["x_px"]), abs(bl["y_px"] - a_["y_px"]))
        worst = max(worst, d)
        print(f"  {label} frame {bl['frame']}: blender ({bl['x_px']:.4f}, {bl['y_px']:.4f}) ae ({a_['x_px']:.4f}, {a_['y_px']:.4f}) diff {d:.6f} px")
    results[f"P5 projection parity {label} (max diff {worst:.6f} px, limit 0.5 px)"] = len(ae) == len(blender) == 3 and worst <= 0.5

print()
for k, v in results.items():
    print(("PASS " if v else "FAIL ") + k)
(w / "comparison.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
