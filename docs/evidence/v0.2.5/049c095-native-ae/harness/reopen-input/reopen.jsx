$.evalFile(new File('C:/CutBridgeZipNative/common.jsx'));
var cbR={status:'IN_PROGRESS',host:app.version,temp:$.getenv('TEMP')};
try{
if(!app.project.file||app.project.file.fsName.indexOf('C:\\CutBridgeValidityEvidence\\')!==0)throw Error('Unexpected test project');
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.open(new File('C:/CutBridgeValidityEvidence/native025-artist-V003.aep'));
$.evalFile(new File('C:/CutBridgeZipNative/ae/CutBridge.jsx'));
CutBridgeContract.loadManifest('C:/CutBridgeInputsR2/\u30d1\u30c3\u30b1\u30fc\u30b8/Native025_EP01_SC010_C001_T01_V003/cutbridge.json');
CutBridgeContract.getState().comp=cbComp();cbR.before=cbSnapshot();cbR.handoff=cbHandoff(CutBridgeContract.getState().manifest);
var cbBuild=CutBridgeContract.buildComp();cbR.buildSuccess=cbBuild.success;cbR.after=cbSnapshot();cbR.qc=CutBridgeContract.runQC();
cbR.status=cbBuild.success&&!cbR.qc.report.summary.ERROR&&cbJson(cbR.before)===cbJson(cbR.after)?'PASS':'FAIL';
app.project.save(new File('C:/CutBridgeValidityEvidence/native025-reopened.aep'));
}catch(cbE){cbR.status='FAIL';cbR.error=String(cbE);}cbSave('same-process-save-close-reopen',cbR);


