/*
 * CutBridge S7 QC+ diagnostic engine.
 *
 * Pure, host-independent diagnostic normalization used by the After Effects panel.
 * The engine never mutates project state and never performs automatic repairs.
 */
(function (root, factory) {
    if (typeof module !== "undefined" && module.exports) {
        module.exports = factory();
    } else {
        if (!root) root = (typeof $ !== "undefined" && $.global) ? $.global : this;
        root.CutBridgeQCPlus = factory();
    }
}(typeof $ !== "undefined" && $.global ? $.global : this, function () {
    "use strict";

    var SEVERITY = {PASS: "PASS", WARNING: "WARNING", ERROR: "ERROR"};
    var SEVERITY_ORDER = {ERROR: 0, WARNING: 1, PASS: 2};
    var SCOPE_ORDER = {
        "package": 0,
        manifest: 1,
        sequence: 2,
        footage: 3,
        layer: 4,
        comp: 5,
        revision: 6,
        host: 7
    };

    function text(value) {
        return value === undefined || value === null ? "" : String(value);
    }

    function clean(value) {
        return text(value).replace(/^\s+|\s+$/g, "");
    }

    function severity(value) {
        value = clean(value).toUpperCase();
        if (!SEVERITY[value]) throw new Error("Unknown QC severity: " + value);
        return value;
    }

    function validCode(value) {
        return /^CBQ-[A-Z0-9]+(?:-[A-Z0-9]+)*$/.test(text(value));
    }

    function diagnostic(spec) {
        if (!spec || typeof spec !== "object") throw new Error("QC diagnostic specification is required.");
        var level = severity(spec.severity);
        var code = clean(spec.code);
        var scope = clean(spec.scope).toLowerCase();
        var message = clean(spec.message);
        var remediation = clean(spec.remediation);
        if (!validCode(code)) throw new Error("QC diagnostic code must be stable CBQ-* identifier: " + code);
        if (!scope) throw new Error("QC diagnostic scope is required for " + code + ".");
        if (!message) throw new Error("QC diagnostic message is required for " + code + ".");
        if (level !== SEVERITY.PASS && !remediation) {
            throw new Error("QC warning/error requires actionable remediation: " + code + ".");
        }
        return {
            severity: level,
            code: code,
            scope: scope,
            subject: clean(spec.subject),
            message: message,
            remediation: remediation,
            detail: clean(spec.detail)
        };
    }

    function rankScope(scope) {
        return Object.prototype.hasOwnProperty.call(SCOPE_ORDER, scope) ? SCOPE_ORDER[scope] : 99;
    }

    function compare(left, right) {
        var a = SEVERITY_ORDER[left.severity], b = SEVERITY_ORDER[right.severity];
        if (a !== b) return a - b;
        a = rankScope(left.scope); b = rankScope(right.scope);
        if (a !== b) return a - b;
        if (left.code < right.code) return -1;
        if (left.code > right.code) return 1;
        if (left.subject < right.subject) return -1;
        if (left.subject > right.subject) return 1;
        if (left.message < right.message) return -1;
        if (left.message > right.message) return 1;
        return 0;
    }

    function normalize(records) {
        if (Object.prototype.toString.call(records) !== "[object Array]") throw new Error("QC records must be an array.");
        var out = [];
        for (var i = 0; i < records.length; i++) out.push(diagnostic(records[i]));
        out.sort(compare);
        return out;
    }

    function summarize(records) {
        records = normalize(records);
        var result = {PASS: 0, WARNING: 0, ERROR: 0, total: records.length};
        for (var i = 0; i < records.length; i++) result[records[i].severity]++;
        result.status = result.ERROR ? "ERROR" : result.WARNING ? "WARNING" : "PASS";
        return result;
    }

    function headline(summary) {
        if (summary.ERROR) return "ERROR — " + summary.ERROR + " error(s), " + summary.WARNING + " warning(s)";
        if (summary.WARNING) return "WARNING — " + summary.WARNING + " warning(s)";
        return "PASS";
    }

    function render(records) {
        records = normalize(records);
        var summary = summarize(records);
        var lines = [];
        for (var i = 0; i < records.length; i++) {
            var item = records[i];
            var line = item.severity + " [" + item.code + "] " +
                (item.subject ? item.subject + ": " : "") + item.message;
            if (item.detail) line += " — " + item.detail;
            if (item.remediation) line += "\n  Next: " + item.remediation;
            lines.push(line);
        }
        return {summary: summary, headline: headline(summary), records: records, text: lines.join("\n")};
    }

    function sequenceRecords(passInfo, manifest, coverage) {
        var out = [], name = passInfo && passInfo.name ? String(passInfo.name) : "UNKNOWN";
        var optional = passInfo && passInfo.required === false;
        var expected = manifest && manifest.frames ? manifest.frames.count : null;
        if (!coverage || coverage.folderExists !== true) {
            out.push(diagnostic({
                severity: optional ? SEVERITY.WARNING : SEVERITY.ERROR,
                code: optional ? "CBQ-SEQ-OPTIONAL-FOLDER-MISSING" : "CBQ-SEQ-REQUIRED-FOLDER-MISSING",
                scope: "sequence",
                subject: name,
                message: optional ? "Optional pass folder is missing." : "Required pass folder is missing.",
                remediation: optional ? "Render this optional pass if the shot needs it, or leave it absent intentionally." : "Render or restore the required pass folder, then run QC again."
            }));
            return out;
        }
        if (coverage.complete !== true) {
            var missing = coverage.missing && coverage.missing.length ? coverage.missing.join(", ") : "unknown";
            out.push(diagnostic({
                severity: optional ? SEVERITY.WARNING : SEVERITY.ERROR,
                code: optional ? "CBQ-SEQ-OPTIONAL-FRAMES-MISSING" : "CBQ-SEQ-REQUIRED-FRAMES-MISSING",
                scope: "sequence",
                subject: name,
                message: "Expected sequence is incomplete.",
                detail: "Missing frame(s): " + missing,
                remediation: optional ? "Re-render the missing optional frames if this pass is needed, then run QC again." : "Re-render or restore the missing required frames, then run QC again."
            }));
        } else {
            out.push(diagnostic({
                severity: SEVERITY.PASS,
                code: "CBQ-SEQ-COMPLETE",
                scope: "sequence",
                subject: name,
                message: expected === null ? "Expected frame sequence is complete." : expected + "/" + expected + " expected frames are present."
            }));
        }
        if (coverage.unexpected && coverage.unexpected.length) {
            out.push(diagnostic({
                severity: SEVERITY.WARNING,
                code: "CBQ-SEQ-UNEXPECTED-MATCHES",
                scope: "sequence",
                subject: name,
                message: coverage.unexpected.length + " unexpected matching filename(s) were found.",
                remediation: "Remove or rename unintended matching files only after confirming they are not artist deliverables; CutBridge will not delete them automatically."
            }));
        }
        return out;
    }

    function compRecords(mismatches) {
        var out = [];
        if (!mismatches || !mismatches.length) {
            out.push(diagnostic({severity: SEVERITY.PASS, code: "CBQ-COMP-SPEC-OK", scope: "comp", message: "Managed comp metadata matches the manifest."}));
            return out;
        }
        for (var i = 0; i < mismatches.length; i++) {
            var token = clean(mismatches[i]).toUpperCase().replace(/[^A-Z0-9]+/g, "-");
            out.push(diagnostic({
                severity: SEVERITY.ERROR,
                code: "CBQ-COMP-DRIFT-" + token,
                scope: "comp",
                message: "Managed comp metadata mismatch: " + mismatches[i] + ".",
                remediation: "Restore the intended managed-comp metadata or deliberately rebuild/migrate the package; QC will not rewrite comp settings automatically."
            }));
        }
        return out;
    }

    function managedObjectRecords(kind, passInfo, observation) {
        kind = clean(kind).toLowerCase();
        if (kind !== "footage" && kind !== "layer") throw new Error("Managed QC kind must be footage or layer.");
        observation = observation || {};
        var status = clean(observation.status).toLowerCase();
        var optional = passInfo && passInfo.required === false;
        var name = passInfo && passInfo.name ? String(passInfo.name) : "UNKNOWN";
        var prefix = kind === "footage" ? "CBQ-FOOTAGE-" : "CBQ-LAYER-";
        var label = kind === "footage" ? "managed footage" : "managed layer";
        if (status === "ok") {
            return [diagnostic({
                severity: SEVERITY.PASS,
                code: prefix + "OK",
                scope: kind,
                subject: name,
                message: label.charAt(0).toUpperCase() + label.slice(1) + " ownership/source matches the manifest."
            })];
        }
        if (status === "missing") {
            return [diagnostic({
                severity: optional ? SEVERITY.WARNING : SEVERITY.ERROR,
                code: prefix + (optional ? "OPTIONAL-MISSING" : "REQUIRED-MISSING"),
                scope: kind,
                subject: name,
                message: (optional ? "optional " : "required ") + label + " is missing.",
                remediation: optional ?
                    "Rebuild this optional pass only if the shot needs it; CutBridge will not synthesize or adopt a replacement automatically." :
                    "Restore/rebuild the required managed object from the trusted package, then run QC again."
            })];
        }
        if (status === "ownership_error") {
            return [diagnostic({
                severity: SEVERITY.ERROR,
                code: prefix + "OWNERSHIP-ERROR",
                scope: kind,
                subject: name,
                message: observation.message || (label.charAt(0).toUpperCase() + label.slice(1) + " ownership cannot be verified."),
                remediation: "Preserve artist work and deliberately resolve the tag/source/container conflict. CutBridge will not adopt, retag, or replace the ambiguous object automatically."
            })];
        }
        throw new Error("Unsupported managed QC observation status: " + status);
    }

    function hostRecords(observation) {
        observation = observation || {};
        var out = [];
        if (observation.inspectable === false) {
            out.push(diagnostic({
                severity: SEVERITY.ERROR,
                code: "CBQ-HOST-STATE-UNINSPECTABLE",
                scope: "host",
                message: "After Effects project state required by QC cannot be inspected safely.",
                remediation: "Use a supported After Effects host/project state and retry QC; CutBridge will not guess ownership when inspection APIs are unavailable."
            }));
        }
        var stale = Number(observation.staleManagedTags || 0);
        if (stale > 0) {
            out.push(diagnostic({
                severity: SEVERITY.ERROR,
                code: "CBQ-HOST-STALE-MANAGED-TAG",
                scope: "host",
                message: stale + " stale or foreign CutBridge-managed tag(s) were found.",
                remediation: "Inspect the tagged objects and deliberately restore or remove stale ownership. CutBridge will not reclaim those objects automatically."
            }));
        }
        if (observation.ownershipAmbiguous === true) {
            out.push(diagnostic({
                severity: SEVERITY.ERROR,
                code: "CBQ-HOST-OWNERSHIP-AMBIGUOUS",
                scope: "host",
                message: observation.message || "Managed ownership is ambiguous.",
                remediation: "Resolve duplicate/conflicting managed objects manually before Build, Revision, or QC continues."
            }));
        }
        if (!out.length) {
            out.push(diagnostic({
                severity: SEVERITY.PASS,
                code: "CBQ-HOST-OWNERSHIP-OK",
                scope: "host",
                message: "Inspectable managed ownership has no stale or ambiguous host-state finding."
            }));
        }
        return out;
    }

    function revisionRecords(assessment, subject) {
        var out = [], i;
        if (!assessment || !assessment.status) {
            out.push(diagnostic({
                severity: SEVERITY.WARNING,
                code: "CBQ-REV-NOT-ASSESSED",
                scope: "revision",
                subject: subject || "",
                message: "Revision compatibility was not assessed.",
                remediation: "Select a candidate CutBridge package and run revision compatibility before replacing managed sources."
            }));
            return out;
        }
        if (assessment.status === "safe") {
            out.push(diagnostic({severity: SEVERITY.PASS, code: "CBQ-REV-SAFE", scope: "revision", subject: subject || "", message: "Revision is compatible with source-only replacement."}));
        } else if (assessment.status === "warning") {
            var warnings = assessment.warnings && assessment.warnings.length ? assessment.warnings : ["Revision requires explicit confirmation."];
            for (i = 0; i < warnings.length; i++) out.push(diagnostic({
                severity: SEVERITY.WARNING,
                code: "CBQ-REV-POLICY-WARNING",
                scope: "revision",
                subject: subject || "",
                message: warnings[i],
                remediation: "Review the revision policy change and continue only through CutBridge's explicit revision confirmation flow."
            }));
        } else {
            var reasons = assessment.reasons && assessment.reasons.length ? assessment.reasons : ["Revision is incompatible."];
            for (i = 0; i < reasons.length; i++) out.push(diagnostic({
                severity: SEVERITY.ERROR,
                code: "CBQ-REV-INCOMPATIBLE",
                scope: "revision",
                subject: subject || "",
                message: reasons[i],
                remediation: "Do not source-swap this candidate. Rebuild or deliberately migrate the composition after resolving the incompatible package change."
            }));
        }
        return out;
    }

    return {
        SEVERITY: SEVERITY,
        diagnostic: diagnostic,
        normalize: normalize,
        summarize: summarize,
        render: render,
        sequenceRecords: sequenceRecords,
        compRecords: compRecords,
        managedObjectRecords: managedObjectRecords,
        hostRecords: hostRecords,
        revisionRecords: revisionRecords
    };
}));
