# CutBridge クイックスタート（日本語）

このガイドは、**S13 までの v0.2.3 未リリース開発版**を対象にしています。

CutBridge は Blender のアニメーションカットを After Effects へ受け渡すための制作パイプラインツールです。カット情報、レンダーパス、バージョン、`cutbridge.json`、AE 側の管理対象コンポ／フッテージ／レイヤー、QC、互換 Revision、日本語優先 UI、データ専用 Studio Preset、そして S10〜S13 で実ホスト検証された限定的な Camera / 3D Null Handoff を一貫したルールで扱います。

基本フロー：

`Blender 情報 + 任意の Studio Preset + 任意の 3D Handoff → Validate Cut → Render Mapping / Package → 連番レンダー → AE Import / Build → handoff_3d がある場合は Camera / 3D Null 再構築 → QC+ → Compatible Revision`

英語版: [QUICK_START.md](QUICK_START.md)

Studio Preset 詳細: [STUDIO_PRESETS.md](STUDIO_PRESETS.md)

3D Handoff 詳細: [HANDOFF_3D.md](HANDOFF_3D.md)

## 開発状態

S1〜S8 で決定的な Blender→AE Handoff、Ownership / Revision / QC、日本語優先 UI を構築しました。S9 で宣言型 Studio Preset を追加し、S10A で Camera / Null の座標・Timing・Projection 契約を確定、S10B で Blender Evaluated-World Producer を追加、S10C で After Effects の Managed Camera / 3D Null 再構築を実装し Native Projection Parity Gate を通過しました。S11 で QA / Documentation / Release Readiness を整備し、S12 で Release-Target の実ホスト End-to-End Campaign を実行しました。S12 で見つかった Native Revision Defect は S13 で修正され、最終 S13F Candidate は V001→V002→V003 を実 AE で通過し、PR #68 で同一 SHA のまま統合されました。

これは開発／Native 検証であり Stable / RC 公開許可ではありません。GitHub Release は存在せず、`release-authorization.json` は Fail-Closed のままです。Repository Governance issue #18 も公開を Block しています。詳細は [RELEASE_READINESS.md](RELEASE_READINESS.md) と [S12_S13_EVIDENCE_SUMMARY.md](S12_S13_EVIDENCE_SUMMARY.md) を参照してください。

## 1. Blender 版 CutBridge をインストール

1. 検証対象ソースから作成した CutBridge Blender ZIP を用意します。
2. Blender Preferences から **Install from Disk** など該当バージョンの拡張機能インストール操作を使用します。
3. CutBridge を有効化します。
4. 3D View の `N` サイドバーで **CutBridge** を開きます。
5. 日本語が基本表示です。必要に応じて English へ切り替えられます。

宣言上の最小 Blender は 4.2.0、主要な自動 Runtime 検証は Blender 5.2.1 LTS です。最小バージョンを満たすだけでは Certification ではありません。詳細は [COMPATIBILITY.md](COMPATIBILITY.md) を参照してください。

## 2. Blender でカット情報を準備

Validate Cut の前に次を確認します。

1. `.blend` を保存する。
2. Active Camera を設定する。
3. FPS / Resolution を設定する。
4. Export Frame Range を設定する。
5. Project / Episode / Scene / Cut / Take / Version を入力する。
6. Package Output を選択する。
7. **Studio Preset Mode** を選択する。

### Studio Preset Mode

**Manual** は後方互換のデフォルトです。BEAUTY / LINE / SHADOW / DEPTH と Sequence Format を直接設定し、標準 Package Identity を維持します。

例：`PROJECT_EP01_SC010_C012_T01_V001`

**CutBridge Default** は組み込みの安全な宣言型 Preset を使用します。

**Custom JSON** はユーザーが選択した UTF-8 JSON を厳格に検証して使用します。ファイルを選んだ後、Validate Cut を実行してください。

Preset で変更できる内容：

