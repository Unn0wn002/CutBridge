from __future__ import annotations

SUPPORTED_LANGUAGES = ("JA", "EN")
DEFAULT_LANGUAGE = "JA"
FALLBACK_LANGUAGE = "EN"

_STRINGS = {
    "EN": {
        "language": "UI Language",
        "project_setup": "Project Setup",
        "scene_metadata": "Scene Metadata",
        "studio_preset": "Studio Preset",
        "preset_mode": "Preset Mode",
        "preset_json": "Preset JSON",
        "preset_manual_hint": "Manual mode keeps the existing pass and format controls.",
        "preset_managed_hint": "Preset mode controls naming, folders, passes, format, version token, and AE comp naming.",
        "preset_controls_passes": "Pass and format controls are read-only while a preset is active.",
        "pass_package": "Pass Package",
        "export": "Export",
        "validation_status": "Validation Status",
        "environment": "Environment",
        "updates": "Updates",
        "project": "Project",
        "episode": "Episode",
        "scene": "Scene",
        "cut": "Cut",
        "take": "Take",
        "version": "Version",
        "package_output": "Package Output",
        "sequence_format": "Sequence Format",
        "beauty": "Beauty",
        "line": "Line",
        "shadow": "Shadow",
        "depth": "Depth",
        "fps": "FPS: {value}",
        "frames": "Frames: {value}",
        "resolution": "Resolution: {value}",
        "camera": "Camera: {value}",
        "camera_not_set": "NOT SET",
        "validate_cut": "Validate Cut",
        "build_package": "Build Package",
        "open_package_folder": "Open Package Folder",
        "ready_to_build": "Ready to build",
        "validation_counts": "{errors} error(s), {warnings} warning(s)",
        "fix": "Fix: {value}",
        "more_issues": "+ {count} more — run Validate Cut for details",
        "platform": "Platform: {value}",
        "python": "Python: {value}",
        "online_access": "Online access: {value}",
        "enabled": "Enabled",
        "disabled": "Disabled",
        "preferences_unavailable": "CutBridge preferences unavailable",
        "channel": "Channel: {value}",
        "update_endpoint_missing": "Update endpoint not configured",
        "online_access_disabled": "Blender online access is disabled",
        "check_updates": "Check for Updates",
        "new_version": "New version: {value}",
        "open_release_page": "Open Release Page",
        "not_checked": "Not checked",
        "updates_user_approved": "No forced updates; installation remains user-approved",
        "validation_failed": "CutBridge: {errors} error(s), {warnings} warning(s). {detail}",
        "validation_warning": "CutBridge: valid with {warnings} warning(s). {detail}",
        "validation_passed": "CutBridge: validation passed. Package target is safe to build.",
        "package_build_failed": "CutBridge package build failed: {detail}",
        "package_created": "CutBridge package created: {path}",
        "build_first": "Build a package first.",
    },
    "JA": {
        "language": "表示言語",
        "project_setup": "プロジェクト設定",
        "scene_metadata": "シーン情報",
        "studio_preset": "スタジオプリセット",
        "preset_mode": "プリセットモード",
        "preset_json": "プリセットJSON",
        "preset_manual_hint": "手動モードでは従来のレンダーパスと形式設定を使用します。",
        "preset_managed_hint": "プリセットが命名、フォルダー、パス、形式、バージョン表記、AEコンポ名を管理します。",
        "preset_controls_passes": "プリセット使用中はレンダーパスと形式設定は読み取り専用です。",
        "pass_package": "レンダーパス",
        "export": "書き出し",
        "validation_status": "検証ステータス",
        "environment": "動作環境",
        "updates": "アップデート",
        "project": "プロジェクト",
        "episode": "話数",
        "scene": "シーン",
        "cut": "カット",
        "take": "テイク",
        "version": "バージョン",
        "package_output": "パッケージ出力先",
        "sequence_format": "連番形式",
        "beauty": "Beauty",
        "line": "Line",
        "shadow": "Shadow",
        "depth": "Depth",
        "fps": "FPS: {value}",
        "frames": "フレーム: {value}",
        "resolution": "解像度: {value}",
        "camera": "カメラ: {value}",
        "camera_not_set": "未設定",
        "validate_cut": "カットを検証",
        "build_package": "パッケージ作成",
        "open_package_folder": "パッケージフォルダーを開く",
        "ready_to_build": "作成準備OK",
        "validation_counts": "エラー {errors}件 / 警告 {warnings}件",
        "fix": "対処: {value}",
        "more_issues": "ほか {count}件 — 詳細は「カットを検証」を実行",
        "platform": "OS: {value}",
        "python": "Python: {value}",
        "online_access": "オンラインアクセス: {value}",
        "enabled": "有効",
        "disabled": "無効",
        "preferences_unavailable": "CutBridge設定を読み込めません",
        "channel": "チャンネル: {value}",
        "update_endpoint_missing": "アップデート配信先が未設定です",
        "online_access_disabled": "Blenderのオンラインアクセスが無効です",
        "check_updates": "アップデートを確認",
        "new_version": "新しいバージョン: {value}",
        "open_release_page": "リリースページを開く",
        "not_checked": "未確認",
        "updates_user_approved": "強制更新はありません。インストールはユーザー承認後に実行されます",
        "validation_failed": "CutBridge: エラー {errors}件 / 警告 {warnings}件。{detail}",
        "validation_warning": "CutBridge: 警告 {warnings}件があります。{detail}",
        "validation_passed": "CutBridge: 検証に合格しました。パッケージを安全に作成できます。",
        "package_build_failed": "CutBridgeパッケージの作成に失敗しました: {detail}",
        "package_created": "CutBridgeパッケージを作成しました: {path}",
        "build_first": "先にパッケージを作成してください。",
    },
}

