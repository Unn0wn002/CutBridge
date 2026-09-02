"""CutBridge version and compatibility constants.

Keep ``__version__`` synchronized with ``blender_manifest.toml``. CI enforces this.
"""

__version__ = "0.2.0"
VERSION = (0, 2, 0)

BLENDER_VERSION_MIN = (4, 2, 0)
TARGET_LTS_SERIES = ((4, 2), (4, 5))

UPDATE_INDEX_SCHEMA_VERSION = 1

# The private source repository is intentionally not an update endpoint.
# Set this to a separately hosted distribution index when that endpoint exists.
DEFAULT_UPDATE_INDEX_URL = ""
