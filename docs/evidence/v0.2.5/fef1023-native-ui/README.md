# Valid bounded-output native Blender and visual evidence

Candidate: `fef102366a9e4b363455f8738b516d57a535ff76`. Exact Blender ZIP SHA-256: `3a53f7af8420909e5ed300440df115dffef2ba1dd196688c7c99789a8a48aa48`. Native host: **Blender 5.2.2 LTS**, inside offline Windows Sandbox.

**Native scoped verdict: PASS.** This fresh snapshot supersedes earlier native runs whose main-render output escaped to `C:\tmp`. Those original records are retained and explicitly marked INVALID. Here `scene.render.filepath` targets the designated `verification-output/tmp/` directory. Every observed saved render path is within approved output; source manifests before/after match. See `verification-closeout.json` for source-manifest identity, screenshot hashes, and exact scope. Blender exited normally with code 0.

Official extension CLI installation and enablement succeeded, isolated preferences persisted, and a fresh GUI process loaded the extension. Scripted native operators built V001/V002/V003, rendered 36 four-pass PNG/OpenEXR outputs, produced Camera/marked Empty metadata, preserved artist compositor state, blocked same-version replacement, and passed fault-injected mapping rollback. Startup update scheduling remained disabled.

Windows native UI automation opened the actual CutBridge tab and inspected English and Japanese layouts at the displayed sidebar width. `panel-en.jpg` and `panel-ja.jpg` show the same project/episode/scene/cut/take/version identities. The synthetic scene was saved inside approved output and closed normally. These are actual isolated-host screenshots, not generated mockups. Automation used the [Computer Use skill](C:/Users/unn0w/.codex/plugins/cache/openai-bundled/computer-use/26.930.31730/skills/computer-use/SKILL.md).

The raw scripted report still says visual inspection NOT_EXECUTED because that script did not perform it. The subsequent trusted visual observation and integrity audit are recorded separately in `verification-closeout.json`; raw reports are not rewritten to manufacture combined results.

Install-dialog inspection, direct Validate/Build button clicks, live update checks, native AE campaign, and Japanese representative-user validation remain unexecuted. This bounded native scope does not authorize publication or certify other hosts. Overall release readiness remains **INSUFFICIENT EVIDENCE**.

Only evidence, screenshots, and harness inputs are retained here. Generated ZIPs, runtime DLLs, blend projects, and image sequences are not committed.
