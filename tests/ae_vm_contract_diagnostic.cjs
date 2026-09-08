const vm = require('node:vm');
const fs = require('node:fs');
const C = require('../apps/after-effects/CutBridge.jsx');

function m(version) {
    return {
        schema: 'cutbridge-manifest', schema_version: 1, cutbridge_version: '0.2.3',
        project: '作品', episode: 'E01', scene: 'S001', cut: 'C001', take: 'T01',
        package_name: '作品_E01_S001_C001_T01_V' + String(version).padStart(3, '0'),
        version, fps: 24, frames: {start: 0, end: 23, count: 24},
        resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        passes: [
            {name: 'BEAUTY', path: 'beauty', sequence_pattern: 'b####.png', required: true},
            {name: 'LINE', path: 'line', sequence_pattern: 'l####.png', required: false}
        ]
    };
}

const current = m(1);
const next = m(2);
console.log('DIRECT_CURRENT=' + JSON.stringify(C.validateManifest(current)));
console.log('DIRECT_NEXT=' + JSON.stringify(C.validateManifest(next)));
const source = fs.readFileSync(require.resolve('../apps/after-effects/revision_manager.js'), 'utf8');
const context = {CutBridgeContract: C};
vm.runInNewContext(source, context);
const result = context.CutBridgeRevisionManager.assess(current, next);
console.log('VM_ASSESS=' + JSON.stringify(result));
if (result.status !== 'safe') process.exit(23);
