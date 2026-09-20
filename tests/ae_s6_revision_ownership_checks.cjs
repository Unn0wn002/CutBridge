/* Revision-entry ownership regressions against the actual JSX in a host-shaped VM.
 * These tests do not execute Adobe After Effects desktop. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');

const fixturePath = path.resolve(__dirname, 'ae_s6_native_host_checks.cjs');
const fixture = new Module(fixturePath, module);
fixture.filename = fixturePath;
fixture.paths = Module._nodeModulePaths(path.dirname(fixturePath));
fixture._compile(fs.readFileSync(fixturePath, 'utf8') +
    '\nmodule.exports = {makeHost, manifest, Contract};\n', fixturePath);
const {makeHost, manifest, Contract} = fixture.exports;

const failures = [];
for (const defect of ['stale orphan layer', 'duplicate footage', 'live comp drift']) {
    const h = makeHost(), v1 = manifest(1), v2 = manifest(2), v3 = manifest(3);
    h.queue(v1); h.click('Import Package'); h.click('Build Comp');
    h.queue(v2); h.click('Update Revision');
    const comp = h.comps()[0], layer = comp.layer(1), source = layer.source;
    const root = h.topRoot(v2.package_name);
    let restore;
    if (defect === 'stale orphan layer') {
        const orphan = comp.layers.add(h.footage()[0]);
        orphan.name = 'ARCHIVE';
        orphan.comment = Contract.managedTag('layer', v1, 'BEAUTY');
        // Removing only its ownership claim makes this an ordinary artist layer.
        restore = () => { orphan.comment = ''; };
    } else if (defect === 'duplicate footage') {
        const duplicate = new source.constructor(source.file);
        duplicate.name = 'DUPLICATE';
        duplicate.parentFolder = source.parentFolder;
        duplicate.mainSource.conformFrameRate = v2.fps;
        duplicate.comment = source.comment;
        h.projectItems.push(duplicate);
        restore = () => duplicate.remove();
    } else {
        comp.width = 1280;
        restore = () => { comp.width = v2.resolution.width; };
    }
    h.reload(); h.queue(v2); h.click('Import Package');
    const before = {confirms: h.confirms.length, footage: h.footage().length,
        swaps: h.replaceFlags.length, layers: comp.numLayers,
        rootName: root.name, compTag: comp.comment, layerTag: layer.comment,
        footageTag: source.comment};
    h.queue(v3); h.click('Update Revision');
    try {
        assert.equal(h.confirms.length, before.confirms, defect + ': must block before confirmation');
        assert.equal(h.footage().length, before.footage, defect + ': must not import');
        assert.equal(h.replaceFlags.length, before.swaps, defect + ': must not swap');
        assert.equal(comp.numLayers, before.layers);
        assert.strictEqual(layer.source, source);
        assert.equal(root.name, before.rootName);
        assert.equal(comp.comment, before.compTag);
        assert.equal(layer.comment, before.layerTag);
        assert.equal(source.comment, before.footageTag);
        assert.match(h.alerts.at(-1), /ownership|stale|metadata|drift/i);
        restore();
        h.queue(v3); h.click('Update Revision');
        assert.match(h.alerts.at(-1), /revision updated to V003/);
        h.reload(); h.queue(v3); h.click('Import Package');
        h.click('Build Comp'); h.click('Run QC');
        assert.match(h.alerts.at(-1), /CutBridge QC — PASS/);
        assert.equal(h.footage()[0].comment, Contract.managedTag('footage', v1, 'BEAUTY'));
        assert.equal(source.comment, before.footageTag, 'historical footage provenance remains');
        console.log('PASS revision preflight: ' + defect);
    } catch (error) { failures.push(error.message); }
}
assert.deepEqual(failures, [], 'Revision must reject existing ownership/comp drift');
console.log('S6 revision ownership: PASS (real AE MANUAL NOT EXECUTED)');