- Package Naming Template
- Render / Preview / Camera Folder
- Pass の順序と Required / Optional
- Sequence Filename Template
- PNG / OpenEXR / TIFF
- Version Prefix / Padding
- After Effects Comp Name

Preset は**データのみ**です。任意コード、コマンド、ネットワーク処理、環境変数展開は実行できません。After Effects は Preset JSON を直接読みません。

### Frame Range

書き出し開始フレームは `0` 以上です。負のフレーム／プリロールは Blender、Schema、AE の各境界で拒否されます。CutBridge はアニメーションを自動リナンバーしません。

## 3. 任意の 3D Camera / Empty Handoff

S10 の 3D Handoff は **任意・デフォルト OFF** です。現時点では通常の N-panel Control ではなく Engineering Opt-in です。

Blender Python から有効化します。

```python
bpy.context.scene.cutbridge.handoff_3d_enabled = True
bpy.context.scene.cutbridge.handoff_3d_pixels_per_blender_unit = 100.0
```

AE の Managed 3D Null にしたい Empty だけを明示的に Mark します。

```python
empty["cutbridge_handoff_3d"] = True
```

対応範囲：

- Active Perspective Camera
- Square Pixel
- Camera Shift = 0
- 明示的に Mark した Empty
- Evaluated World Transform を Frame ごとに Bake

未対応 Camera / Transform は Fail-Closed します。Parent / Constraint / Driver は Blender 側の Evaluated World Result に反映できますが、Blender Hierarchy 自体を AE に再構築しません。

有効化前に [HANDOFF_3D.md](HANDOFF_3D.md) を確認してください。

## 4. Validate Cut

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
- 3D Handoff 有効時は S10 Producer Contract

`ERROR` は停止条件です。Warning は内容確認が必要です。Invalid Preset または未対応 Handoff Data は Package 作成前に Fail-Closed します。

JA / EN を切り替えても Stable Code と判定ロジックは変わりません。

## 5. レンダー出力マッピング

CutBridge は解決済みの論理 Pass に対して決定的な Blender Compositor Output を設定します。

安全ルール：

- CutBridge 管理ノードは `CUTBRIDGE_` 名前空間を使用します。
- 無関係な Artist Node は保持します。
- Mapping 置換は Transactional です。
- Renderer / View Layer で利用できない Pass を架空に生成しません。
- Mapping 失敗で以前の正常な CutBridge Mapping を壊しません。
- Preset から任意 Blender Operation を実行しません。

## 6. Build Package

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

3D Handoff が有効かつ Valid の場合、Manifest に Versioned `handoff_3d` Block が追加され、Camera / Empty の Baked Transform / Projection Sample が入ります。

Custom JSON の場合、Build 開始時点の検証済み Preset を 1 回の Build Transaction 用 Memory Snapshot として固定します。

### 同一 Version の上書き

既存の同一 Version Package に Render / User Payload がある場合は上書きを拒否します。新しい Version を作成するか、既存 Package を明示的に管理してください。

## 7. Blender で連番をレンダー

CutBridge Output へ必要な Pass をレンダーします。AE へ渡す前に Required Pass が期待 Frame Range を満たしていることを確認します。

## 8. After Effects 版 CutBridge を準備

次の 4 Runtime File を同じ Folder に置きます。

- `CutBridge.jsx`
- `revision_manager.js`
- `qc_plus.js`
- `localization.js`

最初は **File > Scripts > Run Script File...** から `CutBridge.jsx` を実行できます。

Dockable Panel として使用する場合は 4 ファイルすべてを `Scripts/ScriptUI Panels` に配置して AE を再起動します。

`localization.js` が欠けている場合は安全に English Fallback へ移行しますが、Build / QC / Revision Safety は弱くなりません。

詳細: [After Effects INSTALL](../apps/after-effects/INSTALL.md)

## 9. AE で Import / Build

