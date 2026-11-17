(function(){
 var out='C:/CutBridgeValidityEvidence';
 var f=new File(out+'/native-ae-stage1.json');
 function json(v){if(v===null||v===undefined)return 'null';if(typeof v==='number'||typeof v==='boolean')return String(v);if(typeof v==='string')return '"'+v.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+'"';var a=[],i;if(v instanceof Array){for(i=0;i<v.length;i++)a.push(json(v[i]));return '['+a.join(',')+']';}for(i in v)if(v.hasOwnProperty(i))a.push(json(i)+':'+json(v[i]));return '{'+a.join(',')+'}';}
 var report={host_version:app.version,candidate_sha:'049c095258f9fc2dd89cbf8f1d7b2b3114d80296',stage:'native-build-qc',temp:$.getenv('TEMP'),alerts:[],checks:[],status:'IN_PROGRESS'};
 function save(){if(!f.open('w'))throw Error('Output file unavailable');f.write(json(report));f.close();}
 var realAlert=alert; alert=function(message){report.alerts.push(String(message));save();};
 function check(name,value,details){report.checks.push({name:name,passed:!!value,details:details});save();if(!value)throw Error(name+' failed');}
 try{
  save();if(app.project.file&&app.project.file.fsName.indexOf('C:\\CutBridgeNativeRepairEvidence')===0)app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);if(app.project&&app.project.numItems>0)throw Error('Expected empty test project; refusing to overwrite existing content');
  $.evalFile(new File('C:/CutBridgeZipNative/ae/CutBridge.jsx'));
  check('exact packaged runtime loaded',typeof CutBridgeContract.buildComp==='function');
  CutBridgeContract.loadManifest('C:/CutBridgeInputsR2/\u30d1\u30c3\u30b1\u30fc\u30b8/Native025_EP01_SC010_C001_T01_V001/cutbridge.json');
  var built=CutBridgeContract.buildComp();check('V001 native Build',built&&built.success,built&&built.error);
  var comp=CutBridgeContract.getState().comp;
  var layers=[];for(var i=1;i<=comp.numLayers;i++){var l=comp.layer(i);layers.push({name:l.name,comment:l.comment,threeDLayer:l.threeDLayer,source:l.source?l.source.name:null});}
  report.composition={name:comp.name,width:comp.width,height:comp.height,frameRate:comp.frameRate,duration:comp.duration,layers:layers};save();
  var qc=CutBridgeContract.runQC();report.qc=qc;save();
  var errors=[];for(i=0;qc&&qc.records&&i<qc.records.length;i++)if(qc.records[i].severity==='ERROR')errors.push(qc.records[i]);
  check('V001 native QC has no errors',qc&&qc.report&&errors.length===0,errors);
  var itemCount=app.project.numItems,layerCount=comp.numLayers;
  var rebuilt=CutBridgeContract.buildComp();check('Repeat Build is idempotent',rebuilt&&rebuilt.success&&app.project.numItems===itemCount&&comp.numLayers===layerCount,{beforeItems:itemCount,afterItems:app.project.numItems,beforeLayers:layerCount,afterLayers:comp.numLayers});
  app.project.save(new File(out+'/native025-stage1.aep'));
  check('Native project saved',new File(out+'/native025-stage1.aep').exists);
  report.status='PASS';save();
 }catch(e){report.status='FAIL';report.error=String(e);report.line=e.line;save();}
 finally{alert=realAlert;}
})();


