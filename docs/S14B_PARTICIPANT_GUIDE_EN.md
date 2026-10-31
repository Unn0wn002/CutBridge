# CutBridge user test: participant guide (v0.2.5 development build, asynchronous)

This guide is for English-speaking testers. Your session is a practice run and general feedback on the English UI. It is **not** part of the Japanese user study (S14B). You work **on your own computer, at your own pace**; there is no meeting or call.

It assumes you have read the [information and consent form](S14B_CONSENT_FORM_EN.md) and sent your consent reply.

## Before you start

- We are testing **CutBridge**, not **you**. Places where you get stuck are the most useful results.
- Each task gives only the goal; finding out how is part of the test.
- **Questions are welcome by email (【contact】).** For trouble receiving the files or with the hash check, just ask. Questions about installing or using CutBridge are answered if you're stuck, but are recorded as help (that's fine).
- If you can't finish a task, that's fine. Write on the record sheet where and why you got stuck, then move on.
- Expect about 90–120 minutes. You can take breaks or split it over several sittings.
- **Use only the test material.** Don't open your own work files.
- CutBridge's display language is set in each CutBridge panel. In After Effects the choice is remembered. In Blender it is saved inside each .blend file, so every test file you open (including the JP03 and JP04 files) may start in Japanese again; switch it to English each time. Finding that setting is part of JP01 and JP06.

## Setup

### The files you received

| File | Used in |
| --- | --- |
| `CutBridge-Blender-v0.2.5.zip` | JP01 (for Blender) |
| `CutBridge-AfterEffects-v0.2.5.zip` | JP06 (for After Effects) |
| `S14B_FX01_start.blend`, `studio_preset_s14b_fx01.json` | JP03–JP05 |
| `S14B_FX01_JP04.blend` | JP04 (keep it in the same folder as the preset file) |
| `JP08_qc_check` folder | JP08 |
| `revisions` folder | JP09 and JP10 |
| `fallback` folder | only if your own V001 can't be used (see JP06 and JP09) |
| `S14B_PARTICIPANT_RECORD_EN.md` (record sheet) | every task |

### If you chose to record

- Start a screen recording before JP01. You can stop it during breaks; several files are fine.
- Record the **whole screen**: you'll move between Blender, After Effects and folders.
  - Windows: Snipping Tool's screen recording (choose Record, then select the whole screen), or OBS Studio. Don't use Xbox Game Bar: it records only one app.
  - macOS: `Shift + Command + 5`, then "Record Entire Screen". If you chose voice, pick a microphone under Options.
- If you chose screen and voice, think aloud as you go ("what does this button do?", "I expected this to save").
- Keep your name, email, notifications and other windows out of the recording.
- Optionally, write the recording time at which you started each task on the record sheet.

### 0. Check the files (hashes)

Check that the two ZIPs are the right ones.

First, extract the archive you received (`S14B-FX02-data-20261031.zip`) to any folder. Don't extract the two CutBridge ZIPs inside it yet. Then open a command window in that folder:

- Windows: open the folder in File Explorer, type `powershell` in the address bar and press Enter.
- macOS: open Terminal, type `cd ` (with a space after it), drag the folder onto the Terminal window and press Enter.

Then run:

- Windows (PowerShell):

  ```text
  Get-FileHash -Algorithm SHA256 CutBridge-Blender-v0.2.5.zip, CutBridge-AfterEffects-v0.2.5.zip
  ```

- macOS (Terminal):

  ```text
  shasum -a 256 CutBridge-Blender-v0.2.5.zip CutBridge-AfterEffects-v0.2.5.zip
  ```