1. `cutbridge.json` を読み込みます。
2. Package Identity / FPS / Frame Count / Validation を確認します。
3. Build を実行します。
4. Required Sequence が不足している場合は失敗します。
5. Optional Pass は Manifest 契約に従い Warning / Skip されます。
6. Valid な `handoff_3d` がある場合は、対応範囲の Managed Camera / 3D Null を再構築します。

Same-name の Artist Object は Name だけで CutBridge 管理対象として採用しません。Ownership が曖昧なら Fail-Closed します。

S10C は Geometry / Light / Bone / Arbitrary Hierarchy / General Scene Sync を追加しません。

Native AE 2026 Build 87 の S10C 検証では、テスト Fixture の最大 2D Projection Error は `0.00018066 px`、Gate は `0.05 px` でした。この結果はテスト済み S10C Scope の Evidence であり、全 AE / OS の Certification ではありません。

## 10. QC+

Build 後や Project 変更後に **QC** を実行します。

QC+ は Stable `CBQ-*` Code を使い、Package / Sequence / Comp / Ownership / Revision State、および該当する場合は Managed S10C Camera / Null State を診断します。

QC は診断専用です。Object の自動採用、Import、Move、Retag、Source Replace、自動修復は行いません。

## 11. V002 / V003 などへ Revision

1. 現在の Managed Project を保持する。
2. 新しい Package を Revision Flow から選択する。
3. Compatibility を確認する。
4. Warning Class は明示確認する。
5. 非互換状態は Source Replacement 前に Fail-Closed する。
6. Compatible の場合のみ Verified Managed Source を置換する。
7. Historical Footage は旧 Version Provenance を保持する。
8. 完了後に Build / QC を再実行する。

Preset の Version 表示が `R0012` のように変わっても、Revision Compatibility の基本となる Manifest `version` は数値のままです。

最終 S13F Native Repair では、Adobe After Effects 2026 `26.3x87` / Build 87 上で V001→V002→V003 の Camera / Null Revision Chain が検証されました。この Evidence はテスト済み Host / Scope に限定され、Fail-Closed Compatibility Check を解除するものではありません。

## 12. 日本語／English Safety Boundary

言語変更で変わるのは表示だけです。

次は変わりません。

- Manifest Value
- Package Identity
- Studio Preset Resolution
- `handoff_3d` Data
- Managed Ownership Tag
- `CBQ-*` / `PRESET_*` Code
- Build / QC / Revision Decision
- 無関係な Blender / AE Object

## 13. Release Boundary

v0.2.3 は未リリースです。CI / S12 / S13 PASS だけを理由に Stable / RC を公開しません。

公開前には issue #18 の Repository-Level Release Governance、日本の Target User に対する Claim に適した S14 Evidence、明示的に Freeze した Release Candidate、`main` への意図的 Promotion、Promoted Tree の Authoritative CI、Exact Authorization、実 Tag Release、Downloaded Asset Verification、Production Update / Distribution Verification が必要です。

Canonical Checklist: [RELEASE_READINESS.md](RELEASE_READINESS.md)

## 次の開発フェーズ

S12 / S13 がテスト済み Scope で完了したため、次の限定フェーズは **S14 — Japanese Target-User Validation & Release Preparation** です。

関連資料：

- [HANDOFF_3D.md](HANDOFF_3D.md)
- [STUDIO_PRESETS.md](STUDIO_PRESETS.md)
- [S12_S13_EVIDENCE_SUMMARY.md](S12_S13_EVIDENCE_SUMMARY.md)
- [RELEASE_READINESS.md](RELEASE_READINESS.md)
- [COMPATIBILITY.md](COMPATIBILITY.md)
- [COMPLETION_STATUS.md](COMPLETION_STATUS.md)
- [ROADMAP.md](ROADMAP.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)
- [After Effects INSTALL](../apps/after-effects/INSTALL.md)
