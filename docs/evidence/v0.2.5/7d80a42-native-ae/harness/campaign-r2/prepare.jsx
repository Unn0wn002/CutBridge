$.evalFile(new File('C:/CutBridgeCampaignR2/common.jsx'));
var cbPrep={status:'IN_PROGRESS',host:app.version,temp:$.getenv('TEMP')};
try{
app.open(new File('C:/CutBridgeEvidence/r2/native025-stage1.aep'));
$.evalFile(new File('C:/CutBridgeInputsR2/ae/CutBridge.jsx'));
CutBridgeContract.loadManifest('C:/CutBridgeInputsR2/\u30d1\u30c3\u30b1\u30fc\u30b8/Native025_EP01_SC010_C001_T01_V001/cutbridge.json');
var cbC=cbComp();CutBridgeContract.getState().comp=cbC;
cbPrep.handoff=cbHandoff(CutBridgeContract.getState().manifest);
var cbArtist=cbC.layers.addText('Original synthetic artist annotation');cbArtist.name='Artist Annotation';cbArtist.comment='ARTIST_UNMANAGED';
var cbBeauty=cbC.layer('BEAUTY');cbBeauty.parent=cbArtist;cbBeauty.shy=true;
var cbOpacity=cbBeauty.property('ADBE Transform Group').property('ADBE Opacity');cbOpacity.setValueAtTime(0,73);cbOpacity.setValueAtTime(1/24,61);cbOpacity.expression='value';
cbBeauty.property('ADBE Effect Parade').addProperty('ADBE Slider Control').property('ADBE Slider Control-0001').setValue(42);
var cbMask=cbBeauty.property('ADBE Mask Parade').addProperty('ADBE Mask Atom');var cbShape=new Shape();cbShape.vertices=[[10,10],[100,10],[100,100],[10,100]];cbShape.closed=true;cbMask.property('ADBE Mask Shape').setValue(cbShape);
cbArtist.moveToEnd();cbPrep.artistBefore=cbSnapshot();app.project.save(new File('C:/CutBridgeEvidence/r2/native025-artist-V001.aep'));cbPrep.status='PASS';
for(var cbI=0;cbI<cbPrep.handoff.length;cbI++)if(!cbPrep.handoff[cbI].passed)cbPrep.status='FAIL';
}catch(cbE){cbPrep.status='FAIL';cbPrep.error=String(cbE);cbPrep.line=cbE.line;}cbSave('artist-preparation',cbPrep);

