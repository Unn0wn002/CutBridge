import hashlib
import json
import pathlib
import stat
import sys
import zipfile

out = pathlib.Path(sys.argv[1])
version = sys.argv[2]
def inventory(root):
    records = {}
    for path in sorted(root.rglob('*')):
        mode = path.lstat().st_mode
        assert not path.is_symlink(), path
        if stat.S_ISDIR(mode):
            records[path.relative_to(root).as_posix()] = {'type': 'directory'}
        else:
            assert stat.S_ISREG(mode), path
            records[path.relative_to(root).as_posix()] = {'type': 'file', 'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    return records
first = inventory(out / 'dist-ci')
second = inventory(out / 'dist-repeat')
assert first == second, 'Repeated output inventories or bytes differ'
expected = {f'CutBridge-Blender-v{version}.zip', f'CutBridge-AfterEffects-v{version}.zip', 'SHA256SUMS.txt','release-metadata.json'}
assert set(first) == expected, first
for line in (out / 'dist-ci/SHA256SUMS.txt').read_text().splitlines():
    digest, filename = line.split('  ')
    assert filename in expected and first[filename]['sha256'] == digest
metadata = json.loads((out / 'dist-ci/release-metadata.json').read_text())
for entry in metadata['artifacts'].values():
    assert first[entry['filename']]['sha256'] == entry['sha256']
with zipfile.ZipFile(out / 'dist-ci' / f'CutBridge-AfterEffects-v{version}.zip') as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == {'CutBridge.jsx','revision_manager.js','qc_plus.js','localization.js','INSTALL.md','LICENSE'}
    install = archive.read('INSTALL.md').decode('utf-8')
    assert f'/blob/v{version}/docs/RELEASE_READINESS.md' in install
    assert 'RELEASE_TAG' not in install and 'development build' not in install.lower() and 'unpublished' not in install.lower()
with zipfile.ZipFile(out / 'dist-ci' / f'CutBridge-Blender-v{version}.zip') as archive:
    assert archive.testzip() is None
    assert 'blender_manifest.toml' in archive.namelist() and 'LICENSE' in archive.namelist()
(out / 'artifact-inspection.json').write_text(json.dumps({'repeated_complete_inventory_identical':True,'artifacts':first,'checksums_and_metadata':'PASS','ae_sidecars_guide_license':'PASS','zip_integrity':'PASS'},indent=2)+'\n')
print('Exact repeated inventory/bytes, hashes, archive integrity and AE installation guide checks passed')
