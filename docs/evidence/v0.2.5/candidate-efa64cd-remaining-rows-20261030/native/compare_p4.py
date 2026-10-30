"""Check the P4 revision chain dumps (scratch script, copied into the evidence folder)."""
import json
import sys
from pathlib import Path

w = Path(sys.argv[1])


def comp(label):
    s = json.loads((w / f"state-{label}.json").read_text(encoding="utf-8"))
    return next(i for i in s["items"] if i["typeName"] == "Composition" and i["name"] == "C014_COMP")


results = {}
before = comp("22-before-revisions")
for label, version in (("23-after-V002", "V002"), ("25-after-V003", "V003")):
    c = comp(label)
    managed = [l for l in c["layers"] if l["comment"].startswith("CUTBRIDGE|1|")]
    artist = [l for l in c["layers"] if l["name"] == "ARTIST_NOTE"]
    results[f"P4 {version}: every managed layer retagged to {version}"] = bool(managed) and all(f"_{version}|" in l["comment"] for l in managed)
    results[f"P4 {version}: same layer count, names and order as before revisions"] = [l["name"] for l in c["layers"]] == [l["name"] for l in before["layers"]]
    results[f"P4 {version}: artist null and note unchanged"] = len(artist) == 1 and artist[0]["comment"] == "artist note: keep me" and artist[0]["position"] == [l for l in before["layers"] if l["name"] == "ARTIST_NOTE"][0]["position"]
    results[f"P4 {version}: artist comp marker unchanged"] = c["markers"] == before["markers"]
for k, v in results.items():
    print(("PASS " if v else "FAIL ") + k)
(w / "comparison-p4.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
