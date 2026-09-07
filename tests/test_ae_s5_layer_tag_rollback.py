import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSX = ROOT / "apps" / "after-effects" / "CutBridge.jsx"


def test_new_managed_layer_tag_failure_rolls_back_without_accumulation():
    source = JSX.read_text(encoding="utf-8")
    start = source.index("    function ensureManagedLayer(")
    end = source.index("\n\n    function orderManagedLayers", start)
    function_source = source[start:end].strip()

    node_script = f"""
const assert = require('assert');
const state = {{layers: {{}}}};
const CutBridgeContract = {{managedTag: () => 'CUTBRIDGE|1|layer|fixture|beauty'}};
function findManagedLayer() {{ return null; }}

eval({json.dumps(function_source)});

const footage = {{id: 'managed-footage'}};
const manifest = {{}};
const artistLayer = {{name: 'artist-layer', untouched: true}};
let liveManagedLayers = 0;
let addCount = 0;
let removeCount = 0;

const comp = {{
  layers: {{
    add(source) {{
      addCount += 1;
      liveManagedLayers += 1;
      const layer = {{
        source,
        name: '',
        startTime: 123,
        remove() {{
          assert.strictEqual(this.source, footage, 'rollback must target only the just-created managed layer');
          removeCount += 1;
          liveManagedLayers -= 1;
        }}
      }};
      Object.defineProperty(layer, 'comment', {{
        configurable: true,
        set() {{ throw new Error('comment tagging unavailable'); }}
      }});
      return layer;
    }}
  }}
}};

for (let attempt = 0; attempt < 2; attempt += 1) {{
  assert.throws(
    () => ensureManagedLayer(comp, footage, manifest, 'beauty'),
    /rolled back|layer comments are required/i
  );
  assert.strictEqual(liveManagedLayers, 0, 'failed retry must restore the pre-build managed-layer count');
  assert.strictEqual(Object.keys(state.layers).length, 0, 'failed layer must never enter the managed-layer cache');
  assert.strictEqual(artistLayer.untouched, true, 'unrelated artist layers must remain untouched');
}}

assert.strictEqual(addCount, 2, 'each retry may create only its own temporary layer');
assert.strictEqual(removeCount, 2, 'each failed temporary layer must be removed');
"""

    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
