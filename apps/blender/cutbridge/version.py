"""CutBridge version and compatibility constants.

Keep ``__version__`` synchronized with ``blender_manifest.toml``. CI enforces this.
"""

__version__ = "0.2.5"
VERSION = (0, 2, 5)

BLENDER_VERSION_MIN = (4, 2, 0)
TARGET_LTS_SERIES = ((4, 2), (4, 5), (5, 2))

UPDATE_INDEX_SCHEMA_VERSION = 1

# The source repository is intentionally not an update endpoint. This verified
# production URL stays outside Blender RNA preferences and never carries secrets.
DEFAULT_UPDATE_INDEX_URL = (
    "https://unn0wn002.github.io/cutbridge-distribution/"
    "cutbridge/release-index.json"
)
