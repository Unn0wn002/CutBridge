from __future__ import annotations

from .localization import localized_issue, normalize_language


_SPECIFIC = {
    "LINE_OUTPUT_UNAVAILABLE": {
        "EN": {
            "title": "Line Pass Cannot Be Generated",
            "what": "Line is enabled, but Blender Freestyle output is unavailable.",
            "why": "The active render engine/View Layer is not exposing a Freestyle output from the Render Layers node.",
            "continue": "No — not while Line remains enabled.",
            "fix": "Enable Freestyle and As Render Pass for this View Layer, or disable Line.",
        },
        "JA": {
            "title": "Lineパスを生成できません",
            "what": "Lineが有効ですが、BlenderのFreestyle出力を利用できません。",
            "why": "現在のレンダーエンジン/View Layerで、Render LayersノードのFreestyle出力が有効になっていません。",
            "continue": "いいえ — Lineを有効にしたままでは続行できません。",
            "fix": "このView LayerでFreestyleと「As Render Pass」を有効にするか、Lineを無効にしてください。",
        },
    },
    "DEPTH_FORMAT_LOSSY": {
        "EN": {
            "title": "Depth Format Warning",
            "what": "Depth is enabled, but the selected sequence format is not OpenEXR.",
            "why": "Depth stores precise camera-distance values; non-OpenEXR output may reduce that precision.",
            "continue": "Yes — this is a warning, not an error.",
            "fix": "Use OpenEXR when accurate Depth data is required.",
        },
        "JA": {
            "title": "Depth形式の警告",
            "what": "Depthが有効ですが、連番形式がOpenEXRではありません。",
            "why": "Depthはカメラからの距離を高精度で保持するため、OpenEXR以外では精度が低下する可能性があります。",
            "continue": "はい — これは警告であり、エラーではありません。",
            "fix": "正確なDepthデータが必要な場合はOpenEXRを使用してください。",
        },
    },
}

_GENERIC = {
    "EN": {
        "ERROR": ("Error", "CutBridge cannot safely continue with the current configuration.", "No."),
        "WARNING": ("Warning", "The workflow may continue, but this condition can affect the result.", "Yes, after reviewing the consequence."),
        "INFO": ("Information", "This is informational and does not block the workflow.", "Yes."),
    },
    "JA": {
        "ERROR": ("エラー", "現在の設定ではCutBridgeを安全に続行できません。", "いいえ。"),
        "WARNING": ("警告", "続行できますが、結果に影響する可能性があるため内容を確認してください。", "はい。影響を確認してから続行できます。"),
        "INFO": ("情報", "情報のみで、ワークフローは停止しません。", "はい。"),
    },
}


def diagnostic_parts(language: str | None, item: dict) -> dict[str, str]:
    """Return user-facing diagnostic fields without changing stable support codes."""
    lang = normalize_language(language)
    code = str(item.get("code", ""))
    specific = _SPECIFIC.get(code, {}).get(lang)
    if specific is not None:
        return dict(specific)

    level = str(item.get("level", "INFO")).upper()
    if level not in {"ERROR", "WARNING", "INFO"}:
        level = "INFO"
    message, fix = localized_issue(lang, item)
    title, why, can_continue = _GENERIC[lang][level]
    return {
        "title": title,
        "what": message,
        "why": why,
        "continue": can_continue,
        "fix": fix,
    }


def _canonical_support_text(item: dict) -> str:
    message = str(item.get("message", "")).strip()
    fix = str(item.get("fix", "")).strip()
    if not message:
        return ""
    if fix:
        return f"{message} Fix: {fix}"
    return message


def format_diagnostic(language: str | None, item: dict) -> str:
    """Compact structured diagnostic that preserves canonical support text.

    The human-facing EN/JA explanation leads. Canonical English text remains
    present when it would otherwise disappear so existing support recipes and
    host-side regression checks do not lose stable diagnostic substrings.
    """
    lang = normalize_language(language)
    parts = diagnostic_parts(lang, item)
    text = f"{parts['title']}: {parts['what']} Why: {parts['why']} Can I continue? {parts['continue']}"
    if parts["fix"]:
        text += f" Fix: {parts['fix']}"

    canonical = _canonical_support_text(item)
    if canonical and canonical not in text:
        text += f" [EN] {canonical}"
    return text
