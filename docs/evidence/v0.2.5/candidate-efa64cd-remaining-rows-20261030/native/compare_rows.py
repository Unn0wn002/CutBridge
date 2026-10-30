"""Compare the N1-N3 / P3 state dumps (scratch script, copied into the evidence folder)."""
import hashlib
import json
import sys
from pathlib import Path

w = Path(sys.argv[1])


def load(label):
    s = json.loads((w / f"state-{label}.json").read_text(encoding="utf-8"))
    s.pop("label")
    return s


def comp(state):
    return next((i for i in state["items"] if i["typeName"] == "Composition" and i["name"] == "C014_COMP"), None)


results = {}


def check(name, ok):
    results[name] = bool(ok)


check("N1: project unchanged by the rejected load (00-empty == 01-after-N1)", load("00-empty") == load("01-after-N1"))
check("N2: refused revision left the project unchanged (05 == 06)", load("05-before-negatives") == load("06-after-N2"))
check("N3: failed revision rolled back completely (05 == 07)", load("05-before-negatives") == load("07-after-N3"))
check("P3: saving did not change project state (05 == 08)", load("05-before-negatives") == load("08-before-quit"))
before, after = load("08-before-quit"), load("09-after-relaunch")
check("P3: state after full quit + relaunch + reopen equals state before quit (08 == 09)", before == after)
c = comp(after)
artist = [l for l in (c or {}).get("layers", []) if l["name"] == "ARTIST_NOTE"]
check("P3: artist null and its note survived", len(artist) == 1 and artist[0]["comment"] == "artist note: keep me")
check("P3: artist comp marker survived", c is not None and "artist marker" in json.dumps(c["markers"]))
check("P3: managed BEAUTY layer still tagged", c is not None and any(l["comment"].startswith("CUTBRIDGE|1|layer|") for l in c["layers"]))
missing = [i["name"] for i in after["items"] if i["typeName"] == "Footage" and i.get("missing")]
check("P3: no missing footage after relaunch", not missing)
check("P3: comp range and FPS unchanged", c is not None and (c["fps"], c["duration"], c["width"], c["height"]) == (comp(before)["fps"], comp(before)["duration"], comp(before)["width"], comp(before)["height"]))
check("P3: state after QC in the relaunched panel equals state after relaunch (09 == 12)", after == load("12-after-qc"))

for label in ("08-before-quit", "09-after-relaunch"):
    print(label, hashlib.sha256(json.dumps(load(label), sort_keys=True).encode()).hexdigest())
for k, v in results.items():
    print(("PASS " if v else "FAIL ") + k)
(w / "comparison-rows.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