_ISSUES_JA = {
    "VIEW_LAYER_MISSING": ("有効なView Layerがありません。", "View Layerを作成または有効化してください。"),
    "PASS_MAPPING_UNSUPPORTED": ("選択したレンダーパスを現在のレンダー設定で使用できません。", "該当パスを無効化するか、対応するレンダーエンジン/View Layer設定に変更してください。"),
    "DEPTH_FORMAT_LOSSY": ("DEPTHは浮動小数点データですが、OpenEXR以外が選択されています。", "DEPTH値を正確に保持する場合はOpenEXRを使用してください。"),
    "ID_MISSING": ("カット識別情報に未入力項目があります。", "プロジェクト/話数/シーン/カット/テイクを確認してください。"),
    "CAMERA_MISSING": ("アクティブカメラが設定されていません。", "Scene Propertiesでアクティブカメラを設定してください。"),
    "FPS_INVALID": ("FPSは0より大きい値が必要です。", "有効なFPSを設定してください。"),
    "NEGATIVE_FRAMES_UNSUPPORTED": ("負の書き出しフレームには対応していません。", "カットとプリロールを0フレーム以降へ移動してください。"),
    "FRAME_RANGE_INVALID": ("終了フレームが開始フレームより前です。", "フレーム範囲を修正してください。"),
    "RESOLUTION_INVALID": ("解像度は正の値が必要です。", "有効な解像度を設定してください。"),
    "PASS_MISSING": ("レンダーパスが選択されていません。", "少なくとも1つのパスを有効にしてください。"),
    "OUTPUT_MISSING": ("パッケージ出力先が空です。", "パッケージ出力先を選択してください。"),
    "BLEND_UNSAVED": (".blendファイルがまだ保存されていません。", "// 相対パスを使う前に.blendファイルを保存してください。"),
    "PRESET_PATH_MISSING": ("カスタムプリセットのJSONファイルが指定されていません。", "手動/標準モードを選ぶか、有効なプリセットJSONを指定してください。"),
    "PRESET_FILE_UNAVAILABLE": ("スタジオプリセットファイルを読み込めません。", "ファイルの場所、権限、UTF-8形式を確認してください。"),
    "PRESET_FILE_TOO_LARGE": ("スタジオプリセットファイルが安全上のサイズ上限を超えています。", "64 KiB以下の宣言的JSONプリセットを使用してください。"),
    "PRESET_JSON_INVALID": ("スタジオプリセットが有効なJSONではありません。", "JSON構文を修正して再検証してください。"),
    "PRESET_SCHEMA_INVALID": ("スタジオプリセットのスキーマが正しくありません。", "CutBridge Studio Presetスキーマを使用してください。"),
    "PRESET_SCHEMA_UNSUPPORTED": ("スタジオプリセットのスキーマバージョンに対応していません。", "現在対応しているスキーマバージョンへ更新してください。"),
    "PRESET_FIELD_INVALID": ("スタジオプリセットに無効または未対応の設定があります。", "プリセットの命名、パス、形式、バージョン設定を確認してください。"),
    "PRESET_PATH_UNSAFE": ("スタジオプリセットに安全でないフォルダーパスがあります。", "相対パスのみを使用し、.. や絶対パスを使用しないでください。"),
    "OUTPUT_UNAVAILABLE": ("パッケージ出力先を使用できません。", "書き込み可能な出力先とアクセス権を確認してください。"),
    "PACKAGE_TARGET_SYMLINK": ("パッケージ出力先がシンボリックリンクです。", "通常のフォルダーを選ぶかCutBridgeのVersionを上げてください。"),
    "PACKAGE_TARGET_NOT_DIRECTORY": ("同名の出力先が存在しますがフォルダーではありません。", "別の出力先を選ぶかCutBridgeのVersionを上げてください。"),
    "PACKAGE_EXISTS": ("同じパッケージに既存のレンダー/ユーザーデータがあります。上書きしません。", "新しいリビジョンとしてVersionを上げるか、既存パッケージを明示的に移動してください。"),
    "PACKAGE_SCAFFOLD_REFRESH": ("同じパッケージがありますがレンダー/ユーザーデータはありません。安全に再作成できます。", "新しいリビジョンにする場合はレンダー前にVersionを上げてください。"),
}


