const assert = require('node:assert/strict');
const path = require('node:path');

const QC = require(path.resolve(__dirname, '../apps/after-effects/qc_plus.js'));

function codes(records) {
  return records.map(r => r.code);
}

{
  const report = QC.render([
    {severity: 'PASS', code: 'CBQ-SEQ-COMPLETE', scope: 'sequence', subject: 'BEAUTY', message: 'Frames complete.'},
    {severity: 'ERROR', code: 'CBQ-COMP-DRIFT-FRAME-RATE', scope: 'comp', message: 'Frame rate differs.', remediation: 'Restore intended frame rate.'},
    {severity: 'WARNING', code: 'CBQ-SEQ-UNEXPECTED-MATCHES', scope: 'sequence', subject: 'BEAUTY', message: 'Unexpected files.', remediation: 'Review matching files.'}
  ]);
  assert.equal(report.headline, 'ERROR — 1 error(s), 1 warning(s)');
  assert.deepEqual(codes(report.records), [
    'CBQ-COMP-DRIFT-FRAME-RATE',
    'CBQ-SEQ-UNEXPECTED-MATCHES',
    'CBQ-SEQ-COMPLETE'
  ]);
  assert.match(report.text, /Next: Restore intended frame rate\./);
  assert.match(report.text, /Next: Review matching files\./);
}

{
  assert.throws(() => QC.diagnostic({
    severity: 'WARNING', code: 'CBQ-TEST-WARN', scope: 'manifest', message: 'warning without next step'
  }), /requires actionable remediation/);
  assert.throws(() => QC.diagnostic({
    severity: 'ERROR', code: 'NOT-STABLE', scope: 'manifest', message: 'bad', remediation: 'fix'
  }), /stable CBQ/);
}

{
  const required = QC.sequenceRecords(
    {name: 'BEAUTY', required: true},
    {frames: {count: 3}},
    {folderExists: false}
  );
  assert.equal(required.length, 1);
  assert.equal(required[0].severity, 'ERROR');
  assert.equal(required[0].code, 'CBQ-SEQ-REQUIRED-FOLDER-MISSING');
  assert.match(required[0].remediation, /required pass folder/);

  const optional = QC.sequenceRecords(
    {name: 'LINE', required: false},
    {frames: {count: 3}},
    {folderExists: false}
  );
  assert.equal(optional[0].severity, 'WARNING');
  assert.equal(optional[0].code, 'CBQ-SEQ-OPTIONAL-FOLDER-MISSING');
}

{
  const incomplete = QC.sequenceRecords(
    {name: 'BEAUTY', required: true},
    {frames: {count: 3}},
    {folderExists: true, complete: false, missing: [2], unexpected: []}
  );
  assert.equal(incomplete[0].code, 'CBQ-SEQ-REQUIRED-FRAMES-MISSING');
  assert.match(incomplete[0].detail, /2/);

  const completeWithExtra = QC.sequenceRecords(
    {name: 'BEAUTY', required: true},
    {frames: {count: 3}},
    {folderExists: true, complete: true, missing: [], unexpected: ['C001_BEAUTY_01.png']}
  );
  assert.deepEqual(codes(completeWithExtra), ['CBQ-SEQ-COMPLETE', 'CBQ-SEQ-UNEXPECTED-MATCHES']);
  assert.equal(QC.summarize(completeWithExtra).status, 'WARNING');
}

{
  const clean = QC.compRecords([]);
  assert.equal(clean[0].severity, 'PASS');
  assert.equal(clean[0].code, 'CBQ-COMP-SPEC-OK');

  const drift = QC.compRecords(['frame rate', 'pixel aspect', 'duration']);
  assert.deepEqual(codes(drift), [
    'CBQ-COMP-DRIFT-FRAME-RATE',
    'CBQ-COMP-DRIFT-PIXEL-ASPECT',
    'CBQ-COMP-DRIFT-DURATION'
  ]);
  assert.ok(drift.every(r => r.severity === 'ERROR'));
  assert.ok(drift.every(r => /will not rewrite comp settings automatically/.test(r.remediation)));
}

