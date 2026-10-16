import pathlib,tomllib
print(tomllib.loads(pathlib.Path('apps/blender/cutbridge/blender_manifest.toml').read_text())['version'],end='')
