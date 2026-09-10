# CutBridge クイックスタート（日本語）

このガイドは、**S9 までの v0.2.3 未リリース開発版**を対象にしています。

CutBridge は Blender のアニメーションカットを After Effects へ受け渡すための制作パイプラインツールです。カット情報、レンダーパス、バージョン、`cutbridge.json`、AE 側の管理対象コンポ／フッテージ／レイヤー、QC、互換性のある差し替え、日本語優先 UI、そして S9 のデータ専用 Studio Preset を一貫したルールで扱います。

基本フロー：

`Blender 情報 + 任意の Studio Preset → Validate Cut → レンダー出力設定／パッケージ作成 → 連番レンダー → AE 読み込み／Build → QC+ → 互換 Revision`

英語版: [QUICK_START.md](QUICK_START.md)

Studio Preset 詳細: [STUDIO_PRESETS.md](STUDIO_PRESETS.md)

## 開発状態

S1〜S8 で Blender→AE の決定的な受け渡し、Ownership / Revision / QC、安全な日本語 UI を構築しました。S9 は既存の Manual 動作と Blender↔AE Package Identity 契約を保持したまま Studio Preset を追加します。

これは開発検証であり Stable / RC 公開許可ではありません。リリースタグ／GitHub Release は存在せず、`release-authorization.json` は未承認のままです。

## 1. Blender 版 CutBridge をインストール

1. 検証対象ソースから作成した CutBridge Blender ZIP を用意します。
2. Blender Preferences から **Install from Disk** など該当バージョンの拡張機能インストール操作を使用します。
3. CutBridge を有効化します。
4. 3D View の `N` サイドバーで **CutBridge** を開きます。
5. 日本語が基本表示です。必要に応じて English へ切り替えられます。

宣言上の最小 Blender は 4.2.0、主要な自動 Runtime 検証は Blender 5.2.1 LTS です。詳細は [COMPATIBILITY.md](COMPATIBILITY.md) を参照してください。

## 2. Blender でカット情報を準備

Validate Cut の前に次を確認します。

1. `.blend` を保存する。
2. Active Camera を設定する。
3. FPS / Resolution を設定する。
4. 書き出し Frame Range を設定する。
5. Project / Episode / Scene / Cut / Take / Version を入力する。
6. Package Output を選択する。
7. **Studio Preset Mode** を選択する。

### Studio Preset Mode

**Manual** は後方互換のデフォルトです。S9 前と同じように BEAUTY / LINE / SHADOW / DEPTH と Sequence Format を直接設定します。標準 Package Identity も維持されます。

例：`PROJECT_EP01_SC010_C012_T01_V001`

**CutBridge Default** は組み込みの安全な宣言型 Preset を使用します。既定 CutBridge 規約を Preset Pipeline 経由で再現します。

**Custom JSON** はユーザーが選択した UTF-8 JSON を厳格に検証して使用します。ファイルを選んだ後、必ず Validate Cut を実行してください。

Preset で変更できる内容：

- Package Naming Template
- Render / Preview / Camera Folder
- Pass の順序と Required / Optional
- Sequence Filename Template
- PNG / OpenEXR / TIFF
- Version Prefix / Padding
- After Effects Comp Name

Preset は**データのみ**です。任意コード、コマンド、ネットワーク処理、環境変数展開は実行できません。

完全な Schema / Example / 制限は [STUDIO_PRESETS.md](STUDIO_PRESETS.md) を参照してください。

### Frame Range

書き出し開始フレームは `0` 以上です。負のフレーム／プリロールは Blender、Schema、AE の各境界で拒否されます。CutBridge はアニメーションを自動リナンバーしません。

## 3. Validate Cut

**Validate Cut** を実行します。

主な検証：

- 必須 ID
- Active Camera
- FPS / Resolution / Frame Range
- Studio Preset Schema / Field / Path Safety
- 解決済み Render Pass
- Package Output
- Renderer / View Layer Capability
- 既存 Package の上書き安全性

`ERROR` は停止条件です。Warning は内容確認が必要です。

Preset 用の安定コードには次があります。

- `PRESET_PATH_MISSING`
- `PRESET_FILE_UNAVAILABLE`
- `PRESET_FILE_TOO_LARGE`
- `PRESET_JSON_INVALID`
- `PRESET_SCHEMA_INVALID`
- `PRESET_SCHEMA_UNSUPPORTED`
- `PRESET_FIELD_INVALID`
- `PRESET_PATH_UNSAFE`

JA / EN を切り替えてもコードと判定ロジックは変わりません。

## 4. レンダー出力マッピング

CutBridge は解決済みの論理 Pass に対して決定的な Blender Compositor Output を設定します。

