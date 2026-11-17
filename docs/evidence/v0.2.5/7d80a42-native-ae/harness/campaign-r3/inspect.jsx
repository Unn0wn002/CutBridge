$.evalFile(new File('C:/CutBridgeCampaignR3/common.jsx'));
$.evalFile(new File('C:/CutBridgeInputsR2/ae/CutBridge.jsx'));
var cbMatch=cbComp().comment.match(/_V00([123])/);if(!cbMatch)throw Error('Version ownership unavailable');
CutBridgeContract.loadManifest('C:/CutBridgeInputsR2/\u30d1\u30c3\u30b1\u30fc\u30b8/Native025_EP01_SC010_C001_T01_V00'+cbMatch[1]+'/cutbridge.json');
CutBridgeContract.getState().comp=cbComp();
var cbS=CutBridgeContract.getState(),cbV=cbS.manifest.version,cbR={status:'IN_PROGRESS',version:cbV,host:app.version,temp:$.getenv('TEMP')};
try{cbR.layers=cbSnapshot();cbR.handoff=cbHandoff(cbS.manifest);cbR.qc=CutBridgeContract.runQC();cbR.status='PASS';for(var cbI=0;cbI<cbR.handoff.length;cbI++)if(!cbR.handoff[cbI].passed)cbR.status='FAIL';if(cbR.qc.report.summary.ERROR)cbR.status='FAIL';app.project.save(new File('C:/CutBridgeEvidence/r2/native025-artist-V00'+cbV+'.aep'));}catch(cbE){cbR.status='FAIL';cbR.error=String(cbE);}cbSave('revision-V00'+cbV,cbR);


