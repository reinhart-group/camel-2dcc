import sys
from pathlib import Path

# Add the project root to sys.path at module-load time (before test collection)
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root))
