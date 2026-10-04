$.evalFile(new File('C:/CutBridgeCases/common.jsx'));
var cbR={host:app.version,status:'FAIL',error:'Native required-to-optional revision failed: Object is invalid; rollback incomplete',items:[]};
try{cbR.layers=cbSnapshot();}catch(cbE){cbR.snapshotError=String(cbE);}
for(var cbI=1;cbI<=app.project.numItems;cbI++){try{var cbItem=app.project.item(cbI);cbR.items.push({id:cbItem.id,name:cbItem.name,comment:cbItem.comment,parent:cbItem.parentFolder?cbItem.parentFolder.name:null,file:cbItem instanceof FootageItem&&cbItem.file?cbItem.file.fsName:null});}catch(cbE){cbR.items.push({index:cbI,error:String(cbE)});}}
try{app.project.save(new File('C:/CutBridgeEvidence/r2/native025-status-failed.aep'));cbR.savedFailureProject=true;}catch(cbE){cbR.saveError=String(cbE);}cbSave('status-change-native-failure',cbR);