{
  const pass = {name: 'BEAUTY', required: true};
  const footageOk = QC.managedObjectRecords('footage', pass, {status: 'ok'});
  assert.equal(footageOk[0].code, 'CBQ-FOOTAGE-OK');
  assert.equal(footageOk[0].severity, 'PASS');

  const requiredMissing = QC.managedObjectRecords('layer', pass, {status: 'missing'});
  assert.equal(requiredMissing[0].code, 'CBQ-LAYER-REQUIRED-MISSING');
  assert.equal(requiredMissing[0].severity, 'ERROR');
  assert.match(requiredMissing[0].remediation, /trusted package/);

  const optionalMissing = QC.managedObjectRecords('layer', {name: 'LINE', required: false}, {status: 'missing'});
  assert.equal(optionalMissing[0].code, 'CBQ-LAYER-OPTIONAL-MISSING');
  assert.equal(optionalMissing[0].severity, 'WARNING');
  assert.match(optionalMissing[0].remediation, /will not synthesize or adopt/);

  const ownership = QC.managedObjectRecords('footage', pass, {
    status: 'ownership_error',
    message: 'Managed footage source/tag no longer matches.'
  });
  assert.equal(ownership[0].code, 'CBQ-FOOTAGE-OWNERSHIP-ERROR');
  assert.equal(ownership[0].severity, 'ERROR');
  assert.match(ownership[0].remediation, /will not adopt, retag, or replace/);
}

{
  const cleanHost = QC.hostRecords({inspectable: true, staleManagedTags: 0, ownershipAmbiguous: false});
  assert.equal(cleanHost[0].code, 'CBQ-HOST-OWNERSHIP-OK');
  assert.equal(cleanHost[0].severity, 'PASS');

  const unsafeHost = QC.hostRecords({
    inspectable: false,
    staleManagedTags: 2,
    ownershipAmbiguous: true,
    message: 'Duplicate managed roots conflict.'
  });
  assert.deepEqual(codes(unsafeHost), [
    'CBQ-HOST-STATE-UNINSPECTABLE',
    'CBQ-HOST-STALE-MANAGED-TAG',
    'CBQ-HOST-OWNERSHIP-AMBIGUOUS'
  ]);
  assert.ok(unsafeHost.every(r => r.severity === 'ERROR'));
  assert.ok(unsafeHost.every(r => r.remediation.length > 0));
}

{
  const safe = QC.revisionRecords({status: 'safe', reasons: [], warnings: []}, 'V004');
  assert.equal(safe[0].code, 'CBQ-REV-SAFE');
  assert.equal(safe[0].severity, 'PASS');

  const warning = QC.revisionRecords({status: 'warning', reasons: [], warnings: ['Required/optional status changed: LINE']}, 'V004');
  assert.equal(warning[0].code, 'CBQ-REV-POLICY-WARNING');
  assert.equal(warning[0].severity, 'WARNING');
  assert.match(warning[0].remediation, /explicit revision confirmation/);

  const incompatible = QC.revisionRecords({status: 'incompatible', reasons: ['Adding passes is unsupported by source-only revision: DEPTH'], warnings: []}, 'V004');
  assert.equal(incompatible[0].code, 'CBQ-REV-INCOMPATIBLE');
  assert.equal(incompatible[0].severity, 'ERROR');
  assert.match(incompatible[0].remediation, /Do not source-swap/);
}

{
  const input = [
    {severity: 'WARNING', code: 'CBQ-SEQ-OPTIONAL-FOLDER-MISSING', scope: 'sequence', subject: 'LINE', message: 'Optional pass folder is missing.', remediation: 'Render if needed.'},
    {severity: 'ERROR', code: 'CBQ-COMP-DRIFT-RESOLUTION', scope: 'comp', message: 'Resolution differs.', remediation: 'Restore intended resolution.'},
    {severity: 'PASS', code: 'CBQ-SEQ-COMPLETE', scope: 'sequence', subject: 'BEAUTY', message: '3/3 expected frames are present.'}
  ];
  assert.equal(QC.render(input).text, QC.render(input.slice().reverse()).text, 'QC output must be deterministic regardless of insertion order');
}

console.log('S7 QC+ diagnostic engine: PASS (severity/codes/remediation/determinism/sequence/comp/ownership/host/revision)');
