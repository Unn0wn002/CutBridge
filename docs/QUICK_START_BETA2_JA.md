# CutBridge v0.2.3-beta.2 ユーザビリティ・クイックスタート

状態: **修正候補向けガイド。リリース済みという意味ではありません。**

このガイドは、次のソース変更候補に向けて整備しているユーザビリティ契約を説明します。リリースガバナンス、ホスト互換性の実機証拠、S14日本語ターゲットユーザー検証の代わりにはなりません。

English: [QUICK_START_BETA2.md](QUICK_START_BETA2.md)

## 基本フロー

`カット準備 → カットを検証 → ERRORを修正 / WARNINGを確認 → パッケージ作成 → 連番レンダー → AEでパッケージ読込 → Build → QC+ → 改訂時はVersionを上げる`

## Blenderのレンダーパス

### Beauty

通常のCombined/Imageレンダーで、メイン映像の連番です。After Effectsで主要なレンダー画像が必要な場合に有効にします。

### Line

Blender Freestyleによる線画パスです。Lineには次が必要です。

1. Scene/レンダー設定でFreestyleが有効;
2. 現在のView LayerでFreestyleが有効;
3. Freestyleの **As Render Pass** が有効;
4. 現在のRender Layersノードに実際の `Freestyle` 出力が存在する。

いずれかが不足している場合、**Build Packageより前にValidate CutがERRORを返します**。Lineを有効にしたまま安全に続行することはできません。Freestyleを正しく設定するか、Lineを無効にしてください。

### Shadow

レンダーエンジンに依存する単独のShadowパスです。Blender 5.2では、現在のCutBridge Shadow契約はEEVEEのShadow Render Layers出力を対象に検証します。Cyclesは、この契約で必要な同じ単独Shadow出力を提供しません。

Shadowが選択されていて、現在のレンダーエンジン/View Layerが必要な出力を提供できない場合、**Build Packageより前にValidate CutがERRORを返します**。対応するレンダー/View Layer設定へ変更するか、Shadowを無効にしてください。

### Depth

深度ベースのコンポジットやエフェクトに使うカメラ距離データです。

- **OpenEXR:** 正確なDepth値が必要な場合の推奨形式。
- **PNG/TIFF:** 続行はできますが、精度低下の可能性があるためWARNINGを表示します。

Depth形式の警告はエラーではありません。

## 4パス同時ワークフロー

要求されている `Beauty + Line + Shadow + Depth` の同時構成は、Line/Freestyle要件を満たす **EEVEE** について、現在のBlender 5.2.1自動マッピング検証で確認対象になっています。

回帰テストでは、Beautyのみ、Beauty+Line、Beauty+Shadow、Depth PNG、Depth OpenEXR、Beauty+Line+Shadowも確認します。

正確な自動検証範囲は [FOUR_PASS_WORKFLOW_BETA2.md](FOUR_PASS_WORKFLOW_BETA2.md) を参照してください。

## 連番形式

v0.2.3のmanifest/preset構成では、パッケージ単位で1つのSequence Formatを使用します。現在は選択した形式が **有効な全パス** に適用されます。

パスごとの形式指定は、この修正候補では中途半端に実装しません。Studio Preset、Blenderコンポジター出力、manifest、パッケージ整合性、AE連番読込、過去データ互換性に同時に影響するため、後方互換性を含む別設計として追跡します。

## スタジオプリセット

Studio Presetは、命名、フォルダー、パス選択、連番形式、バージョン表記、AEコンポ名などを制御できる宣言的データプロファイルです。

- **Manual:** パスとSequence Formatを直接編集できます。
- **Preset管理モード:** 決定的なパッケージ識別を維持するため、管理対象値は読み取り専用になります。

Custom PresetはBuild Packageの前に検証を通す必要があります。

## Validate Cut と Build Package

### Validate Cut

重要な診断は次の4点を伝えます。

- **何が起きたか**
- **なぜ起きたか**
- **続行できるか**
- **どう直すか**

重要度の契約:

- **INFO:** 情報のみ。必ずしも操作は不要。
- **WARNING:** 影響を理解したうえで続行可能。
- **ERROR:** 修正するまで安全に続行できない。

安定した技術コードはサポート/デバッグ用として残しますが、ユーザーが最初に解読しなければならない文章にはしません。

Validate Cutは事前検証のみで、パッケージを作成しません。

### Build Package

Buildは、事前検証に合格した後でCutBridge管理のコンポジター出力と決定的なVersion付きパッケージを作成します。