安全ルール：

- CutBridge 管理ノードは `CUTBRIDGE_` 名前空間を使用します。
- 無関係な Artist Node は保持します。
- Mapping 置換は Transactional です。
- Renderer / View Layer で利用できない Pass を架空に生成しません。
- Mapping 失敗で以前の正常な CutBridge Mapping を壊しません。
- Preset から任意 Blender Operation を実行しません。

## 5. Build Package

Validate 成功後に **Build Package** を実行します。

Manual / Default の代表例：

```text
PROJECT_EP01_SC010_C012_T01_V001/
├── cutbridge.json
├── camera/
├── preview/
└── render/
    ├── beauty/
    ├── line/
    ├── shadow/
    └── depth/
```

実際の Folder / Sequence / Required Policy / Comp Name / Layer Order は `cutbridge.json` に記録されます。

Custom JSON の場合、Build 開始時点の検証済み Preset を 1 回の Build Transaction 用に Memory Snapshot として固定します。Build 中に元 JSON を編集しても Blender Mapping と生成 Manifest が別々の Preset を使うことはありません。

Manifest には正規化済み Preset 情報として `mode`, Schema/Version, Preset `id`, `name` だけを記録します。元 Preset の File Path は記録しません。

### 同一 Version の上書き

既存の同一 Version Package に Render / User Payload がある場合は上書きを拒否します。新しい Version を作成するか、既存 Package を明示的に管理してください。

## 6. Blender で連番をレンダー

CutBridge Output へ必要な Pass をレンダーします。AE へ渡す前に Required Pass が期待 Frame Range を満たしていることを確認します。

## 7. After Effects 版 CutBridge を準備

次の 4 Runtime File を同じ Folder に置きます。

- `CutBridge.jsx`
- `revision_manager.js`
- `qc_plus.js`
- `localization.js`

最初は **File > Scripts > Run Script File...** から `CutBridge.jsx` を実行できます。

Dockable Panel として使用する場合は 4 ファイルすべてを `Scripts/ScriptUI Panels` に配置して AE を再起動します。

`localization.js` が欠けている場合は安全に English Fallback へ移行しますが、Build / QC / Revision Safety は弱くなりません。

## 8. AE で Import / Build

1. `cutbridge.json` を読み込みます。
2. Package Identity / FPS / Frame Count / Validation を確認します。
3. Build を実行します。
4. Required Sequence が不足している場合は失敗します。
5. Optional Pass は Manifest 契約に従い Warning / Skip されます。

S9 でも After Effects は Studio Preset JSON を直接読みません。Blender が解決した Manifest のみを使用します。つまり Preset File を AE 側の新しい Trust Boundary にしません。

## 9. QC+

Build 後や Project 変更後に **QC** を実行します。

QC+ は安定した `CBQ-*` Code を使い、Package / Sequence / Comp / Ownership / Revision State を診断します。

QC は診断専用です。Object の自動採用、Import、Move、Retag、Source Replace、自動修復は行いません。

## 10. V002 / V003 などへ Revision

1. 現在の Managed Project を保持する。
2. 新しい Package を Revision Flow から選択する。
3. Compatibility を確認する。
4. Warning Class は明示確認する。
5. 非互換状態は Source Replacement 前に Fail Closed する。
6. Compatible の場合のみ Verified Managed Source を置換する。
7. Historical Footage は旧 Version Provenance を保持する。
8. 完了後に Build / QC を再実行する。

Preset の Version 表示が `R0012` のように変わっても、Revision Compatibility の基本となる Manifest `version` は数値のままです。

## 11. 日本語／English Safety Boundary

言語変更で変わるのは表示だけです。

次は変わりません。

- Manifest Value
- Package Identity
- Studio Preset Resolution
- Managed Ownership Tag
- `CBQ-*` / `PRESET_*` Code
- Build / QC / Revision Decision
- 無関係な Blender / AE Object

## 12. Release Boundary

v0.2.3 は未リリースです。CI PASS だけを理由に Stable / RC を公開しません。

公開前には issue #18 の Repository-Level Release Governance、検証済み Candidate の `main` への意図的 Promotion、Exact Authorization、実 Tag Release、Downloaded Asset Verification、Production Update Index、残りの E2E / Target User Validation が必要です。

## 次の開発フェーズ

S9 Studio Presets 統合後の次フェーズは **S10 — Camera / Null Handoff Investigation** です。

関連資料：

- [STUDIO_PRESETS.md](STUDIO_PRESETS.md)
- [COMPLETION_STATUS.md](COMPLETION_STATUS.md)
- [ROADMAP.md](ROADMAP.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)
- [After Effects INSTALL](../apps/after-effects/INSTALL.md)
