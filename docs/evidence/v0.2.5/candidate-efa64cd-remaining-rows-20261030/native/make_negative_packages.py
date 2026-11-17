"""Make the N1-N3 negative packages from the exported V001/V002 (scratch script, copied into the evidence folder).

Each variant lives under its own parent folder so the package folder keeps its expected name.
  N1: V001 with the "fps" field removed from cutbridge.json        -> import must be rejected
  N2: V002 with fps changed from 24 to 30                          -> revision must be refused
  N3: V002 with required BEAUTY frame 2 deleted                    -> revision must fail and roll back
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

work = Path(sys.argv[1])
src = work / "cutbridge_exports"
v1, v2 = "QAPROJ_EP01_SC010_C014_T01_V001", "QAPROJ_EP01_SC010_C014_T01_V002"
lines = []


def clone(name, variant):
    dst = work / f"negative_{variant}" / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src / name, dst)
    return dst


def rewrite(manifest_path, change):
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    change(data)
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


n1 = clone(v1, "n1")
rewrite(n1 / "cutbridge.json", lambda d: d.pop("fps"))
n2 = clone(v2, "n2")
rewrite(n2 / "cutbridge.json", lambda d: d.__setitem__("fps", 30))
n3 = clone(v2, "n3")
removed = n3 / "render" / "beauty" / "C014_BEAUTY_0002.png"
removed.unlink()

for label, path in (("N1 manifest", n1 / "cutbridge.json"), ("N2 manifest", n2 / "cutbridge.json"), ("N3 manifest", n3 / "cutbridge.json")):
    lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {label}  {path.relative_to(work).as_posix()}")
lines.append(f"N3 removed: {removed.relative_to(work).as_posix()} (exists after: {removed.exists()})")
(work / "negative-packages.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
