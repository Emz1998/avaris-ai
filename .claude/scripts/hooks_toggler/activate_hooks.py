import sys
import json
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_json, get_cache, clear_cache  # type: ignore

SETTINGS_FILE = ".claude/settings.local.json"
CACHE_FILE = ".claude/scripts/hooks_toggler/cache.json"


def reactivate_hooks() -> None:
    data = get_cache("hooks", {}, CACHE_FILE)
    if not data:
        print("No hooks to reactivate")
        return
    set_json("hooks", data, SETTINGS_FILE)


if __name__ == "__main__":
    reactivate_hooks()
