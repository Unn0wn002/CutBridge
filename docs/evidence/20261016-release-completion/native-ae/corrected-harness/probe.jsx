(function () {
    var output = new Folder("C:/Evidence/verification-output/native-ae");
    if (!output.exists && !output.create()) throw Error("Native AE output cannot be created");
    var report = new File(output.fsName + "/availability.json");
    function quote(value) { return '"' + String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n") + '"'; }
    var buildName = "UNAVAILABLE", buildNumber = "UNAVAILABLE";
    try { buildName = String(app.buildName); } catch (_) {}
    try { buildNumber = String(app.buildNumber); } catch (_) {}
    if (!report.open("w")) throw Error("Native AE availability report cannot be written");
    report.write('{"status":"AVAILABLE","host_version":' + quote(app.version) + ',"build_name":' + quote(buildName) + ',"build_number":' + quote(buildNumber) + ',"os":' + quote($.os) + ',"engine":' + quote($.engineName) + ',"temp":' + quote($.getenv("TEMP")) + ',"candidate_execution":"NOT_EXECUTED","native_campaign":"NOT_EXECUTED","license_files":"NOT_MAPPED","scope":"Availability only; no CutBridge runtime loaded"}');
    report.close();
    app.quit();
}());
