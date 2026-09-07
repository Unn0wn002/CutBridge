# CutBridge v0.2.3 — Test Plan

Run the complete automated commands in [CONTRIBUTING.md](CONTRIBUTING.md). Release safety coverage also checks repeatability, license inclusion, output preservation, artifact symlinks, source/output separation, and mismatched version constants.

## Blender tests

| ID | Test | Expected |
|---|---|---|
| B01 | Empty Cut ID | Validation error |
| B02 | No active camera | Validation error |
| B03 | Frame 1–12, 24 fps | Manifest count = 12, fps = 24 |
| B04 | Japanese metadata e.g. `テスト作品` | UTF-8 JSON is created correctly |
| B05 | BEAUTY+LINE only | Only two render pass folders + manifest entries |
| B06 | Build V001 then V002 | Two deterministic package folders |
| B07 | Register CutBridge 0.2.3 with official `bpy 5.2.1` | Extension registers without `StringProperty` or RNA registration errors |
| B08 | Disable and re-enable CutBridge in the same Blender session | No `already registered as a subclass` error |
| B09 | Simulate/encounter a failed registration, then retry enable | CutBridge cleans partial registrations and can retry without restarting Blender |
| B10 | Open Environment panel on Blender 5.2 | Reports CutBridge 0.2.3, Blender 5.2.x, platform, Python, and Target LTS status |
| B11 | Build a package with CutBridge 0.2.3 | Generated manifest version matches the canonical extension version |
| B12 | Missing camera, Cut ID, output, passes, or valid frame range | Validation reports the corresponding error and blocks package generation |
| B13 | BEAUTY; BEAUTY+LINE; all four passes | Folder tree and manifest entries match the selected passes exactly |
| B14 | Build a release artifact | Root manifest/modules, synchronized metadata, and recomputed SHA-256 values pass |
| B15 | Configure BEAUTY/LINE/SHADOW/DEPTH render outputs on supported Blender 5.2.1 setup | CutBridge-owned compositor outputs use deterministic package locations/patterns |
| B16 | Existing unrelated artist compositor nodes before CutBridge mapping | Artist-owned nodes remain untouched |
| B17 | Replacement render mapping fails after a prior valid mapping exists | Pending nodes/settings roll back and the previous valid CutBridge mapping is preserved |
| B18 | Same-version package contains rendered/user payload | Build is blocked with actionable version/package guidance; payload is preserved |
| B19 | Empty CutBridge scaffold exists for the same version | Safe refresh is allowed with the documented warning path |
| B20 | Build V001/V002/V003 with Japanese metadata and filesystem-invalid source characters | Version folders coexist, prior payload is preserved, and safe package tokens are deterministic |
| B21 | Negative export range | Validation and direct manifest production reject it with rebase-to-frame-0 guidance |

Automated Blender checks run headlessly. They validate RNA lifecycle, render-mapping state transitions, package generation/integrity, schema/producer contracts, and selected Blender API behavior. Blender GUI installation/panel behavior and After Effects GUI behavior remain separate manual test areas unless real evidence is recorded.

## After Effects tests

| ID | Test | Expected |
|---|---|---|
| A01 | Load a valid CutBridge manifest | Status shows package / FPS / frame count |
| A02 | Build comp from prepared image sequences | Resolution, FPS, and duration match manifest |
| A03 | Layer order | Layers follow `ae.layer_order` in manifest |
| A04 | Remove a required pass folder and run QC/import inspection | Required pass blocks import/build with actionable error |
| A05 | Change manifest FPS and build a new comp | Comp uses manifest FPS |
| A06 | Japanese path/package name | Manifest loads without encoding failure |
| A07 | Missing optional pass | Warning/skip; complete required passes remain usable |
| A08 | Missing expected middle frame | Missing frame number is diagnosed before complete-sequence import |
| A09 | Extra or wrong-padding matching filename | QC reports unexpected sequence filename without treating it as the expected frame |
| A10 | Unsupported `schema_version` | Manifest is rejected before import |
| A11 | Absolute/traversal/URI-escaped/unsafe pass path | Manifest or host adapter rejects path escape before footage import |
| A12 | Legacy ExtendScript runtime without native `JSON.parse` | Valid JSON data parses; executable/malformed text is rejected without `eval` |
| A13 | AE `PRODUCT_VERSION` differs from canonical release version | Release build fails before artifacts are written |
| A14 | Tagged managed comp moved out of `01_COMP` | Build fails before replacement creation; the moved comp remains untouched |
| A15 | Duplicate tagged managed comps | Build fails closed before footage/layer mutation |
| A16 | Managed comp metadata drift after script reload | QC rediscovers the tagged comp and reports the mismatch |
| A17 | Previously imported optional pass becomes unavailable | The stale optional layer is not treated as verified or reordered |
| A18 | Valid pass names matching object prototype keys | `constructor`, `toString`, and `__proto__` values are not false duplicates |
| A19 | Cached footage loses tag, name, source, and folder in one session | Build fails closed without importing a replacement or reclaiming the live artist item |
| A20 | Cached layer loses tag, name, source, and comp ownership evidence in one session | Build fails closed without adding a replacement layer or reordering the artist layer |
| A21 | Managed comp or required footage is deleted before QC, including after script reload | QC reports explicit missing managed state; package-only QC remains valid before any managed project state exists |
| A22 | Combined footage or layer drift is present after script reload | Build fails before replacement import/layer creation and preserves the existing object |
| A23 | Managed package root is moved while tagged managed objects remain | QC reports managed-state ownership failure instead of package-only PASS |
| A24 | A late build operation fails after new footage/layer creation | Newly created managed footage/layers roll back; existing comp scaffold and artist work remain |

