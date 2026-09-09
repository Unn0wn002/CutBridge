const assert = require('assert');
const l10n = require('../apps/after-effects/localization.js');

function test(name, fn) {
  try {
    fn();
    console.log('PASS ' + name);
  } catch (err) {
    console.error('FAIL ' + name + ': ' + err.message);
    process.exitCode = 1;
  }
}

test('Japanese is the first-class default with deterministic English fallback', () => {
  assert.strictEqual(l10n.DEFAULT_LOCALE, 'JA');
  assert.strictEqual(l10n.FALLBACK_LOCALE, 'EN');
  assert.strictEqual(l10n.normalizeLocale('ja'), 'JA');
  assert.strictEqual(l10n.normalizeLocale('EN'), 'EN');
  assert.strictEqual(l10n.normalizeLocale('unknown'), 'EN');
});

test('primary panel labels are locale-aware and not slash-combined', () => {
  const keys = ['language_label', 'no_package', 'import_package', 'build_comp', 'run_qc', 'update_revision'];
  keys.forEach((key) => {
    const ja = l10n.tr('JA', key);
    const en = l10n.tr('EN', key);
    assert(ja.length > 0 && en.length > 0);
    assert.notStrictEqual(ja, en);
    assert(!ja.includes(' / '));
    assert(!en.includes(' / '));
  });
});

test('missing keys and invalid locale fall back safely', () => {
  assert.strictEqual(l10n.tr('JA', 's8.missing.key'), 's8.missing.key');
  assert.strictEqual(l10n.tr('invalid', 'build_comp'), '2. Build Comp');
});

test('locale state changes without touching workflow data', () => {
  assert.strictEqual(l10n.setLocale('EN'), 'EN');
  assert.strictEqual(l10n.getLocale(), 'EN');
  assert.strictEqual(l10n.setLocale('JA'), 'JA');
  assert.strictEqual(l10n.getLocale(), 'JA');
});

test('Japanese error wrapper preserves canonical English support detail', () => {
  const canonical = 'FPS changes are unsupported.';
  const text = l10n.formatError('JA', canonical);
  assert(text.startsWith('CutBridge エラー'));
  assert(text.includes('[EN] ' + canonical));
  assert.strictEqual(l10n.formatError('EN', canonical), 'CutBridge\n\n' + canonical);
});

test('revision reasons are Japanese-first while canonical text survives', () => {
  const fps = l10n.localizeRevisionReason('JA', 'FPS changes are unsupported.');
  assert(fps.startsWith('FPSの変更には対応していません。'));
  assert(fps.includes('[EN] FPS changes are unsupported.'));
  const block = l10n.formatRevisionBlocked('JA', ['Resolution changes are unsupported.']);
  assert(block.startsWith('差し替えを実行できません:'));
  assert(block.includes('[EN] Resolution changes are unsupported.'));
});

test('QC localization preserves stable CBQ code and canonical English message', () => {
  const record = {
    severity: 'ERROR',
    code: 'CBQ-COMP-DRIFT-FRAME-RATE',
    scope: 'comp',
    subject: 'C012_COMP',
    message: 'Managed comp metadata mismatch: frame rate.',
    remediation: 'Restore the intended managed comp metadata.'
  };
  const localized = l10n.localizeDiagnostic('JA', record);
  assert.strictEqual(localized.code, record.code);
  assert.strictEqual(localized.severity, record.severity);
  assert(localized.message.startsWith('管理コンポのフレームレート'));
  assert(localized.message.includes('[EN] ' + record.message));
  assert(localized.remediation.includes('[EN] ' + record.remediation));
  assert.deepStrictEqual(l10n.localizeDiagnostic('EN', record), record);
});

test('QC headline and remediation marker remain support-readable', () => {
  assert.strictEqual(l10n.qcHeadline('JA', 'PASS'), '合格 / PASS');
  assert.strictEqual(l10n.qcHeadline('JA', 'ERROR'), 'エラー / ERROR');
  const text = l10n.localizeRenderedQC('JA', 'ERROR [CBQ-X] x\nNext: Repair it.');
  assert(text.includes('対処 / Next: Repair it.'));
  assert(text.includes('CBQ-X'));
});

if (process.exitCode) process.exit(process.exitCode);
console.log('S8 After Effects localization engine: PASS');
