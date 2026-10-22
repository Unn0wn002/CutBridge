$.evalFile(new File('C:/CutBridgeCloseoutR2/common.jsx'));
var cbR={status:'IN_PROGRESS',host:app.version,checks:[]};
function cbLoadClean(){if(app.project.file&&app.project.file.fsName.indexOf('C:\CutBridgeEvidence')===0)app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);app.open(new File('C:/CutBridgeEvidence/r2/native025-artist-V003.aep'));CutBridgeContract.loadManifest('C:/CutBridgeInputsR2/\u30d1\u30c3\u30b1\u30fc\u30b8/Native025_EP01_SC010_C001_T01_V003/cutbridge.json');CutBridgeContract.getState().comp=cbComp();}
function cbRecord(n,ok,d){cbR.checks.push({name:n,passed:!!ok,details:d});cbSave('native-negative-ownership',cbR);}
try{
$.evalFile(new File('C:/CutBridgeInputsR2/ae/CutBridge.jsx'));
cbLoadClean();cbComp().layer('LINE').remove();var cbBefore=cbSnapshot();var cbQC=CutBridgeContract.runQC();cbRecord('deleted required layer QC fails closed',cbQC.report.summary.ERROR>0&&cbJson(cbSnapshot())===cbJson(cbBefore),cbQC);
cbLoadClean();cbComp().layer('LINE').comment='ARTIST_DETAGGED';cbBefore=cbSnapshot();cbQC=CutBridgeContract.runQC();cbRecord('detagged required layer QC fails closed',cbQC.report.summary.ERROR>0&&cbJson(cbSnapshot())===cbJson(cbBefore),cbQC);
cbLoadClean();var cbFolder=cbComp().parentFolder;cbFolder.name='ARTIST_RENAMED_COMP_FOLDER';cbBefore=cbSnapshot();var cbItems=app.project.numItems,cbBuild=CutBridgeContract.buildComp();cbQC=CutBridgeContract.runQC();cbRecord('missing managed folder Build and QC fail closed',!cbBuild.success&&cbQC.report.summary.ERROR>0&&app.project.numItems===cbItems&&cbJson(cbSnapshot())===cbJson(cbBefore),{build:cbBuild,qc:cbQC});
cbLoadClean();cbFolder=app.project.items.addFolder('01_COMP');cbFolder.parentFolder=cbComp().parentFolder.parentFolder;cbBefore=cbSnapshot();cbItems=app.project.numItems;cbBuild=CutBridgeContract.buildComp();cbQC=CutBridgeContract.runQC();cbRecord('duplicate managed folder Build and QC fail closed',!cbBuild.success&&cbQC.report.summary.ERROR>0&&app.project.numItems===cbItems&&cbJson(cbSnapshot())===cbJson(cbBefore),{build:cbBuild,qc:cbQC});
cbLoadClean();cbR.status='PASS';for(var cbI=0;cbI<cbR.checks.length;cbI++)if(!cbR.checks[cbI].passed)cbR.status='FAIL';
}catch(cbE){cbR.status='FAIL';cbR.error=String(cbE);cbR.line=cbE.line;}cbSave('native-negative-ownership',cbR);