## S4 automated contract gate

`node tests/ae_contract_checks.cjs` executes pure helpers and a mocked host adapter. `pytest -q tests/test_ae_contract.py` also checks Draft 2020-12 schema agreement. Missing Node is a failure, never a silent skip. CI installs Node explicitly.

Coverage includes host/third-realm arrays; schema/version fields; positive/zero/single-frame ranges; rejection of negative, fractional, non-finite, reversed and wrong-count ranges; strict FPS/resolution; traversal/absolute/URI/malformed paths; Unicode filenames; exact missing/extra frame detection; required/optional pass behavior; alias rejection; legacy data-only JSON parsing; and canonical AE product version.

Official `bpy 5.2.1` integration tests observe Blender's signed frame filename (`-0001`), verify actionable negative-export rejection, and feed real generated zero/positive manifests plus Blender-formatted names to the AE contract. No render or AE GUI success is inferred from those tests.

Release validation rejects AE version drift before writing artifacts. Release simulation checks ZIP contents, reproducibility and SHA-256 sums.

## Manual application tests

These remain `MANUAL NOT EXECUTED` until real evidence is recorded.

| Case | Expected |
|---|---|
| Install/enable current Blender extension in supported GUI build | Add-on/extension enables and CutBridge panel is usable |
| Validate and Build Package in Blender GUI | Actionable diagnostics match automated contract and package is created safely |
| Render configured pass sequences | Expected files are produced for the selected renderer/View Layer setup |
| Load a real package in After Effects | Manifest loads without host/runtime error |
| Build AE comp | Resolution/FPS/duration/folders/layers agree with manifest |
| Export range begins at 0 | Blender package and AE import/comp/QC agree |
| Negative export range | Actionable rejection; animation is not changed |
| Required middle frame absent | Import blocked with missing frame number |
| Optional folder/frame absent | Warning and skip; other complete passes import |
| Extra matching file | Build/QC warning names the affected pass |
| Japanese package/pass/sequence paths | Correct file resolution and import |
| Folder/file symlink or alias | Rejected before footage import |
| Older ExtendScript without native JSON | Valid JSON loads; executable text is rejected |
| Repeat package import | First build, repeated build, manifest reload and script reload retain singleton managed items/layers; tag/container drift blocks without adoption or duplication |
| V001 → V002 revision | Preservation behavior is tested only after S6 is implemented |

## Target-user task test

After the product reaches the appropriate validation stage, measure with representative users:

1. Manual setup time for one cut in AE.
2. CutBridge setup time.
3. Number/type of handoff errors.
4. Whether the tester understood diagnostics without developer intervention.
5. Which automation was useful versus intrusive.
6. Revision/rework impact when V002 replaces V001.

Do not claim timing, error-rate, usability, or Japanese target-user results until the test was actually run.

## S5 ownership/cache automated gate

`node tests/ae_s5_checks.cjs` executes the entire JSX panel with host mocks and re-evaluates it against the same project to simulate script reload. It runs through `tests/test_ae_s5.py` in CI. The source-guard, comp/layer rollback, and partial-retry-order regressions remain mandatory. The current harness contains 45 groups.

| Change after successful Build | Expected same-session and script-reload result |
|---|---|
| Footage tag removed/changed/unreadable | Block ambiguous ownership; do not re-tag or import a duplicate |
| Footage moved from managed render folder | Block folder ownership drift; preserve moved object |
| Layer tag removed/changed/unreadable | Block ambiguous ownership; do not add a duplicate |
| Tagged layer moved to another comp | Block expected-comp mismatch; preserve both comps |
| Cached item/layer has wrong host type/container | Reject live ownership; never report safe reuse |
| Duplicate persistent footage/layer tag | Block ambiguous ownership |
| Moved or duplicate managed comp tag | Block before creating or mutating a replacement comp |
| Cached reference removed; valid live replacement and matching layer source exist | Rediscover and validate live replacement; no import/layer duplication |
| Artist footage/layers with unrelated names/sources | Preserve contents and artist relative order |
| Comp metadata drift after script reload | Rediscover the managed comp and report the mismatch |
| Optional pass folder disappears after a prior import | Warn/skip the optional pass without reordering its stale layer |
| Pass names using inherited object keys | Accept valid names without false duplicate errors |
| QC following footage ownership/source/FPS failure | Report managed-footage error even after cache invalidation or reload |
| Cached footage or layer loses all identifying signals while the object remains live | Fail closed without importing footage or adding a layer over the live user-modified object |
| Managed comp or required managed footage is deleted before QC | Report explicit missing managed state rather than a false package-only PASS |
| Combined footage/layer drift remains after script reload | Preflight the existing managed comp/layer state before importing or adding replacements |
| Managed package root is moved but tagged managed comp remains | Report managed-comp validation failure; do not issue package-only PASS |
| Late build failure after new managed objects are created | Roll back only the newly created footage/layers and preserve unrelated project state |

Manual repetition in a supported AE desktop installation remains `MANUAL NOT EXECUTED`. Mocks cannot certify native host handles, comment persistence, undo behavior or OS filesystem semantics.
