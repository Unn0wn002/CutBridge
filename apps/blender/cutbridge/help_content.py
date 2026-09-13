from __future__ import annotations

from .localization import normalize_language


HELP_CONTENT = {
    "beauty": {
        "EN": ("Beauty", (
            ("What is this?", "The normal Combined/Image render used as the main picture."),
            ("When to use it", "Enable Beauty for the primary rendered image sequence."),
            ("Limitations", "Beauty uses the active scene, View Layer, renderer, and color-management setup."),
            ("Artist work", "CutBridge links the Render Layers output to its own managed File Output node; artist-owned compositor nodes are preserved."),
        )),
        "JA": ("Beauty", (
            ("これは何？", "通常のCombined/Imageレンダーで、メイン映像として使用します。"),
            ("いつ使う？", "主要なレンダー連番を書き出すときに有効にします。"),
            ("制限", "現在のScene、View Layer、レンダーエンジン、カラーマネジメント設定を使用します。"),
            ("既存作業への影響", "CutBridge管理のFile Outputノードへ接続し、アーティスト所有のコンポジターノードは保持します。"),
        )),
    },
    "line": {
        "EN": ("Line", (
            ("What is this?", "A Freestyle line-art render pass for outlines and line work."),
            ("How to use it", "Enable Blender Freestyle and Freestyle 'As Render Pass' for the active View Layer, then run Validate Cut."),
            ("Can I continue if unavailable?", "No. Disable Line or configure a renderer/View Layer that exposes the Freestyle Render Layers output."),
            ("Artist work", "Validation probes a detached compositor tree and does not rewrite the artist compositor."),
        )),
        "JA": ("Line", (
            ("これは何？", "輪郭線や線画用のFreestyleレンダーパスです。"),
            ("使い方", "Blender Freestyleと、現在のView Layerの「As Render Pass」を有効にしてから「カットを検証」を実行します。"),
            ("利用できない場合", "続行できません。Lineを無効にするか、Freestyle出力に対応したレンダー/View Layer設定へ変更してください。"),
            ("既存作業への影響", "検証は独立した一時コンポジターツリーで行い、アーティストのコンポジターを変更しません。"),
        )),
    },
    "shadow": {
        "EN": ("Shadow", (
            ("What is this?", "The renderer's Shadow data pass, when the active engine/View Layer exposes it."),
            ("When to use it", "Use it when compositing needs shadow information separated from Beauty."),
            ("Limitations", "Availability is renderer-dependent. Validate Cut must pass before Build Package."),
            ("Optional?", "Yes. Disable Shadow when the current renderer does not provide the required pass."),
        )),
        "JA": ("Shadow", (
            ("これは何？", "現在のレンダーエンジン/View Layerが提供するShadowデータパスです。"),
            ("いつ使う？", "Beautyとは別に影情報をコンポジットしたい場合に使用します。"),
            ("制限", "対応状況はレンダーエンジンに依存します。「パッケージ作成」の前に検証を通してください。"),
            ("任意？", "はい。必要なShadowパスを提供できない設定では無効にしてください。"),
        )),
    },
    "depth": {
        "EN": ("Depth", (
            ("What is this?", "A camera-distance data pass used for depth-based compositing and effects."),
            ("Recommended format", "Use OpenEXR when accurate Depth values are required."),
            ("PNG/TIFF", "CutBridge allows the workflow to continue but warns because precision can be reduced."),
            ("Optional?", "Yes. Enable Depth only when downstream compositing needs it."),
        )),
        "JA": ("Depth", (
            ("これは何？", "深度ベースのコンポジットやエフェクトに使う、カメラ距離のデータパスです。"),
            ("推奨形式", "正確なDepth値が必要な場合はOpenEXRを使用してください。"),
            ("PNG/TIFF", "続行はできますが、精度が低下する可能性があるためCutBridgeは警告します。"),
            ("任意？", "はい。後工程でDepthが必要な場合だけ有効にします。"),
        )),
    },
    "sequence_format": {
        "EN": ("Sequence Format", (
            ("What is this?", "The image-sequence format used by the current v0.2.3 package architecture."),
            ("Current behavior", "One selected format applies to every enabled pass in the package."),
            ("Recommended", "PNG is practical for normal image passes; OpenEXR is recommended when accurate Depth data matters."),
            ("Limitation", "Per-pass format overrides are not part of the current stable manifest contract."),
        )),
        "JA": ("連番形式", (
            ("これは何？", "現在のv0.2.3パッケージ構成で使用する画像連番形式です。"),
            ("現在の動作", "選択した1つの形式が、パッケージ内の有効な全パスに適用されます。"),
            ("推奨", "通常の画像パスはPNGが扱いやすく、正確なDepthが必要な場合はOpenEXRを推奨します。"),
            ("制限", "パスごとの形式上書きは、現在の安定したmanifest契約には含まれていません。"),
        )),
    },
    "studio_preset": {
        "EN": ("Studio Preset", (
            ("What is this?", "A validated data-only profile for naming, folders, enabled passes, format, version token, and AE comp naming."),
            ("Manual", "Keeps the visible pass and format controls editable."),
            ("Default/Custom", "Preset-controlled values become read-only so package identity stays deterministic."),
            ("Safety", "Custom presets are declarative JSON and are validated before use."),
        )),
        "JA": ("スタジオプリセット", (
            ("これは何？", "命名、フォルダー、有効パス、形式、バージョン表記、AEコンポ名を定義する検証済みデータプロファイルです。"),
            ("手動", "表示されているパス/形式設定を編集できます。"),
            ("Default/Custom", "パッケージ識別を決定的に保つため、プリセット管理項目は読み取り専用になります。"),
            ("安全性", "Customプリセットは宣言的JSONのみで、使用前に検証されます。"),
        )),
    },
    "validate": {
        "EN": ("Validate Cut", (
            ("What does it do?", "Checks metadata, renderer/pass capability, Line/Freestyle readiness, preset validity, optional handoff data, and package-target safety."),
            ("Does it build?", "No. Validation does not create a package."),
            ("Errors", "An ERROR must be fixed before Build Package can safely continue."),
            ("Warnings", "A WARNING explains a consequence but does not necessarily block Build Package."),
        )),
        "JA": ("カットを検証", (
            ("何をする？", "メタデータ、レンダー/パス対応、Line/Freestyle、プリセット、任意ハンドオフデータ、出力先の安全性を確認します。"),
            ("作成もする？", "いいえ。検証だけではパッケージを作成しません。"),
            ("エラー", "ERRORは「パッケージ作成」の前に修正する必要があります。"),
            ("警告", "WARNINGは影響を説明しますが、必ずしも作成を停止しません。"),
        )),
    },
    "build": {
        "EN": ("Build Package", (
            ("What does it do?", "Creates deterministic CutBridge-managed render outputs, folders, and cutbridge.json after preflight passes."),
            ("Overwrite safety", "Existing rendered/user data for the same package version is not overwritten."),
            ("Failure safety", "Pass mapping is transactional; a failed mapping attempt removes its pending nodes and restores changed render/View Layer flags."),
            ("Next revision", "Increase Version for a new V002/V003 package rather than replacing an existing revision."),
        )),
        "JA": ("パッケージ作成", (
            ("何をする？", "検証後にCutBridge管理のレンダー出力、フォルダー、cutbridge.jsonを決定的に作成します。"),
            ("上書き保護", "同じVersionに既存のレンダー/ユーザーデータがある場合は上書きしません。"),
            ("失敗時の安全性", "パスマッピングはトランザクション方式で、失敗した一時ノードを削除し変更したレンダー/View Layer設定を戻します。"),
            ("次のリビジョン", "既存リビジョンを置き換えず、Versionを上げてV002/V003を作成してください。"),
        )),
    },
    "version": {
        "EN": ("Version", (
            ("What is this?", "The package revision number used to separate V001, V002, V003, and later handoffs."),
            ("When to change it", "Increment Version when creating a new revision after an existing package contains render/user data."),
            ("Safety", "Different versions get distinct package identities so earlier revisions can coexist."),
        )),
        "JA": ("バージョン", (
            ("これは何？", "V001、V002、V003などのハンドオフを分離するパッケージのリビジョン番号です。"),
            ("いつ変更する？", "既存パッケージにレンダー/ユーザーデータがある状態で新しいリビジョンを作るときに増やします。"),
            ("安全性", "Versionごとに別のパッケージ識別を持つため、以前のリビジョンと共存できます。"),
        )),
    },
    "camera": {
        "EN": ("Camera", (
            ("What is this?", "The active Blender scene camera recorded in the package metadata."),
            ("Required", "A scene camera is required for a valid production cut."),
            ("3D handoff", "Experimental producer-side Camera/3D sample data remains hidden and is not release-facing until native AE reconstruction is fully validated."),
        )),
        "JA": ("カメラ", (
            ("これは何？", "パッケージメタデータに記録されるBlender Sceneのアクティブカメラです。"),
            ("必須", "有効なプロダクションカットにはSceneカメラが必要です。"),
            ("3Dハンドオフ", "実験的なCamera/3Dサンプル出力は非表示のままで、AE側のネイティブ再構築検証が完了するまでリリース向け機能として扱いません。"),
        )),
    },
    "output_path": {
        "EN": ("Package Output", (
            ("What is this?", "The parent directory where versioned CutBridge package folders are created."),
            ("Relative paths", "A // path is relative to the saved .blend file; save the blend before relying on it."),
            ("Safety", "CutBridge checks the target before Build and fails closed on unsafe collisions or protected existing data."),
        )),
        "JA": ("パッケージ出力先", (
            ("これは何？", "Version付きCutBridgeパッケージフォルダーを作成する親ディレクトリです。"),
            ("相対パス", "// は保存済み.blendファイル基準です。利用する前にblendを保存してください。"),
            ("安全性", "作成前に出力先を検証し、危険な衝突や保護すべき既存データがある場合は停止します。"),
        )),
    },
    "three_d_handoff": {
        "EN": ("Camera / 3D Handoff", (
            ("Status", "Experimental producer-only data path; it is intentionally not a normal release-facing control."),
            ("What it can contain", "Camera and supported transform samples for controlled Blender-to-AE reconstruction experiments."),
            ("Limitation", "Do not assume AE Camera/3D Null creation is release-supported until the exact native-host validation gate passes."),
        )),
        "JA": ("Camera / 3Dハンドオフ", (
            ("状態", "実験的なproducer-onlyデータ経路で、通常のリリース向け操作としては意図的に表示していません。"),
            ("含められるもの", "管理されたBlender→AE再構築試験用のCameraおよび対応トランスフォームサンプルです。"),
            ("制限", "正確なネイティブホスト検証ゲートを通るまでは、AE Camera/3D Null生成をリリース対応と見なさないでください。"),
        )),
    },
}


def get_help(topic: str, language: str | None):
    item = HELP_CONTENT.get(str(topic), HELP_CONTENT["validate"])
    return item[normalize_language(language)]
