# CutBridge クイックスタート（日本語）

このガイドは、**S8 まで統合済みの v0.2.3 未リリース版 `develop`** を対象にしています。

CutBridge は Blender のアニメーションカットを After Effects へ受け渡すための制作パイプラインツールです。カット情報、レンダーパス、バージョン、`cutbridge.json`、AE 側の管理対象コンポ／フッテージ／レイヤー、QC、互換性のある差し替えを一貫したルールで扱います。

基本フロー：

`Blender で情報入力 → Validate Cut → レンダー出力設定／パッケージ作成 → 連番レンダー → AE で読み込み／Build → QC+ → 互換性のある差し替え`

英語版: [QUICK_START.md](QUICK_START.md)

## 現在の開発状態

S1〜S8 は `develop` に統合済みです。S8 のマージコミットは `368b977582feadc26543825b4d31ffd5f6266a4f`、マージ後 CI `34380737455` は PASS しています。

S8 の実機確認もマージ前に PASS しています。

- Blender 5.2.1 LTS
- Adobe After Effects 2026 v26.3.0 Build 87

ただし、これは開発検証の証拠であり、安定版リリースの許可ではありません。現在 GitHub Release / リリースタグは存在せず、`release-authorization.json` は意図的に未承認のままです。

## 1. Blender 版 CutBridge をインストール

開発テストでは、検証対象の正確なソースから作成した CutBridge Blender ZIP を使用してください。

1. 対応 Blender を起動します。宣言上の最小バージョンは 4.2.0、現在の主要な自動実行テストは Blender 5.2.1 LTS です。
2. Preferences から **Install from Disk** など、その Blender バージョンに対応した拡張機能インストール操作を使用します。
3. CutBridge ZIP を選択して有効化します。
4. 3D View の `N` サイドバーを開き、**CutBridge** タブを選択します。
5. 日本語が基本表示です。必要に応じて UI Language から English に切り替えられます。

最小バージョンを満たすだけでは「正式対応済み／認証済み」という意味にはなりません。詳細は [COMPATIBILITY.md](COMPATIBILITY.md) を参照してください。

## 2. Blender でカット情報を準備

Validate Cut の前に次を確認します。

1. `.blend` ファイルを保存する。
2. Scene Camera を設定する。
3. FPS と解像度を設定する。
4. 書き出しフレーム範囲を設定する。
5. Project / Episode / Scene / Cut / Take / Version を入力する。
6. Package Output を選択する。
7. 必要な BEAUTY / LINE / SHADOW / DEPTH パスを選択する。

### フレーム範囲のルール

CutBridge の書き出し開始フレームは `0` 以上です。負のフレーム／プリロールは Blender、スキーマ、AE の各境界で拒否されます。

CutBridge はアニメーションを勝手に番号変更しません。必要な場合は、パッケージ作成前に書き出し範囲を 0 以降へリベースしてください。

## 3. Validate Cut

**Validate Cut** を実行します。

主な確認項目：

- 必須 ID
- Active Camera
- FPS
- Resolution
- Frame Range
- Render Pass
- Package Output
- Renderer / View Layer の対応状態
- 既存パッケージへの安全性

`ERROR` は処理停止条件です。Warning は内容を確認してから進んでください。

JA / EN を切り替えても、検証ロジックや機械用識別子は変化しません。

## 4. レンダー出力マッピング

CutBridge は選択された論理パス用に決定的な Blender compositor 出力を設定します。

安全ルール：

- CutBridge 管理ノードは `CUTBRIDGE_` 名前空間を使用します。
- ユーザー／アーティストが作成した無関係なノードは保持します。
- 設定の置換はトランザクションとして扱います。
- Renderer / View Layer で利用できないパスを架空の出力として作りません。
- 新しい設定に失敗した場合、以前の正常な CutBridge マッピングを壊さないことが前提です。

## 5. Build Package

Validate が成功したら **Build Package** を実行します。

例：

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

選択したパスだけがパッケージ対象になります。実際の連番ファイル名ルールは `cutbridge.json` に記録されます。

### 同一 Version の上書きについて

既存の同一 Version パッケージにレンダー結果やユーザーデータが存在する場合、CutBridge は安全のため上書きを拒否します。

V002 / V003 など新しい Version を作成するか、古いパッケージを明示的に手動管理してください。

