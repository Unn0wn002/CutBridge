"""CutBridge version and compatibility constants.

Keep ``__version__`` synchronized with ``blender_manifest.toml``. CI enforces this.
"""

__version__ = "0.2.3"
VERSION = (0, 2, 3)

BLENDER_VERSION_MIN = (4, 2, 0)
TARGET_LTS_SERIES = ((4, 2), (4, 5), (5, 2))

UPDATE_INDEX_SCHEMA_VERSION = 1

# The private source repository is intentionally not an update endpoint.
# This transport endpoint is compiled into a distribution build rather than
# persisted as a Blender RNA preference.
DEFAULT_UPDATE_INDEX_URL = ""
