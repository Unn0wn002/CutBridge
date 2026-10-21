from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'apps' / 'after-effects' / 'CutBridge.jsx').read_text(encoding='utf-8')


def test_beta2_ae_panel_has_status_hierarchy_and_context_help():
    assert 'function showContextHelp(topic)' in SOURCE
    assert 'status_ready: "READY"' in SOURCE
    assert 'status_warning: "WARNING"' in SOURCE
    assert 'status_error: "ERROR"' in SOURCE
    assert 'status_ready: "準備完了 / READY"' in SOURCE
    assert 'status_warning: "警告 / WARNING"' in SOURCE
    assert 'status_error: "エラー / ERROR"' in SOURCE
    assert SOURCE.count('row.add("button", undefined, "?")') == 1
    for topic in ('load', 'build', 'qc', 'revision'):
        assert f'"{topic}"' in SOURCE


def test_beta2_ae_panel_explains_what_to_do_and_when():
    for key in ('desc_load', 'desc_build', 'desc_qc', 'desc_revision'):
        assert f'{key}:' in SOURCE
    for suffix in ('_what', '_when', '_recommended', '_limits'):
        assert f'help_load{suffix}' in SOURCE
        assert f'help_build{suffix}' in SOURCE
        assert f'help_qc{suffix}' in SOURCE
        assert f'help_revision{suffix}' in SOURCE


def test_panel_open_and_help_are_not_bound_to_build_side_effects():
    tail = SOURCE[SOURCE.index('var panel = buildUI(thisObj);'):]
    assert 'buildComp();' not in tail
    assert 'runQC();' not in tail
    assert 'updateRevision();' not in tail
