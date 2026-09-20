const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const source = fs.readFileSync(require.resolve("../apps/after-effects/revision_manager.js"), "utf8");

function manifest(version, extraPass = false) {
    const value = {
        schema: "cutbridge-manifest",
        schema_version: 1,
        cutbridge_version: "0.2.3",
        project: "PROJECT_A",
        episode: "EP01",
        scene: "SC010",
        cut: "C012",
        take: "T01",
        version,
        package_name: `PROJECT_A_EP01_SC010_C012_T01_V${String(version).padStart(3, "0")}`,
        fps: 24,
        frames: {start: 0, end: 23, count: 24},
        resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        passes: [
            {name: "BEAUTY", path: "render/beauty", sequence_pattern: "C012_BEAUTY_####.png", required: true}
        ],
        ae: {comp_name: "C012_COMP", layer_order: ["BEAUTY"]}
    };
    if (extraPass) {
        value.passes.push({name: "DEPTH", path: "render/depth", sequence_pattern: "C012_DEPTH_####.png", required: true});
        value.ae.layer_order.push("DEPTH");
    }
    return value;
}

// Generic browser-style loading without either the shared contract or an AE host
// must remain fail-closed.
assert.throws(() => vm.runInNewContext(source, {}), /Load CutBridgeContract/);

// Real After Effects exposes $.global. In that host shape the revision manager
// must initialize even though CutBridgeContract is scoped inside CutBridge.jsx.
const ae = {};
ae.$ = {global: ae};
vm.runInNewContext(source, ae);
assert.ok(ae.CutBridgeRevisionManager, "AE-like host did not bind CutBridgeRevisionManager");

const manager = ae.CutBridgeRevisionManager;
assert.equal(manager.assess(manifest(3), manifest(4)).status, "safe");
const added = manager.assess(manifest(3), manifest(4, true));
assert.equal(added.status, "incompatible");
assert.match(added.reasons.join("; "), /Adding passes is unsupported by source-only revision: DEPTH/);

console.log("S6 ExtendScript binding/pass-set guard: PASS");
