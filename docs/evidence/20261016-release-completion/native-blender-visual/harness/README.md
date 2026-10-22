# External visual inspection input

Prepared only; do not execute outside the policy-proven offline Windows Sandbox. No repository changes or VM launch are part of this preparation.

Use the same official extension-manager repo ID `cutbridge_candidate` and installed exact Blender ZIP as the successful native campaign. Preserve the installation and launcher logs. Read-only inputs are `C:\Review\candidate.json`, this script and the exact ZIP selected by `CUTBRIDGE_BLENDER_ZIP` (default `C:\Inputs\CutBridge-Blender-v0.2.5.zip`). Launch the real Blender GUI with `--python-exit-code 1 --python <readonly-path>\visual_blender.py`, without `--background` or preference-resetting `--factory-startup`.

Set `PYTHONPYCACHEPREFIX`, `TEMP`, `TMP`, `TMPDIR`, `BLENDER_USER_CONFIG`, `BLENDER_USER_DATAFILES` and `BLENDER_USER_EXTENSIONS` under `C:\Evidence\verification-output`. The disposable scene, reports, control file and screenshots stay under `C:\Evidence\verification-output\native-blender-visual`. No render, package build or update request is issued.

The script selects the real CutBridge sidebar using `Region.active_panel_category` after native categories have drawn, sets the actual `scene.cutbridge.language` property, and starts in EN. It writes `ready.json` and an actual native Blender screen capture after redraw. These files are **not visual acceptance** until the trusted observer inspects the screenshots. The documented category API is [Blender 5.2 Region](https://docs.blender.org/api/5.2/bpy.types.Region.html); [native area split and screenshot operators](https://docs.blender.org/api/5.2/bpy.ops.screen.html) provide optional narrow layout and captures.

For controlled phases, the trusted root writes a small JSON command to the output-side `phase.json`, with a strictly increasing integer `sequence` and one of these exact phase values:

```json
{"sequence":1,"phase":"JA"}
```

- `EN`, `JA`: switch the actual addon locale, select CutBridge and capture after redraw.
- `NARROW_EN`, `NARROW_JA`: switch locale and record actual current sidebar width; the observer can drag the native sidebar edge then send `CAPTURE`.
- `NARROW_API_EN`, `NARROW_API_JA`: optionally split the real VIEW_3D area to about 320 pixels and show its actual normal CutBridge sidebar. The report records actual dimensions and whether width is at most 320; inspect readability/clipping yourself. This is a native layout change, not an image transformation.
- `HELP_CAMERA_EN`, `HELP_CAMERA_JA`: optionally invoke the actual Camera help popup showing the narrowed reconstruction/QC wording. The observer may need Escape before the next phase.
- `CAPTURE`: record/capture current actual state without changing locale/layout.
- `QUIT`: request normal Blender exit after two seconds.

Wait for `READY_FOR_INDEPENDENT_INSPECTION` and the matching sequence in `ready.json` before inspecting that phase image. If category selection cannot be scripted, the report records the error; the observer may click the actual CutBridge tab and send `CAPTURE`. No category or narrow-width success is invented.

The default observation timeout is 180 seconds; the launcher may set `CUTBRIDGE_VISUAL_TIMEOUT_SECONDS` between 60 and 900. Timeout requests a normal quit and does not produce PASS. The launcher must record actual PID/exit, input manifests, policy/runtime isolation and screenshot hashes, then the observer separately records visible EN/JP/narrow/help scope and any glyph/clipping limitations. Installation dialogs, real Validate/Build button clicks, live manual update behavior, AE and S14B stay unexecuted here.
