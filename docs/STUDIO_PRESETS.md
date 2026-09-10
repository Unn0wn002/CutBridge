# CutBridge Studio Presets

Studio Presets let CutBridge adapt deterministic Blender → After Effects handoff conventions without hard-coding one studio workflow into the product.

S9 presets are **declarative JSON data only**. They do not execute code, run commands, expand environment variables, access the network, or grant ownership over existing After Effects project items.

## Preset modes

The Blender N-panel exposes three modes:

- **Manual** — preserves the pre-S9 CutBridge behavior. Blender pass toggles and Sequence Format remain directly editable. Package naming remains `{project}_{episode}_{scene}_{cut}_{take}_V###`.
- **CutBridge Default** — uses the built-in safe preset. It intentionally reproduces the default CutBridge conventions while proving the preset pipeline.
- **Custom JSON** — loads one user-selected UTF-8 JSON preset after strict validation.

Manual remains the default mode so existing scenes and workflows do not silently change behavior after upgrading.

## Trust boundary

A custom preset is treated as untrusted input.

CutBridge validates the full document before it can influence package generation. Validation is fail-closed:

- root must be a JSON object;
- `schema` must be `cutbridge-studio-preset`;
- `schema_version` must currently be `1`;
- unknown fields are rejected;
- the file is limited to 64 KiB;
- the file must decode as UTF-8 JSON;
- folder values must be safe relative forward-slash paths;
- `..`, absolute paths, backslashes, empty segments, and overlapping/nested role folders are rejected;
- naming templates accept only documented placeholders;
- template format specifications, conversions, path separators, and control characters are rejected;
- only known CutBridge passes and sequence formats are accepted;
- duplicate passes are rejected;
- pass `required` values must be booleans;
- version prefix/padding is bounded.

Build Package freezes the validated custom preset into an in-memory snapshot for that build. If the source JSON file changes while the build is running, package naming, compositor mapping, directory creation, and `cutbridge.json` still use the same validated snapshot.

## Schema and example

Authoritative schema:

`packages/shared/cutbridge-studio-preset.schema.json`

Safe example:

`docs/examples/studio-preset.default.json`

Example:

```json
{
  "schema": "cutbridge-studio-preset",
  "schema_version": 1,
  "id": "cutbridge-default",
  "name": "CutBridge Default",
  "naming": {
    "package": "{project}_{episode}_{scene}_{cut}_{take}_{version}",
    "sequence": "{cut}_{pass}_####",
    "ae_comp": "{cut}_COMP"
  },
  "folders": {
    "render": "render",
    "preview": "preview",
    "camera": "camera"
  },
  "passes": [
    {
      "name": "BEAUTY",
      "required": true
    }
  ],
  "output": {
    "image_format": "PNG"
  },
  "versioning": {
    "prefix": "V",
    "padding": 3
  }
}
```

## Naming placeholders

The following placeholders are supported:

- `{project}`
- `{episode}`
- `{scene}`
- `{cut}`
- `{take}`
- `{version}`
- `{pass}`

`naming.sequence` must contain `{pass}` and the literal `####` frame token.

Templates describe a filename/name component, not an arbitrary path. `/` and `\` are therefore rejected in naming templates. Folder structure belongs under `folders`.

## Folder roles

Preset folder roles are:

- `folders.render` — parent directory for pass sequence folders;
- `folders.preview` — preview/review payload directory;
- `folders.camera` — camera handoff directory.

Each value may contain multiple safe relative segments such as `frames/final` or `handoff/camera`.

The three role trees must be disjoint. For example, this is rejected because the preview folder is nested inside the render tree:

```json
{
  "render": "media",
  "preview": "media/review",
  "camera": "camera"
}
```

## Pass definitions and order

Supported logical passes remain:

- `BEAUTY`
- `LINE`
- `SHADOW`
- `DEPTH`

The preset `passes` array is ordered. That order becomes the normalized manifest pass order and After Effects `layer_order` contract.

Each pass also carries `required: true|false`. After Effects continues to use the manifest's established required/optional semantics; it does **not** load the Studio Preset file itself.

Example:

```json
"passes": [
  {"name": "LINE", "required": false},
  {"name": "BEAUTY", "required": true}
]
```

A preset can request only a pass that the current Blender renderer/View Layer can actually expose. Existing CutBridge render-capability validation remains authoritative.

## Sequence format

Supported values:

- `PNG`
- `OPEN_EXR`
- `TIFF`

Existing DEPTH guidance remains: use OpenEXR when floating-point depth precision must be preserved.

## Version token

`versioning` controls the display token used by preset-managed names and `version_label`.

Example:

```json
"versioning": {
  "prefix": "R",
  "padding": 4
}
```

Version `12` becomes `R0012`.

The numeric manifest `version` remains an integer and continues to drive revision compatibility. A custom display token does not change revision ordering semantics.

## After Effects boundary

After Effects does not open, parse, or trust the Studio Preset JSON file.

Blender resolves the preset into the existing handoff manifest contract:

- `package_name`;
- `version_label`;
- `passes[].path`;
- `passes[].sequence_pattern`;
- `passes[].required`;
- `folders`;
- `ae.comp_name`;
- `ae.layer_order`.

The manifest also records normalized preset provenance:

```json
"studio_preset": {
  "mode": "custom",
  "schema": "cutbridge-studio-preset",
  "schema_version": 1,
  "id": "jp-studio-a",
  "name": "JP Studio A"
}
```

The source preset path is deliberately **not** stored in `cutbridge.json`.

Existing manifests remain valid because `studio_preset` is optional in the CutBridge manifest schema.

## Stable validation codes

Preset-specific machine-facing codes remain English/stable across Japanese and English UI:

- `PRESET_PATH_MISSING`
- `PRESET_FILE_UNAVAILABLE`
- `PRESET_FILE_TOO_LARGE`
- `PRESET_JSON_INVALID`
- `PRESET_SCHEMA_INVALID`
- `PRESET_SCHEMA_UNSUPPORTED`
- `PRESET_FIELD_INVALID`
- `PRESET_PATH_UNSAFE`

Interactive explanations are localized, but these codes are not translated.

## Recommended authoring workflow

1. Copy `docs/examples/studio-preset.default.json` outside the installed extension package.
2. Give the preset a unique non-confidential `id` and readable `name`.
3. Change only the documented data fields.
4. In Blender, select **Custom JSON** and choose the file.
5. Run **Validate Cut**.
6. Resolve every preset/render/package error before Build Package.
7. Build a package and inspect `cutbridge.json` before adopting the preset in production.

Do not bundle a confidential real-studio convention in public/customer distributions without explicit permission. Prefer generic or customer-owned preset files.