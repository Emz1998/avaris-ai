#!/usr/bin/env python3
"""Reset workflow cache to default state."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_cache, load_cache, write_cache


DEFAULT_CACHE_STATE = {
    "block_stoppage": {"condition": False, "reason": "Phase transition allowed"},
    "phases_completed": [],
    "skills_triggered": [],
    "subagents_triggered": [],
    "active_subagent": "",
    "current_phase": "explore",
    "current_subagent": "",
    "is_active": False,
    "retrigger_flag": 0,
}


def reset_cache() -> None:
    """Reset the cache to default workflow state."""
    try:
        cache = load_cache()

        # Update cache with defaults while preserving session_id if exists
        session_id = cache.get("session_id", "")

        for key, value in DEFAULT_CACHE_STATE.items():
            cache[key] = value

        if session_id:
            cache["session_id"] = session_id

        write_cache(cache)
        print("Cache reset successfully")

    except Exception as e:
        print(f"Cache reset error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    reset_cache()
