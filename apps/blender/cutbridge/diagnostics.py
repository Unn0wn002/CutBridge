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
    "SHADOW_OUTPUT_UNAVAILABLE": {
        "EN": {
            "title": "Shadow Pass Cannot Be Generated",
            "what": "Shadow is enabled, but the active renderer/View Layer does not expose the required Shadow output.",
            "why": "Shadow pass availability depends on the render engine. Blender 5.2 exposes the standalone Shadow pass in EEVEE, not Cycles.",
            "continue": "No — not while Shadow remains enabled in this renderer configuration.",
            "fix": "Use an EEVEE/View Layer setup that exposes Shadow, or disable Shadow.",
        },
        "JA": {
            "title": "Shadowパスを生成できません",
            "what": "Shadowが有効ですが、現在のレンダーエンジン/View Layerでは必要なShadow出力を利用できません。",
            "why": "Shadowパスの利用可否はレンダーエンジンに依存します。Blender 5.2の単独ShadowパスはEEVEEで利用でき、Cyclesでは利用できません。",
            "continue": "いいえ — このレンダー設定でShadowを有効にしたままでは続行できません。",
            "fix": "Shadow出力を利用できるEEVEE/View Layer設定を使用するか、Shadowを無効にしてください。",
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
    "PACKAGE_RENDER_READY": {
        "EN": {
            "title": "Package Already Built — Ready to Render",
            "what": "The current package already contains render/user payload and its manifest matches the current cut/render settings.",
            "why": "This is a valid post-build state. CutBridge's overwrite protection applies to Build Package, not to Blender's Render Animation command.",
            "continue": "Yes — continue Render Animation. Do not rebuild this same version.",
            "fix": "Increment Version only when intentionally creating a new revision/package.",
        },
        "JA": {
            "title": "パッケージ作成済み — レンダリング可能",
            "what": "現在のパッケージには既存のレンダー/ユーザーデータがあり、manifestは現在のカット/レンダー設定と一致しています。",
            "why": "これは正常な作成後の状態です。CutBridgeの上書き保護は「パッケージ作成」に対するもので、Blenderの「アニメーションをレンダリング」は停止しません。",
            "continue": "はい — そのままアニメーションをレンダリングできます。同じVersionでパッケージを再作成しないでください。",
            "fix": "新しいリビジョン/パッケージを意図して作成するときだけVersionを上げてください。",
        },
    },
    "PACKAGE_EXISTS": {
        "EN": {
            "title": "Existing Package Is Protected",
            "what": "This version already contains render/user data, so Build Package will not overwrite it.",
            "why": "CutBridge protects completed or in-progress package payload from destructive same-version rebuilds.",
            "continue": "Yes for rendering the already-built package; no for rebuilding this same version.",
            "fix": "Continue Render Animation without Build Package, or increment Version for a new revision.",
        },
        "JA": {
            "title": "既存パッケージを保護しています",
            "what": "このVersionには既存のレンダー/ユーザーデータがあるため、「パッケージ作成」では上書きしません。",
            "why": "CutBridgeは完成済み/レンダリング途中のデータを同じVersionの再作成から保護します。",
            "continue": "既存パッケージのレンダリングは続行できますが、同じVersionのパッケージ再作成はできません。",
            "fix": "パッケージを再作成せずレンダリングを続けるか、新しいリビジョンではVersionを上げてください。",
        },
    },
    "PACKAGE_STATE_MISMATCH": {
        "EN": {
            "title": "Existing Package Does Not Match Current Settings",
            "what": "The target package already contains payload, but its manifest cannot be verified as the current cut/render contract.",
            "why": "Writing new output with changed settings could mix incompatible frames or metadata into an existing revision.",
            "continue": "No — not for new output into this existing package with the changed settings.",
            "fix": "Restore the settings used by the package or increment Version for a new revision.",
        },
        "JA": {
            "title": "既存パッケージと現在の設定が一致しません",
            "what": "出力先には既存データがありますが、manifestを現在のカット/レンダー契約と一致する状態として確認できません。",
            "why": "設定が変わったまま新しい出力を書き込むと、既存リビジョンに互換性のないフレームやメタデータが混在する可能性があります。",
            "continue": "いいえ — 変更後の設定で、この既存パッケージへ新しい出力を追加しないでください。",
            "fix": "そのパッケージ作成時の設定に戻すか、新しいリビジョンとしてVersionを上げてください。",
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
