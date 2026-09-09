(function (root, factory) {
    var api = factory();
    if (typeof module !== "undefined" && module.exports) module.exports = api;
    else root.CutBridgeLocalization = api;
}(typeof $ !== "undefined" && $.global ? $.global : this, function () {
    "use strict";

    var DEFAULT_LOCALE = "JA";
    var FALLBACK_LOCALE = "EN";
    var currentLocale = DEFAULT_LOCALE;

    var STRINGS = {
        EN: {
            language_label: "UI Language",
            no_package: "No package loaded",
            import_package: "1. Import Package",
            build_comp: "2. Build Comp",
            run_qc: "3. Run QC",
            update_revision: "4. Update Revision",
            workflow_note: "v{version}: validated package -> idempotent comp -> QC",
            package_status: "{name} | {fps}fps | {frames}f",
            choose_manifest: "Choose CutBridge cutbridge.json",
            choose_revision: "Choose newer CutBridge cutbridge.json",
            revision_file_required: "Choose the cutbridge.json file from the newer package.",
            revision_blocked: "Revision blocked:",
            revision_confirm: "Update CutBridge revision to V{version}?",
            warnings: "Warnings:",
            revision_scope: "Only verified CutBridge-managed sources and metadata will be changed.",
            revision_updated: "CutBridge: revision updated to V{version}.",
            revision_preserved: "Managed layer properties and artist layers were preserved.",
            confirmation_unavailable: "After Effects confirmation UI is unavailable; revision was not applied.",
            comp_built: "CutBridge: comp built",
            comp_reused: "CutBridge: comp reused safely",
            rollback_created: "Newly created managed objects were rolled back.",
            error_intro: "CutBridge Error",
            qc_pass: "PASS",
            qc_warning: "WARNING",
            qc_error: "ERROR",
            next_prefix: "Next: "
        },
        JA: {
            language_label: "表示言語",
            no_package: "パッケージ未読み込み",
            import_package: "1. パッケージ読み込み",
            build_comp: "2. コンポ作成",
            run_qc: "3. QC実行",
            update_revision: "4. 差し替え",
            workflow_note: "v{version}: 検証済みパッケージ -> 安全なコンポ作成 -> QC",
            package_status: "{name} | {fps}fps | {frames}フレーム",
            choose_manifest: "CutBridgeのcutbridge.jsonを選択",
            choose_revision: "新しいCutBridgeパッケージのcutbridge.jsonを選択",
            revision_file_required: "新しいパッケージのcutbridge.jsonを選択してください。",
            revision_blocked: "差し替えを実行できません:",
            revision_confirm: "CutBridgeをV{version}へ差し替えますか？",
            warnings: "警告:",
            revision_scope: "検証済みのCutBridge管理ソースとメタデータのみ変更します。",
            revision_updated: "CutBridge: V{version}へ差し替えました。",
            revision_preserved: "管理レイヤーのプロパティと作業用レイヤーは保持されました。",
            confirmation_unavailable: "After Effectsの確認ダイアログを使用できないため、差し替えは実行されませんでした。",
            comp_built: "CutBridge: コンポを作成しました",
            comp_reused: "CutBridge: コンポを安全に再利用しました",
            rollback_created: "新しく作成した管理オブジェクトをロールバックしました。",
            error_intro: "CutBridge エラー",
            qc_pass: "合格 / PASS",
            qc_warning: "警告 / WARNING",
            qc_error: "エラー / ERROR",
            next_prefix: "対処 / Next: "
        }
    };

    var QC_JA = {
        "CBQ-PACKAGE-IDENTITY-OK": ["パッケージIDとマニフェスト名は有効です。", ""],
        "CBQ-MANIFEST-SCHEMA-OK": ["マニフェスト形式はCutBridgeでサポートされています。", ""],
        "CBQ-MANIFEST-FPS-OK": ["FPS設定は有効です。", ""],
        "CBQ-MANIFEST-FRAMES-OK": ["フレーム数は整合しています。", ""],
        "CBQ-MANIFEST-RESOLUTION-OK": ["解像度設定は有効です。", ""],
        "CBQ-MANIFEST-CONTRACT-ERROR": ["マニフェスト契約に問題があります。", "信頼できるBlenderパッケージからcutbridge.jsonを修正または再生成してください。"],
        "CBQ-SEQ-COMPLETE": ["連番フレームはそろっています。", ""],
        "CBQ-SEQ-REQUIRED-FOLDER-MISSING": ["必須レンダーパスのフォルダーがありません。", "必須パスをレンダーまたは復元してからQCを再実行してください。"],
        "CBQ-SEQ-OPTIONAL-FOLDER-MISSING": ["任意レンダーパスのフォルダーがありません。", "必要な場合のみ任意パスをレンダーし、プレースホルダーは作成しないでください。"],
        "CBQ-SEQ-REQUIRED-FRAMES-MISSING": ["必須レンダーパスのフレームが不足しています。", "不足フレームを再レンダーまたは復元してからQCを再実行してください。"],
        "CBQ-SEQ-OPTIONAL-FRAMES-MISSING": ["任意レンダーパスのフレームが不足しています。", "必要な場合のみ不足フレームをレンダーしてください。"],
        "CBQ-SEQ-UNEXPECTED-MATCHES": ["連番フォルダーに想定外の一致ファイルがあります。", "ファイル名と連番パターンを確認してください。"],
        "CBQ-SEQ-INSPECTION-ERROR": ["連番の検査に失敗しました。", "パス、エイリアス、ファイル名を確認してください。"],
        "CBQ-FOOTAGE-OK": ["管理フッテージの所有権とソースは正常です。", ""],
        "CBQ-FOOTAGE-REQUIRED-MISSING": ["必須の管理フッテージがありません。", "信頼できるパッケージから意図的に再構築してください。"],
        "CBQ-FOOTAGE-OPTIONAL-MISSING": ["任意の管理フッテージがありません。", "必要な場合のみ任意パスを再構築してください。"],
        "CBQ-FOOTAGE-OWNERSHIP-ERROR": ["管理フッテージの所有権を確認できません。", "タグ、ソース、配置を確認し、自動採用せずに競合を解消してください。"],
        "CBQ-LAYER-OK": ["管理レイヤーの所有権とソースは正常です。", ""],
        "CBQ-LAYER-REQUIRED-MISSING": ["必須の管理レイヤーがありません。", "管理レイヤーを意図的に復元または再構築してください。"],
        "CBQ-LAYER-OPTIONAL-MISSING": ["任意の管理レイヤーがありません。", "必要な場合のみ任意レイヤーを再構築してください。"],
        "CBQ-LAYER-OWNERSHIP-ERROR": ["管理レイヤーの所有権を確認できません。", "アーティスト作業を保持したままタグ、ソース、配置の競合を解消してください。"],
        "CBQ-COMP-SPEC-OK": ["管理コンポの設定はマニフェストと一致しています。", ""],
        "CBQ-COMP-DRIFT-RESOLUTION": ["管理コンポの解像度がマニフェストと一致しません。", "意図した設定へ戻すか、意図的に再構築/移行してください。"],
        "CBQ-COMP-DRIFT-PIXEL-ASPECT": ["管理コンポのピクセル縦横比がマニフェストと一致しません。", "意図した設定へ戻すか、意図的に再構築/移行してください。"],
        "CBQ-COMP-DRIFT-FRAME-RATE": ["管理コンポのフレームレートがマニフェストと一致しません。", "意図した設定へ戻すか、意図的に再構築/移行してください。"],
        "CBQ-COMP-DRIFT-DURATION": ["管理コンポの尺がマニフェストと一致しません。", "意図した設定へ戻すか、意図的に再構築/移行してください。"],
        "CBQ-COMP-OWNERSHIP-ERROR": ["管理コンポの所有権を確認できません。", "コンポ/フォルダーの配置と管理タグを確認してください。"],
        "CBQ-COMP-FOLDER-MISSING": ["管理コンポ用フォルダーがありません。", "信頼できるCutBridge構造を意図的に復元してください。"],
        "CBQ-COMP-MISSING": ["管理コンポがありません。", "信頼できるCutBridgeコンポを意図的に再構築してください。"],
        "CBQ-HOST-STATE-UNINSPECTABLE": ["After Effectsの管理状態を完全に検査できません。", "管理状態を確認できるプロジェクト状態でQCを再実行してください。"],
        "CBQ-HOST-STALE-MANAGED-TAG": ["古い、または別パッケージの管理タグがあります。", "自動で付け替えず、対象を確認して意図的に復元または解除してください。"],
        "CBQ-HOST-OWNERSHIP-AMBIGUOUS": ["管理オブジェクトの所有権が重複または曖昧です。", "Build/差し替え/QCを続ける前に重複や競合を解消してください。"],
        "CBQ-HOST-OWNERSHIP-OK": ["管理オブジェクトの所有権に競合はありません。", ""],
        "CBQ-REV-SAFE": ["差し替え互換性は安全です。", ""],
        "CBQ-REV-POLICY-WARNING": ["差し替えには確認が必要な警告があります。", "内容を確認し、意図した差し替えの場合のみ続行してください。"],
        "CBQ-REV-INCOMPATIBLE": ["この差し替えは互換性がありません。", "ソース差し替えを行わず、意図的に再構築または移行してください。"],
        "CBQ-REV-NOT-ASSESSED": ["差し替え互換性は未評価です。", "必要な場合は差し替え評価を実行してください。"]
    };

    function own(obj, key) { return Object.prototype.hasOwnProperty.call(obj, key); }

    function normalizeLocale(locale) {
        var value = String(locale || "").toUpperCase();
        return value === "JA" || value === "EN" ? value : FALLBACK_LOCALE;
    }

    function formatTemplate(template, values) {
        var text = String(template == null ? "" : template), key, re;
        values = values || {};
        for (key in values) {
            if (!own(values, key)) continue;
            re = new RegExp("\\{" + key + "\\}", "g");
            text = text.replace(re, String(values[key]));
        }
        return text;
    }

    function tr(locale, key, values) {
        var lang = normalizeLocale(locale), table = STRINGS[lang] || STRINGS.EN;
        var template = own(table, key) ? table[key] : (own(STRINGS.EN, key) ? STRINGS.EN[key] : key);
        return formatTemplate(template, values);
    }

    function setLocale(locale) {
        currentLocale = normalizeLocale(locale);
        return currentLocale;
    }

    function getLocale() { return currentLocale; }

    function formatError(locale, canonicalEnglish) {
        var lang = normalizeLocale(locale), detail = String(canonicalEnglish == null ? "" : canonicalEnglish);
        if (lang !== "JA") return "CutBridge\n\n" + detail;
        return tr(lang, "error_intro") + "\n\n[EN] " + detail;
    }

    function localizeRevisionReason(locale, reason) {
        var lang = normalizeLocale(locale), text = String(reason == null ? "" : reason), ja = "";
        if (lang !== "JA") return text;
        if (text === "FPS changes are unsupported.") ja = "FPSの変更には対応していません。";
        else if (text === "Resolution changes are unsupported.") ja = "解像度の変更には対応していません。";
        else if (text === "Pixel aspect changes are unsupported.") ja = "ピクセル縦横比の変更には対応していません。";
        else if (text === "Duration changes are unsupported.") ja = "尺の変更には対応していません。";
        else if (text.indexOf("Previously required pass missing: ") === 0) ja = "以前必須だったレンダーパスがありません: " + text.substring("Previously required pass missing: ".length);
        else if (text.indexOf("Adding passes is unsupported by source-only revision: ") === 0) ja = "ソース差し替えだけではレンダーパスを追加できません: " + text.substring("Adding passes is unsupported by source-only revision: ".length);
        else if (text.indexOf("Removing an optional pass is unsupported by source-only revision: ") === 0) ja = "ソース差し替えだけでは任意レンダーパスを削除できません: " + text.substring("Removing an optional pass is unsupported by source-only revision: ".length);
        if (!ja) return text;
        return ja + " [EN] " + text;
    }

    function formatRevisionBlocked(locale, reasons) {
        var lang = normalizeLocale(locale), lines = [tr(lang, "revision_blocked")], i;
        for (i = 0; reasons && i < reasons.length; i++) lines.push("- " + localizeRevisionReason(lang, reasons[i]));
        return lines.join("\n");
    }

    function localizeDiagnostic(locale, record) {
        var lang = normalizeLocale(locale), copy = {}, key, translated;
        for (key in record) if (own(record, key)) copy[key] = record[key];
        if (lang !== "JA") return copy;
        translated = QC_JA[String(record.code || "")];
        if (!translated) return copy;
        if (translated[0]) copy.message = translated[0] + (record.message ? " [EN] " + record.message : "");
        if (translated[1]) copy.remediation = translated[1] + (record.remediation ? " [EN] " + record.remediation : "");
        else if (record.remediation) copy.remediation = record.remediation;
        return copy;
    }

    function localizeRecords(locale, records) {
        var out = [], i;
        for (i = 0; records && i < records.length; i++) out.push(localizeDiagnostic(locale, records[i]));
        return out;
    }

    function qcHeadline(locale, headline) {
        var value = String(headline || "").toUpperCase();
        if (value === "PASS") return tr(locale, "qc_pass");
        if (value === "WARNING") return tr(locale, "qc_warning");
        if (value === "ERROR") return tr(locale, "qc_error");
        return headline;
    }

    function localizeRenderedQC(locale, text) {
        if (normalizeLocale(locale) !== "JA") return String(text || "");
        return String(text || "").replace(/\nNext: /g, "\n" + tr("JA", "next_prefix"));
    }

    return {
        DEFAULT_LOCALE: DEFAULT_LOCALE,
        FALLBACK_LOCALE: FALLBACK_LOCALE,
        normalizeLocale: normalizeLocale,
        tr: tr,
        setLocale: setLocale,
        getLocale: getLocale,
        formatError: formatError,
        localizeRevisionReason: localizeRevisionReason,
        formatRevisionBlocked: formatRevisionBlocked,
        localizeDiagnostic: localizeDiagnostic,
        localizeRecords: localizeRecords,
        qcHeadline: qcHeadline,
        localizeRenderedQC: localizeRenderedQC
    };
}));
