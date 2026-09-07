const assert = require("assert");
const R = require("../apps/after-effects/revision_manager.js");
function m(v, overrides) {
  const base={schema:"cutbridge-manifest",schema_version:1,version:v,package_name:"CUT|SCENE|010",project:"P",episode:"E",scene:"S",cut:"010",take:"A",fps:24,frames:{start:0,end:23,count:24},resolution:{width:1920,height:1080,pixel_aspect:1},passes:[{name:"BEAUTY",required:true,path:"beauty",sequence_pattern:"beauty####.png"},{name:"LINE",required:false,path:"line",sequence_pattern:"line####.png"}]};
  overrides=overrides||{}; Object.keys(overrides).forEach(k=>base[k]=overrides[k]); return base;
}
function status(a,s){assert.strictEqual(a.status,s,JSON.stringify(a));}
assert.strictEqual(R.revisionNumber("V001"),1); assert.strictEqual(R.revisionNumber("V002"),2); assert.strictEqual(R.revisionNumber(3),3); assert.strictEqual(R.identity(m(1)),"CUT|SCENE|010");
status(R.assess(m(1),m(2)),"safe");
status(R.assess(m(1),m(2,{resolution:{width:2048,height:1080,pixel_aspect:1}})),"warning");
status(R.assess(m(1),m(2,{fps:30})),"incompatible");
status(R.assess(m(1),m(2,{frames:{start:1,end:24,count:24}})),"incompatible");
status(R.assess(m(1),m(2,{resolution:{width:1920,height:1080,pixel_aspect:1.1}})),"incompatible");
status(R.assess(m(1),m(2,{package_name:"CUT|SCENE|011"})),"incompatible");
status(R.assess(m(1),m(2,{schema_version:2})),"incompatible");
status(R.assess(m(1),m(2,{passes:[{name:"LINE",required:false,path:"line",sequence_pattern:"line####.png"}]})),"incompatible");
assert.strictEqual(R.selectLatest(m(1),[m(2),m(3),m(1),m(4,{fps:30})]).version,3); assert.strictEqual(R.discover(m(1),[m(3),m(2)]).length,2);
const current=m(1),candidate=m(2),managed={managed:true,passName:"BEAUTY",source:"old",tag:R.managedTag("layer",current,"BEAUTY")},artist={managed:false,passName:"LINE",source:"artist",tag:"artist"};
const p=R.plan(current,candidate,[managed,artist]); status(p,"safe"); assert.strictEqual(p.actions.length,1); assert.ok(p.preserve.indexOf("effects")>=0); assert.strictEqual(R.plan(current,m(2,{package_name:"CUT|SCENE|999"}),[managed]).actions.length,0);
let removed=0; assert.throws(()=>R.apply(p,{importReplacement:()=>({id:"new"}),validateReplacement:()=>true,swapManagedSource:()=>{throw new Error("swap failed");},removeImportedReplacement:()=>{removed++;}},false),/swap failed/); assert.strictEqual(removed,1);
assert.throws(()=>R.apply(R.plan(current,m(2,{resolution:{width:2048,height:1080,pixel_aspect:1}}),[managed]),{importReplacement:()=>({}),swapManagedSource:()=>{}},false),/explicit confirmation/);
console.log("S6 revision checks: PASS");
