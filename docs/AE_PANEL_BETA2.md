# CutBridge v0.2.3-beta.2 — After Effects Panel Guide

Status: **candidate documentation / not release authorization**.

The beta.2 AE panel is designed to answer four questions directly in the UI: **what does this do, when should I use it, what is recommended, and what are the limitations?** Opening the panel or opening contextual help does not build or mutate the AE project.

## Package and status

The top section shows the current package and a simple status state:

- **READY** — the last inspected action completed successfully for the shown scope.
- **WARNING** — user review or another setup step is required.
- **ERROR** — the last action failed or QC+ found a blocking problem.

The status is guidance, not a substitute for the detailed CutBridge error/QC message and support code.

## 1. Load Package

**What:** reads the Blender-generated `cutbridge.json` and makes that package current in CutBridge.

**Use it when:** starting a cut or switching to another CutBridge package.

**Recommended:** choose the exact `cutbridge.json` from the package you intend to composite.

**Limitation:** loading alone does not import footage, create a comp, or modify artist layers.

## 2. Build

**What:** creates or safely reuses CutBridge-managed folders, footage, layers, and the deterministic comp.

**Use it when:** a valid package is loaded and required render sequences are available.

**Recommended:** Build once, then composite normally while keeping artist-authored work separate from CutBridge-managed ownership.

**Limitation:** CutBridge fails closed on unsafe paths and ambiguous managed ownership rather than guessing.

## 3. QC+

**What:** inspects package identity, sequence completeness, managed ownership, and comp settings without rebuilding the project.

**Use it when:** after Build, before handoff/delivery, and after meaningful revisions.

**Recommended:** treat **ERROR** as blocking; inspect **WARNING**; preserve `CBQ-*` support codes when reporting a problem.

**Limitation:** QC+ reports problems but intentionally does not auto-repair ambiguous ownership or missing production content.

## 4. Revision

**What:** updates compatible CutBridge-managed sources and metadata from a newer package while preserving artist-owned work covered by the revision contract.

**Use it when:** moving through a normal `V001 -> V002 -> V003` Blender package revision.

**Recommended:** save the AE project first, select the newer package, review warnings, then confirm the expected revision.

**Limitation:** unsupported FPS, resolution, duration, pass-set, or ownership changes are blocked or require deliberate rebuild/migration.

## Current release boundary

The panel remains a dockable ScriptUI Panel/palette. This beta.2 repair improves hierarchy, descriptions, contextual help, and status feedback. Native-host verification on the exact frozen candidate is still required before expanding any compatibility or release claim.