## 6. Blender で連番をレンダー

CutBridge が設定した出力先へ必要なパスをレンダーします。

AE に渡す前に、必須パスの連番が期待フレーム範囲を満たしていることを確認してください。

## 7. After Effects 版 CutBridge を準備

S8 の開発パッケージでは、次の **4 ファイルを同じフォルダに置きます**。

- `CutBridge.jsx`
- `revision_manager.js`
- `qc_plus.js`
- `localization.js`

最初の確認方法：

1. After Effects の **File > Scripts > Run Script File...** を開く。
2. `CutBridge.jsx` を選択する。
3. CutBridge パネルが開くことを確認する。
4. 日本語表示と English 切り替えを確認する。

Dockable Panel として使う場合は、4 ファイルすべてを該当バージョンの `Scripts/ScriptUI Panels` へ配置して AE を再起動します。

`localization.js` が欠けている／壊れている場合、UI は安全に English fallback へ移行する必要があります。ただし Build / QC / Revision の安全判定は弱くなりません。

## 8. AE でパッケージを読み込み、Build

1. CutBridge から `cutbridge.json` を読み込みます。
2. Package Identity / FPS / Frame Count / Validation を確認します。
3. Build を実行して CutBridge 管理コンポ／フォルダ／フッテージ／レイヤーを作成します。
4. 必須連番が不足している場合は Build を成功扱いにしません。
5. Optional Pass が利用できない場合は、契約上の Warning / Skip ルールに従います。

CutBridge は「名前が似ている」「Source が似ている」だけのアーティストオブジェクトを自動的に管理対象へ取り込みません。

## 9. QC+

Build 後、またはプロジェクト状態を変更した後に **QC** を実行します。

S7 QC+ は安定した `CBQ-*` コードと PASS / WARNING / ERROR を使用します。

主なチェック：

- Package / Manifest
- 必須／Optional 連番
- Missing / Unexpected Frame
- Comp Resolution / Pixel Aspect / FPS / Duration
- Managed Footage / Layer Ownership
- Stale / Foreign / Ambiguous Managed State
- Revision Compatibility

QC は診断専用です。QC 自体がオブジェクトの採用、読み込み、移動、再タグ付け、Source 差し替え、自動修復を行う設計にはしません。

## 10. V002 / V003 へ差し替え

新しい互換パッケージへ更新する場合：

1. 現在の管理対象プロジェクトを保持します。
2. Revision フローから新しいパッケージを選択します。
3. Compatibility 診断を確認します。
4. Warning クラスの変更は明示確認が必要です。
5. Geometry / Pass Set / Ownership / Package Structure が非互換の場合は Source 差し替え前に停止します。
6. 互換性がある場合のみ、検証済みの CutBridge 管理 Source を置換します。
7. 旧 Version の管理フッテージは履歴由来情報を保持します。
8. 完了後に Build / QC を再実行します。

CutBridge は互換性を作るために既存コンポを勝手にリサイズ／リタイムしません。

## 11. 日本語／English の安全境界

言語変更で変わってよいものはユーザー表示だけです。

次は変えてはいけません。

- Manifest 値
- Package Identity
- Managed Tag / Ownership
- `CBQ-*` コード
- Build / QC / Revision の判定
- 無関係な Blender Scene / AE Project オブジェクト

## 12. リリース境界

現在の v0.2.3 は未リリースです。

CI PASS や S8 実機 PASS だけを理由に Stable / RC を公開しないでください。

RC / Stable の前には少なくとも以下が必要です。

- issue #18 の repository-level release governance
- 検証済み候補を `main` へ意図的に promotion
- exact main/tag/channel/prerelease の明示 authorization
- 実際の tag-triggered release
- 公開 ZIP / checksum / metadata の再検証
- production update index の確認
- リリース主張に必要な End-to-End / Target User validation

## 次の開発フェーズ

S8.5 ドキュメント整合が `develop` に統合され、マージ後 CI が PASS した後の次フェーズは **S9 — Studio Presets** です。

関連資料：

- [COMPLETION_STATUS.md](COMPLETION_STATUS.md)
- [ROADMAP.md](ROADMAP.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md)
- [After Effects INSTALL](../apps/after-effects/INSTALL.md)
