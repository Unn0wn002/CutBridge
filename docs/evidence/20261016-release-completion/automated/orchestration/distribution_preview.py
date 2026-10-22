import importlib.util
import json
import pathlib
import shutil
import tomllib
import zipfile

import jsonschema

out = pathlib.Path('C:/Evidence/verification-output')
metadata = json.loads((out / 'dist-ci/release-metadata.json').read_text())
index = json.loads(pathlib.Path('C:/Review/production-release-index.json').read_text())
before = list(index['releases'])
version = metadata['version']
base = 'https://unn0wn002.github.io/cutbridge-distribution'
artifact = metadata['artifacts']['blender']
filename = artifact['filename']
entry = {'version':version,'channel':'stable','blender_version_min':metadata['blender_version_min'],'release_page_url':f'{base}/releases/v{version}/','download_url':f'{base}/releases/v{version}/{filename}','sha256':artifact['sha256']}
assert not any(item['version'] == version for item in before)
index['releases'] = [entry, *before]
index.pop('generated_at',None)
jsonschema.validate(index,json.loads(pathlib.Path('packages/update/release-index.schema.json').read_text()))
spec = importlib.util.spec_from_file_location('candidate_updates','apps/blender/cutbridge/updates.py')
updates = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updates)
for current in ('0.2.3',version,'99.0.0'):
    selected=updates.select_latest_compatible(index,current_version=current,blender_version=(5,2,1),platform_name='windows-x64')
    assert (selected['version'] if selected else None) == (version if current == '0.2.3' else None)
assert index['releases'][1:] == before
preview=out/'distribution-preview'
(preview/'cutbridge').mkdir(parents=True)
(preview/'blender').mkdir()
release=preview/'releases'/f'v{version}'
release.mkdir(parents=True)
for source in (out/'dist-ci').iterdir():
    shutil.copyfile(source,release/source.name)
(preview/'cutbridge/release-index.json').write_text(json.dumps(index,indent=2)+'\n')
with zipfile.ZipFile(out/'dist-ci'/filename) as package:
    manifest=tomllib.loads(package.read('blender_manifest.toml').decode())
manifest.pop('build',None)
manifest.update(archive_url='./'+filename,archive_size=(out/'dist-ci'/filename).stat().st_size,archive_hash='sha256:'+artifact['sha256'])
(preview/'blender/index.json').write_text(json.dumps({'version':'v1','blocklist':[],'data':[manifest]},indent=2)+'\n')
shutil.copyfile(out/'dist-ci'/filename,preview/'blender'/filename)
(preview/'DO_NOT_PUBLISH.txt').write_text('Unpublished partial candidate preview. Preserve production v0.2.3; authorized publication, independent published-download verification and official Blender index generation are required before distribution.\n')
(out/'distribution-preview-result.json').write_text(json.dumps({'candidate_version':version,'schema':'PASS','retained_previous_entries':'PASS','v023_update_selection':'PASS','no_downgrade':'PASS','official_blender_generator_comparison':'NOT_EXECUTED','publication':'NOT_EXECUTED'},indent=2)+'\n')
print('Offline preview schema, preserved prior entries, update selection and no downgrade passed; NOT PUBLISHED')
