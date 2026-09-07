import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSX = ROOT / "apps" / "after-effects" / "CutBridge.jsx"


def test_new_managed_comp_tag_failure_rolls_back_without_accumulation():
    source = JSX.read_text(encoding="utf-8")
    start = source.index("    function ensureManagedComp(")
    end = source.index("\n\n    function findManagedLayer", start)
    function_source = source[start:end].strip()

    node_script = f"""
const assert = require('assert');
function CompItem() {{}}
const CutBridgeContract = {{
  managedTag: () => 'CUTBRIDGE|1|comp|fixture|CUT001_COMP',
  expectedCompSpec: () => ({{width: 1920, height: 1080, pixelAspect: 1, duration: 1, frameRate: 24}}),
  compSpecErrors: () => []
}};
function findTaggedProjectItem() {{ return null; }}
function findNamedComp() {{ return null; }}
function setItemComment(item, value) {{ item.comment = value; }}

let liveCreatedComps = 0;
let addCount = 0;
let removeCount = 0;
const artistComp = {{name: 'artist-comp', untouched: true}};
const compFolder = {{name: '01_COMP'}};

const app = {{
  project: {{
    items: {{
      addComp(name, width, height, pixelAspect, duration, frameRate) {{
        addCount += 1;
        liveCreatedComps += 1;
        const comp = new CompItem();
        comp.name = name;
        comp.width = width;
        comp.height = height;
        comp.pixelAspect = pixelAspect;
        comp.duration = duration;
        comp.frameRate = frameRate;
        comp.remove = function() {{
          removeCount += 1;
          liveCreatedComps -= 1;
        }};
        Object.defineProperty(comp, 'comment', {{
          configurable: true,
          set() {{ throw new Error('comment tagging unavailable'); }}
        }});
        return comp;
      }}
    }}
  }}
}};

eval({json.dumps(function_source)});

for (let attempt = 0; attempt < 2; attempt += 1) {{
  assert.throws(
    () => ensureManagedComp({{}}, compFolder, 'CUT001_COMP'),
    /rolled back|comments are required|initialization failed/i
  );
  assert.strictEqual(liveCreatedComps, 0, 'failed retry must restore the pre-build comp count');
  assert.strictEqual(artistComp.untouched, true, 'unrelated artist comps must remain untouched');
}}

assert.strictEqual(addCount, 2, 'each retry may create only its own temporary comp');
assert.strictEqual(removeCount, 2, 'each failed temporary comp must be removed');
"""

    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