Compare the output with these values and write the result on the record sheet (upper or lower case doesn't matter):

- `CutBridge-Blender-v0.2.5.zip`: `abf5882d56856d4662e95b2ac1335fb0dc6e818f5f7113235dce0529385b2207`
- `CutBridge-AfterEffects-v0.2.5.zip`: `ecfb26ce8e5ad50638e17b35104efc2210d222b4ac8f10fccf0fba2748c17d8f`

**If they don't match, stop here** and tell 【contact】.

## Task brief

Use these values in JP03. The start file deliberately does **not** match them; check and set each one.

| Item | Value |
| --- | --- |
| Project / Episode / Scene / Cut / Take | `S14B` / `EP01` / `SC001` / `C001` / `T01` |
| Version | `1` (the first package) |
| Active camera | `CAM_MAIN` |
| FPS | 24 |
| Resolution | 960 × 540 (100%) |
| Frame range | 1 to 12 |
| Output folder | an empty folder you create |
| Preset | Custom, using `studio_preset_s14b_fx01.json` |

The preset contains two passes: `BEAUTY` (required) and `LINE` (optional).

**Artist work for JP07:** after building the comp in After Effects, add your own work:

1. one new layer (a solid, a null, anything);
2. an effect on any layer;
3. a mask on any layer;
4. a changed opacity on any layer;
5. a parent link between two layers.

JP09 and JP10 check whether this work survives the updates.

## Tasks

After each task, write the result, what you did, and what confused you on the record sheet. Note any term or message you didn't understand or could misread.

### JP01 — Install CutBridge in Blender

Install and enable CutBridge from `CutBridge-Blender-v0.2.5.zip`, and open the CutBridge panel.

### JP02 — Understand the panel

Looking at the CutBridge panel, write in your own words what each of these is for:

- the Project / Episode / Scene / Cut / Take / Version fields;
- the button that validates the cut, and the button that builds the package;
- the Studio Preset mode;
- the safety messages and status shown.

### JP03 — Set up the cut

Open `S14B_FX01_start.blend` and set the metadata, active camera, FPS, resolution, frame range, output folder and preset as the task brief says. Then **save the file under a new name**; you'll need it in JP05.

### JP04 — Recover from an error

Open `S14B_FX01_JP04.blend`. It has one problem put in on purpose. Validate the cut, work out from the message what is wrong, fix it, and validate again until it passes. You can close the file without saving afterwards.

### JP05 — Build the package

Open the file you saved in JP03, and with validation passing, build the package. Then render the animation for the whole frame range (1 to 12); the package is not complete until it is rendered. On the record sheet, write which folder was created, the package version, and what you think would happen if you built the same version again.

### JP06 — Open the package in After Effects

Make the CutBridge panel available from `CutBridge-AfterEffects-v0.2.5.zip`, and load the package you built in JP05 (`cutbridge.json`).

Only if your own package really can't be loaded, continue with the package in the `fallback` folder. **If you use it, write that on the record sheet.**

### JP07 — Build the After Effects comp

Build the comp from the loaded package. Then add the artist work from the task brief, and write how you tell CutBridge's layers apart from your own. Save the project.

### JP08 — Read the QC+ results

1. Run QC+ on your JP07 project and write down the result.
2. Then create a **new project** in After Effects, load and build the package in the `JP08_qc_check` folder, and run QC+. This package has one problem put in on purpose. Write what is wrong and what should be done about it.
3. Close the new project without saving and go back to your JP07 project.

### JP09 — Update to V002

Update your JP07 project with the V002 package in the `revisions` folder. Write what the confirmation message means and which version you have after the update.

If your own V001 can't be updated, write what you saw under JP09 on the record sheet. Then create a **new project** in After Effects, redo JP06 (load) and JP07 (build, artist work, save) with the `fallback` V001, and continue with JP09 (no need to redo JP08). **Write on the record sheet under JP09 that you used `fallback`.**

### JP10 — Update to V003 and check your work is still there

Next, update to V003 from the `revisions` folder. Check that the version is now V003, and whether your artist work (effect, mask, opacity, your own layer, parenting) is still there. Write it down.

### JP11 — Save, close and reopen

Save the project, quit After Effects completely and start it again. Open the project and reopen the CutBridge panel. Check the package state (such as the version), run QC+ again, and write down the result.

JP12 (camera and 3D null handoff) is skipped: in v0.2.5 it can't be turned on from the normal UI.

## Final questions

Answer the "Final questions" on the record sheet in writing.

## When you're done

1. Stop the recording. If you recorded, check that nothing private is visible before sending. You may still decide not to send it.
2. Send the record sheet (and the recording) via 【return method】. If you agreed to attach screenshots, list their file names and which task each shows under "Anything else" on the record sheet.
3. **Remove CutBridge**
   - Blender: open **Edit → Preferences → Add-ons**, find CutBridge, open its menu (▾) and choose **Uninstall**.
   - After Effects: delete the four files (`CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, `localization.js`) wherever you put them. If you copied them into After Effects' `Scripts/ScriptUI Panels` folder, delete them from there (only these four files, not the folder). One harmless display-language setting stays in After Effects' preferences.
   - You can also delete the packages, the After Effects project and the files you received.

Thank you for your help.

---

Contact: 【contact】
