#!/usr/bin/env bash
# Read only from the independently pinned orchestration checkout, not candidate.
# Wrap the existing CONTRIBUTING commands; never publish or change authorization.
set -euo pipefail
OUT="$PWD/verification-output"
if [[ "${1:-}" == --preflight ]]; then
python -I - <<'PY'
import os, socket
from pathlib import Path
assert not any(os.environ.get(k) for k in ('GH_TOKEN', 'GITHUB_TOKEN', 'SSH_AUTH_SOCK', 'ACTIONS_RUNTIME_TOKEN'))
assert not Path('/var/run/docker.sock').exists()
assert not Path('/candidate/.git').exists()
try:
    Path('/candidate/write-probe').write_text('unexpected')
except OSError:
    pass
else:
    raise SystemExit('candidate source mount is writable')
with socket.socket() as probe:
    probe.settimeout(1)
    try:
        probe.connect(('1.1.1.1', 443))
    except OSError:
        pass
    else:
        raise SystemExit('network accessible')
print('Isolation probes: read-only candidate, offline, no credential environment or socket')
PY
  exit 0
fi
[[ "${1:-}" == --checks ]] || exit 2
python -m compileall -q apps tools tests
python -m pytest -q -p no:cacheprovider --junitxml="$OUT/pytest.xml"
python tests/test_blender_runtime_52.py
for file in CutBridge.jsx revision_manager.js qc_plus.js localization.js; do
  node_file="$file"
  if [[ "$file" == CutBridge.jsx ]]; then node_file=CutBridge.js; fi
  cp "apps/after-effects/$file" "$TMPDIR/$node_file"
  node --check "$TMPDIR/$node_file"
done
for check in ae_s6_revision_checks ae_s6_optional_pass_lifecycle_checks ae_s6_extend_script_binding_checks ae_s7_qc_plus_checks ae_s7_native_qc_binding_checks ae_s8_localization_checks ae_s8_native_ui_binding_checks ae_s10c_reconstruction_checks ae_s13_revision_3d_tag_migration_checks; do
  node "tests/$check.cjs"
done
python tools/build_release.py --tag "v${CUTBRIDGE_VERSION}" --output "$OUT/dist-ci"
python tools/build_release.py --tag "v${CUTBRIDGE_VERSION}" --output "$OUT/dist-repeat"
(cd "$OUT/dist-ci" && tr -d '\r' < SHA256SUMS.txt | sha256sum --check)
# Complete repeated-output inventories/bytes are compared by trusted orchestration
# after the container and all candidate processes are removed.
python - <<'PY'
import importlib.util, json, shutil, tomllib, zipfile
from pathlib import Path
import jsonschema
out = Path('verification-output')
metadata = json.loads((out / 'dist-ci/release-metadata.json').read_text())
index = json.loads(Path('/verification-input/production-release-index.json').read_text())
before = list(index['releases'])
version = metadata['version']
base = 'https://unn0wn002.github.io/cutbridge-distribution'
artifact = metadata['artifacts']['blender']
filename = artifact['filename']
entry = {'version': version, 'channel': 'stable', 'blender_version_min': metadata['blender_version_min'], 'release_page_url': f'{base}/releases/v{version}/', 'download_url': f'{base}/releases/v{version}/{filename}', 'sha256': artifact['sha256']}
assert not any(item['version'] == version for item in before), 'candidate already advertised'
index['releases'] = [entry, *before]
index.pop('generated_at', None)
jsonschema.validate(index, json.loads(Path('packages/update/release-index.schema.json').read_text()))
spec = importlib.util.spec_from_file_location('updates', 'apps/blender/cutbridge/updates.py')
updates = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updates)
for current in ('0.2.3', version, '99.0.0'):
    selected = updates.select_latest_compatible(index, current_version=current, blender_version=(5, 2, 1), platform_name='windows-x64')
    assert (selected['version'] if selected else None) == (version if current == '0.2.3' else None)
assert index['releases'][1:] == before
preview = out / 'distribution-preview'
(preview / 'cutbridge').mkdir(parents=True)
(preview / 'blender').mkdir()
release = preview / 'releases' / f'v{version}'
release.mkdir(parents=True)
for source in (out / 'dist-ci').iterdir():
    shutil.copyfile(source, release / source.name)
(preview / 'cutbridge/release-index.json').write_text(json.dumps(index, indent=2) + '\n')
with zipfile.ZipFile(out / 'dist-ci' / filename) as package:
    manifest = tomllib.loads(package.read('blender_manifest.toml').decode())
manifest.pop('build', None)
manifest.update(archive_url='./' + filename, archive_size=(out / 'dist-ci' / filename).stat().st_size, archive_hash='sha256:' + artifact['sha256'])
(preview / 'blender/index.json').write_text(json.dumps({'version': 'v1', 'blocklist': [], 'data': [manifest]}, indent=2) + '\n')
shutil.copyfile(out / 'dist-ci' / filename, preview / 'blender' / filename)
links = ''.join(f'<li><a href="{item.name}">{item.name}</a></li>' for item in sorted(release.iterdir()))
(release / 'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><title>CutBridge v{version} candidate</title><h1>CutBridge v{version} candidate</h1><p>Unpublished preview. Owner authorization and published-download verification are required before distribution.</p><ul>{links}</ul></html>')
(preview / 'DO_NOT_PUBLISH.txt').write_text('Unpublished candidate artifacts. Verify the authorized published release before mirroring. Preserve production v0.2.3; never replace it with this partial preview.\n')
print('Distribution simulation passed: schema, retained entries, update selection/no downgrade; NOT PUBLISHED')
PY