多層防御として、検証後にホスト状態が変わった場合や事前検証が迂回された場合でも、Build側のRender Layersソケット確認がパッケージフォルダー作成前にfail-closedします。

アーティスト所有のコンポジター状態は保持する必要があります。CutBridgeが管理するのはCutBridge管理のマッピング領域だけです。

### パッケージ作成後: レンダリング可能状態

現在のパッケージにレンダー/ユーザーデータが入った後も、**Build Packageは同じVersionを上書きしないよう保護されます**。この保護は「パッケージ作成」に対するもので、Blenderの「アニメーションをレンダリング」自体を停止するものではありません。

既存の `cutbridge.json` が現在のカット/レンダー契約と一致している場合、通常の検証ステータスは **「パッケージ作成済み — レンダリング可能」** (`PACKAGE_RENDER_READY`) を表示します。そのままアニメーションをレンダリングし、同じVersionでBuild Packageを再実行しないでください。

既存パッケージにデータがある一方で、現在の設定がmanifestと一致しない場合は `PACKAGE_STATE_MISMATCH` を表示します。元の設定へ戻すかVersionを上げてから新しい出力を作成してください。設定の異なる出力を既存リビジョンへ混在させないでください。

## Version運用

`Version` はパッケージの改訂番号です。

- 初回ハンドオフ: V001;
- 次の改訂: V002;
- その次: V003。

既存の同一Versionパッケージにレンダー/ユーザーデータがある場合、上書きしないでください。新しい改訂ではVersionを上げ、過去のパッケージと共存させます。同じVersionがすでに作成済みで現在の設定と一致している場合は、パッケージを再作成せず、そのままレンダリングを続けます。

## パッケージ出力先

Package Outputは、Version付きCutBridgeパッケージを作成する親ディレクトリです。

Blenderの `//` は保存済み `.blend` ファイルからの相対パスです。相対出力を使う前に `.blend` を保存してください。

CutBridgeはBuild前に出力先を検証し、保護すべき同一Versionデータ、安全でない出力先、衝突がある場合はfail-closedします。

## Camera / 3Dハンドオフ

Blender Sceneのアクティブカメラはカットの必須メタデータです。

既存のproducer-side Camera/3Dサンプルデータ経路は **実験的で、通常のBlenderパネルでは意図的にリリース向け機能として表示していません**。正確な候補ソースでAE Camera/3D Nullワークフローのネイティブ検証が完了するまで、一般的なBlender↔AEシーン同期機能として扱わないでください。

## After Effectsパネル

`CutBridge.jsx` は現在、次の両方に対応する構造です。

- `Scripts/ScriptUI Panels` に配置した場合のドッキング可能なScriptUI Panel;
- スクリプトとして実行した場合のpalette/undocked実行。

パネルを開くだけではCutBridge管理のプロジェクト状態を作成・変更しません。明示的なユーザー操作が必要です。

現在の操作:

- **Load Package:** `cutbridge.json` を選択/読込し、パッケージ状態を更新。
- **Build:** manifestに従い、検証済みCutBridge管理のフォルダー、フッテージ、コンポ、レイヤーのみを作成/再利用。
- **QC+:** パッケージ/プロジェクト状態を検査し、所有状態を勝手に修復せず決定的な診断を報告。
- **Revision:** 検証済み管理状態に対して、互換性のあるsource-oriented改訂のみを適用。

CutBridge管理オブジェクトはCutBridge所有メタデータで識別します。名前やソースが似ているだけのアーティスト所有オブジェクトを自動採用してはいけません。

AEパネルの視覚階層/contextual help改善はbeta.2修正キャンペーンの未完了項目であり、サポート表現を変更する前に実機ホストで再検証する必要があります。

## 互換性境界

このガイドだけからホスト互換性を推定しないでください。

Blender 4.2/4.5/5.2およびAE 2020–2026の必要検証は [COMPATIBILITY_CAMPAIGN_BETA2.md](COMPATIBILITY_CAMPAIGN_BETA2.md) を参照してください。古いAEバージョンは実機証拠が得られるまで未検証です。

## リリース境界

この修正作業はv0.2.3公開を承認しません。手順は引き続き次の通りです。

`S14 PASS → governance解決 → exact RC freeze → exact RC CI → deliberate main promotion → promoted-main CI → exact authorization tuple → publication → independent artifact verification → distribution/update verification`

これらのゲートが実際に完了するまでは、CutBridgeは **NOT RELEASE READY** です。