def normalize_language(language: str | None) -> str:
    value = str(language or "").upper()
    return value if value in SUPPORTED_LANGUAGES else FALLBACK_LANGUAGE


def tr(language: str | None, key: str, **values) -> str:
    lang = normalize_language(language)
    template = _STRINGS.get(lang, {}).get(key)
    if template is None:
        template = _STRINGS[FALLBACK_LANGUAGE].get(key, key)
    try:
        return template.format(**values)
    except (KeyError, ValueError):
        return template


def localized_issue(language: str | None, item: dict) -> tuple[str, str]:
    """Return localized user text while leaving stable issue codes untouched."""
    lang = normalize_language(language)
    message = str(item.get("message", "CutBridge validation issue.")).strip()
    fix = str(item.get("fix", "")).strip()
    if lang != "JA":
        return message, fix
    translated = _ISSUES_JA.get(str(item.get("code", "")))
    if translated is None:
        return message, fix
    return translated


def format_localized_issue(language: str | None, item: dict) -> str:
    """Format JP-first interactive text while preserving canonical support text.

    Existing production tests, support recipes, and automation consume stable
    English diagnostic substrings. Japanese therefore leads the interactive
    report, but mapped Japanese diagnostics append their canonical English
    message/fix. Machine-facing validation codes remain outside this formatter.
    """
    lang = normalize_language(language)
    canonical_message = str(item.get("message", "CutBridge validation issue.")).strip()
    canonical_fix = str(item.get("fix", "")).strip()
    message, fix = localized_issue(lang, item)

    localized = message
    if fix:
        localized += " " + tr(lang, "fix", value=fix)

    # English and untranslated Japanese fallbacks are already canonical.
    if lang != "JA" or (message == canonical_message and fix == canonical_fix):
        return localized

    canonical = canonical_message
    if canonical_fix:
        canonical += " Fix: " + canonical_fix
    return localized + " [EN] " + canonical
