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

console.log('S7 QC+ diagnostic engine: PASS (severity/codes/remediation/deterministic ordering/sequence/comp/revision)');
