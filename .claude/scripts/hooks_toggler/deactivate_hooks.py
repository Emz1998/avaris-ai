import sys
import json
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import get_json, set_json, get_cache, set_cache, clear_cache  # type: ignore

SETTINGS_FILE = ".claude/settings.local.json"
CACHE_FILE = ".claude/scripts/hooks_toggler/cache.json"


def deactivate_hooks() -> None:
    data = get_json("hooks", {}, SETTINGS_FILE)
    if not data:
        print("No hooks to deactivate")
        return
    set_cache(
        "hooks",
        data,
        CACHE_FILE,
    )
    set_json("hooks", {}, SETTINGS_FILE)


if __name__ == "__main__":
    deactivate_hooks()
