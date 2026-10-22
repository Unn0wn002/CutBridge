(function () {
    var output='C:/Evidence/verification-output/native-ae', phases=['campaign','negative','rollback','reopen'];
    function record(value){var f=new File(output+'/all-status.json');f.encoding='UTF-8';if(!f.open('w'))throw Error('Cannot write phase checkpoint');f.write(value);f.close();}
    function quote(s){return '"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n')+'"';}
    var results=[],failed=false;
    record('{"status":"IN_PROGRESS","scope":"Scripted native phases only; no S14B or GUI installer claim"}');
    try{
        for(var i=0;i<phases.length;i++){
            var previous=Window.find('palette','CutBridge');if(previous)previous.close();
            $.evalFile(new File('C:/NativeAEInput/'+phases[i]+'.jsx'));
            results.push('{"phase":'+quote(phases[i])+',"status":'+quote(CB.report.status)+'}');
            if(CB.report.status!=='PASS')failed=true;
            record('{"status":"IN_PROGRESS","phases":['+results.join(',')+']}');
        }
        record('{"status":'+quote(failed?'INSUFFICIENT EVIDENCE':'PASS')+',"phases":['+results.join(',')+'],"normal_quit_requested":true}');
    }catch(error){record('{"status":"INSUFFICIENT EVIDENCE","error":'+quote(error)+',"phases":['+results.join(',')+']}');}
    try{if(app.project)app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);}catch(_){}
    app.quit();
}());
